from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.gate_contracts import GateDecision, ObservationClass, PhaseSpace, RelationalObservation
from ciel_geometry.phasenav.gate_fabric import evaluate_gate
from ciel_geometry.phasenav.pnv_precise import sentence_phase_precise
from ciel_sot_agent.pnv_megasorter_bridge import (
    SCHEMA,
    build_rag_envelope,
    proposal_to_candidate_operation,
)


def _obs(idx: int, confidence: float = 0.8, text: str | None = None) -> RelationalObservation:
    text = text or f"phase memory document {idx}"
    return RelationalObservation(
        observation_id=f"obs:rag:{idx}",
        source="OCTOPUS_RAG:TEST",
        observation_class=ObservationClass.RETRIEVED,
        payload={"idx": idx, "filename": f"doc-{idx}.md", "essence": text},
        provenance=(f"knowledge-db:doc_analysis:{idx}", f"document:doc-{idx}.md"),
        confidence=confidence,
        phase36=sentence_phase_precise(text),
        phase_space=PhaseSpace.PNV_PRECISE_PHASE_36,
    )


def test_envelope_is_deterministic_and_plan_only():
    observations = [_obs(1), _obs(2)]
    a = build_rag_envelope("memory return", observations)
    b = build_rag_envelope("memory return", observations)
    assert a.batch_id == b.batch_id
    assert a.schema == SCHEMA
    assert a.mode == "PLAN_ONLY"
    assert a.metadata["authority"] == "NOEMA"


def test_only_evidenced_retrieved_for_edges_are_created():
    observations = [_obs(1), _obs(2)]
    envelope = build_rag_envelope("memory return", observations)
    assert len(envelope.nodes) == 3
    assert len(envelope.relations) == 2
    query_id = envelope.nodes[0].node_id
    assert all(rel.kind == "retrieved_for" for rel in envelope.relations)
    assert {rel.source for rel in envelope.relations} == {"obs:rag:1", "obs:rag:2"}
    assert all(rel.target == query_id for rel in envelope.relations)
    assert all(rel.evidence for rel in envelope.relations)
    assert not any(rel.source.startswith("obs:rag") and rel.target.startswith("obs:rag") for rel in envelope.relations)


def test_foreign_36d_space_is_reencoded_not_silently_relabelled():
    source_phase = tuple([0.0] * 36)
    observation = RelationalObservation(
        observation_id="obs:surface",
        source="SURFACE",
        observation_class=ObservationClass.MEASURED,
        payload={"filename": "surface", "essence": "surface phase observation"},
        provenance=("surface:phi",),
        confidence=1.0,
        phase36=source_phase,
        phase_space=PhaseSpace.OSCILLATOR_PHASE_36,
    )
    envelope = build_rag_envelope("surface", [observation])
    node = envelope.nodes[1]
    assert node.phase_space == PhaseSpace.PNV_PRECISE_PHASE_36.value
    assert node.metadata["input_phase_space"] == PhaseSpace.OSCILLATOR_PHASE_36.value
    assert node.metadata["phase_source"] == "REENCODED_FROM_TEXT"
    assert node.phase36 != source_phase


def test_inbound_proposal_recovers_original_relation_evidence():
    observation = _obs(1, text="memory return")
    envelope = build_rag_envelope("memory return", [observation])
    query_id = envelope.nodes[0].node_id
    proposal = {
        "source_card_id": observation.observation_id,
        "target_card_id": query_id,
        "gate_type": "PHASE_ALIGNMENT_GATE",
        "confidence": 0.91,
        "reason": "candidate relation",
        "mutation_allowed": False,
    }
    operation, state = proposal_to_candidate_operation(proposal, envelope)
    assert operation.metadata["candidate_only"] is True
    assert operation.evidence == observation.provenance
    assert operation.mutates is False
    assert state.identity == observation.observation_id
    gate = evaluate_gate(operation, state)
    assert gate.decision in {GateDecision.OPEN, GateDecision.HOLD}
    assert "operation has no explicit evidence" not in gate.reasons


def test_inbound_proposal_without_originating_relation_is_held():
    observations = [_obs(1), _obs(2)]
    envelope = build_rag_envelope("memory return", observations)
    proposal = {
        "source_card_id": "obs:rag:1",
        "target_card_id": "obs:rag:2",
        "gate_type": "PHASE_ALIGNMENT_GATE",
        "confidence": 0.99,
        "reason": "MegaSorter alone claims similarity",
        "mutation_allowed": False,
    }
    operation, state = proposal_to_candidate_operation(proposal, envelope)
    assert operation.evidence == ()
    gate = evaluate_gate(operation, state)
    assert gate.decision is GateDecision.HOLD
    assert "operation has no explicit evidence" in gate.reasons
