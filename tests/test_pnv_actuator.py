from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.gate_contracts import (
    DoctorDecision,
    DoctorVerdict,
    PhaseOperation,
    PhaseSpace,
    RelationalState,
)
from ciel_geometry.phasenav.gate_fabric import evaluate_gate
from ciel_geometry.phasenav.pnv_precise import sentence_phase_precise
from ciel_sot_agent.pnv_actuator import ActuationDenied, prepare_actuation


AUTH = "NOEMA:OWNER:TEST"
PHASE = sentence_phase_precise("memory return")


def _state() -> RelationalState:
    return RelationalState(
        identity="card:test",
        kind="card",
        phase36=PHASE,
        phase_space=PhaseSpace.PNV_PRECISE_PHASE_36,
        order_parameter=0.95,
        holonomy_defect=0.01,
        associator_defect=0.01,
        conflict=0.01,
        provenance=("source:test",),
    )


def _operation(**overrides) -> PhaseOperation:
    values = {
        "operation_id": "op:write",
        "relation_type": "MEMORY_WRITE",
        "source_id": "card:test",
        "phase_signature36": PHASE,
        "phase_signature_space": PhaseSpace.PNV_PRECISE_PHASE_36,
        "mutation_class": "MEMORY_WRITE",
        "evidence": ("source:test",),
        "authority_requirements": (AUTH,),
        "reversible": True,
        "return_required": True,
    }
    values.update(overrides)
    return PhaseOperation(**values)


def _doctor(op: PhaseOperation) -> DoctorVerdict:
    return DoctorVerdict(
        operation_id=op.operation_id,
        decision=DoctorDecision.PASS,
        reasons=("validated",),
        evidence=("doctor:test",),
    )


def test_permit_requires_open_gate_passed_doctor_and_authority():
    state = _state()
    operation = _operation()
    gate = evaluate_gate(operation, state, authority=(AUTH,))
    permit = prepare_actuation(operation, state, gate, _doctor(operation), authority=(AUTH,))
    assert permit.status == "PREPARED_NOT_APPLIED"
    assert permit.operation_id == operation.operation_id
    assert permit.before_hash
    assert permit.authority == (AUTH,)
    assert permit.return_required is True


def test_missing_authority_cannot_get_permit():
    state = _state()
    operation = _operation()
    # Gate itself is already a hard reject when authority is absent.
    gate = evaluate_gate(operation, state, authority=())
    with pytest.raises(ActuationDenied):
        prepare_actuation(operation, state, gate, _doctor(operation), authority=())


def test_read_only_candidate_cannot_be_passed_to_actuator():
    state = _state()
    operation = _operation(mutation_class="READ_ONLY", authority_requirements=())
    gate = evaluate_gate(operation, state)
    with pytest.raises(ActuationDenied, match="mutation operations only"):
        prepare_actuation(operation, state, gate, _doctor(operation), authority=())


def test_irreversible_mutation_is_denied_by_initial_policy():
    state = _state()
    operation = _operation(reversible=False)
    gate = evaluate_gate(operation, state, authority=(AUTH,))
    with pytest.raises(ActuationDenied, match="reversible"):
        prepare_actuation(operation, state, gate, _doctor(operation), authority=(AUTH,))
