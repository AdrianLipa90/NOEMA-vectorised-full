from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.gate_contracts import ObservationClass, PhaseSpace, RelationalObservation
from ciel_geometry.phasenav.pnv_precise import sentence_phase_precise
from ciel_sot_agent.pnv_megasorter_transport import (
    TRANSPORT_CONTRACT,
    TRANSPORT_CONTRACT_SHA256,
    TRANSPORT_DESCRIPTOR,
    build_transport_envelope,
    envelope_from_transport_dict,
    proposal_batch_to_transport_candidates,
)

CONTRACT_PATH = ROOT / "contracts" / "noema_megasorter_transport_v1.json"
FIXTURE_PATH = ROOT / "contracts" / "fixtures" / "noema_megasorter_roundtrip_v1.json"


def _sha(value: dict) -> str:
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def test_canonical_contract_artifact_matches_runtime_descriptor():
    artifact = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert artifact["descriptor"] == TRANSPORT_DESCRIPTOR
    assert artifact["descriptor_sha256"] == TRANSPORT_CONTRACT_SHA256
    assert _sha(artifact["descriptor"]) == TRANSPORT_CONTRACT_SHA256
    assert artifact["authority"] == "NOEMA"


def test_golden_roundtrip_fixture_recovers_only_originating_noema_evidence():
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert fixture["transport_contract"] == TRANSPORT_CONTRACT
    assert fixture["transport_contract_sha256"] == TRANSPORT_CONTRACT_SHA256

    envelope = envelope_from_transport_dict(fixture["envelope"])
    candidates = proposal_batch_to_transport_candidates(
        fixture["expected_proposal_batch"],
        envelope,
    )
    assert len(candidates) == 1
    operation, state = candidates[0]
    expected = fixture["expected_candidate"]
    assert operation.source_id == expected["source_id"]
    assert operation.target_id == expected["target_id"]
    assert operation.relation_type == expected["relation_type"]
    assert list(operation.evidence) == expected["evidence"]
    assert operation.mutation_class == expected["mutation_class"]
    assert operation.metadata["candidate_only"] is expected["candidate_only"]
    assert state.identity == expected["source_id"]


def test_outbound_runtime_envelope_carries_contract_fingerprint():
    text = "transport conformance observation"
    observation = RelationalObservation(
        observation_id="obs:m6:1",
        source="OCTOPUS_RAG:TEST",
        observation_class=ObservationClass.RETRIEVED,
        payload={"filename": "m6.md", "essence": text},
        provenance=("fixture:m6",),
        confidence=0.8,
        phase36=sentence_phase_precise(text),
        phase_space=PhaseSpace.PNV_PRECISE_PHASE_36,
    )
    envelope = build_transport_envelope("transport conformance", [observation])
    assert envelope.metadata["transport_contract"] == TRANSPORT_CONTRACT
    assert envelope.metadata["transport_contract_sha256"] == TRANSPORT_CONTRACT_SHA256


def test_envelope_contract_drift_is_rejected():
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    fixture["envelope"]["metadata"]["transport_contract_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        envelope_from_transport_dict(fixture["envelope"])


def test_return_contract_drift_is_rejected_before_m5_candidate_conversion():
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    envelope = envelope_from_transport_dict(fixture["envelope"])
    batch = fixture["expected_proposal_batch"]
    batch["metadata"]["transport_contract_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        proposal_batch_to_transport_candidates(batch, envelope)
