from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.gate_contracts import DoctorDecision, GateDecision, ObservationClass, PhaseSpace, RelationalObservation
from ciel_geometry.phasenav.gate_fabric import GatePolicy
from ciel_geometry.phasenav.pnv_precise import sentence_phase_precise
from ciel_sot_agent.pnv_cycle import evaluate_megasorter_candidate_cycle
from ciel_sot_agent.pnv_megasorter_bridge import build_rag_envelope


def _observation(text: str = "memory return") -> RelationalObservation:
    return RelationalObservation(
        observation_id="obs:rag:1",
        source="OCTOPUS_RAG:TEST",
        observation_class=ObservationClass.RETRIEVED,
        payload={"idx": 1, "filename": "memory.md", "essence": text},
        provenance=("knowledge-db:doc_analysis:1", "document:memory.md"),
        confidence=0.9,
        phase36=sentence_phase_precise(text),
        phase_space=PhaseSpace.PNV_PRECISE_PHASE_36,
    )


def _healthy_snapshot() -> dict:
    return {
        "R_H": 0.0,
        "n_sectors": 1,
        "nonlocal_eba_defect_mean": 0.0,
        "nonlocal_coherent_fraction": 1.0,
        "euler_bridge_closure_score": 1.0,
        "nonlocal_phi_berry_mean": 0.0,
        "euler_bridge_target_phase": 0.0,
    }


def test_full_candidate_cycle_can_validate_but_cannot_promote_without_actuator():
    observation = _observation()
    envelope = build_rag_envelope("memory return", [observation])
    query_id = envelope.nodes[0].node_id
    proposal = {
        "source_card_id": observation.observation_id,
        "target_card_id": query_id,
        "gate_type": "PHASE_ALIGNMENT_GATE",
        "confidence": 0.95,
        "mutation_allowed": False,
    }
    permissive_for_test = GatePolicy(open_threshold=0.0, hold_threshold=0.0)
    result = evaluate_megasorter_candidate_cycle(
        proposal,
        envelope,
        diagnostic_snapshot=_healthy_snapshot(),
        gate_policy=permissive_for_test,
    )
    assert result.gate.decision is GateDecision.OPEN
    assert result.doctor.decision is DoctorDecision.PASS
    assert result.receipt.actuator_status == "DRY_RUN"
    assert result.receipt.promoted is False
    assert result.mutation_occurred is False
    assert result.debt is None
    assert result.promotion.decision == "HOLD_PROMOTION"
    assert any("DRY_RUN" in reason for reason in result.promotion.reasons)


def test_unbacked_megasorter_relation_turns_into_debt_not_action():
    observations = [_observation("alpha"), RelationalObservation(
        observation_id="obs:rag:2",
        source="OCTOPUS_RAG:TEST",
        observation_class=ObservationClass.RETRIEVED,
        payload={"idx": 2, "filename": "beta.md", "essence": "beta"},
        provenance=("knowledge-db:doc_analysis:2", "document:beta.md"),
        confidence=0.9,
        phase36=sentence_phase_precise("beta"),
        phase_space=PhaseSpace.PNV_PRECISE_PHASE_36,
    )]
    envelope = build_rag_envelope("query", observations)
    proposal = {
        "source_card_id": "obs:rag:1",
        "target_card_id": "obs:rag:2",
        "gate_type": "PHASE_ALIGNMENT_GATE",
        "confidence": 1.0,
        "mutation_allowed": False,
    }
    result = evaluate_megasorter_candidate_cycle(
        proposal,
        envelope,
        diagnostic_snapshot=_healthy_snapshot(),
    )
    assert result.gate.decision is GateDecision.HOLD
    assert result.doctor.decision is DoctorDecision.HOLD
    assert result.debt is not None
    assert result.receipt.debt_id == result.debt.debt_id
    assert result.promotion.decision == "HOLD_PROMOTION"
