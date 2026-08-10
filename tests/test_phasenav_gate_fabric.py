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
    GateDecision,
    ObservationClass,
    PhaseOperation,
    PhaseSpace,
    RelationalObservation,
    RelationalState,
)
from ciel_geometry.phasenav.gate_fabric import evaluate_gate
from ciel_geometry.phasenav.return_protocol import close_dry_run
from ciel_sot_agent.pnv_doctor import evaluate_doctor


PHASE = tuple([1.0] + [0.0] * 35)


def _state(**overrides):
    values = {
        "identity": "card:test",
        "kind": "card",
        "phase36": PHASE,
        "phase_space": PhaseSpace.OPERATOR_SIGNATURE_36,
        "order_parameter": 0.95,
        "holonomy_defect": 0.02,
        "associator_defect": 0.01,
        "conflict": 0.01,
        "provenance": ("source:test",),
    }
    values.update(overrides)
    return RelationalState(**values)


def _read_op(**overrides):
    values = {
        "operation_id": "op:inspect",
        "relation_type": "inspect",
        "source_id": "card:test",
        "phase_signature36": PHASE,
        "phase_signature_space": PhaseSpace.OPERATOR_SIGNATURE_36,
        "mutation_class": "READ_ONLY",
        "evidence": ("source:test",),
    }
    values.update(overrides)
    return PhaseOperation(**values)


def test_phase36_is_strict():
    with pytest.raises(ValueError):
        RelationalState(
            identity="x",
            kind="card",
            phase36=(0.0,) * 24,
            phase_space=PhaseSpace.CARD_VECTOR_36,
        )


def test_phase_vector_requires_named_coordinate_space():
    with pytest.raises(ValueError):
        RelationalState(identity="x", kind="card", phase36=PHASE)


def test_simulated_observation_is_not_canonical_evidence():
    obs = RelationalObservation(
        observation_id="obs:sim",
        source="sync-noise",
        observation_class=ObservationClass.SIMULATED,
        payload={"value": 1},
        provenance=("simulation:seed",),
    )
    assert obs.canonical_evidence_eligible is False


def test_identical_high_quality_phase_opens_read_only_gate():
    result = evaluate_gate(_read_op(), _state())
    assert result.decision is GateDecision.OPEN
    assert result.score is not None
    assert result.score >= 0.72
    assert result.metrics["phase_space_match"] == 1.0


def test_cross_space_36d_comparison_is_held_until_projection_exists():
    state = _state(phase_space=PhaseSpace.OSCILLATOR_PHASE_36)
    result = evaluate_gate(_read_op(), state)
    assert result.decision is GateDecision.HOLD
    assert result.metrics["phase_space_match"] == 0.0
    assert any("explicit projection" in reason for reason in result.reasons)


def test_missing_phase_is_hold_not_fabricated():
    result = evaluate_gate(
        _read_op(phase_signature36=None, phase_signature_space=PhaseSpace.UNKNOWN),
        _state(),
    )
    assert result.decision is GateDecision.HOLD
    assert any("no 36D phase signature" in reason for reason in result.reasons)


def test_missing_authority_is_hard_reject():
    op = _read_op(authority_requirements=("NOEMA:OWNER",))
    result = evaluate_gate(op, _state(), authority=())
    assert result.decision is GateDecision.REJECT
    assert result.hard_failures


def test_mutation_without_evidence_is_held():
    op = _read_op(
        operation_id="op:mutate",
        mutation_class="MEMORY_WRITE",
        evidence=(),
    )
    result = evaluate_gate(op, _state())
    assert result.decision is GateDecision.HOLD


def test_doctor_passes_read_only_even_in_high_rh_mode():
    gate = evaluate_gate(_read_op(), _state())
    snapshot = {
        "R_H": 100.0,
        "n_sectors": 1,
        "nonlocal_eba_defect_mean": 1.0,
        "nonlocal_coherent_fraction": 0.0,
        "euler_bridge_closure_score": 0.0,
        "nonlocal_phi_berry_mean": 3.141592653589793,
        "euler_bridge_target_phase": 0.0,
    }
    verdict = evaluate_doctor(_read_op(), gate, snapshot)
    assert verdict.decision is DoctorDecision.PASS
    assert verdict.checks["rh_severity"] == "high"


def test_doctor_rejects_mutation_in_high_rh_mode():
    op = _read_op(
        operation_id="op:mutate",
        mutation_class="MEMORY_WRITE",
        evidence=("source:test",),
    )
    gate = evaluate_gate(op, _state())
    assert gate.decision is GateDecision.OPEN
    snapshot = {
        "R_H": 100.0,
        "n_sectors": 1,
        "nonlocal_eba_defect_mean": 1.0,
        "nonlocal_coherent_fraction": 0.0,
        "euler_bridge_closure_score": 0.0,
        "nonlocal_phi_berry_mean": 3.141592653589793,
        "euler_bridge_target_phase": 0.0,
    }
    verdict = evaluate_doctor(op, gate, snapshot)
    assert verdict.decision is DoctorDecision.REJECT


def test_dry_run_never_promotes_and_preserves_state_hash():
    op = _read_op()
    state = _state()
    gate = evaluate_gate(op, state)
    doctor = DoctorVerdict(
        operation_id=op.operation_id,
        decision=DoctorDecision.PASS,
        reasons=("test",),
    )
    receipt, debt = close_dry_run(op, state, gate, doctor)
    assert debt is None
    assert receipt.promoted is False
    assert receipt.actuator_status == "DRY_RUN"
    assert receipt.before_hash == receipt.after_hash


def test_dry_run_materializes_debt_on_hold():
    op = _read_op(phase_signature36=None, phase_signature_space=PhaseSpace.UNKNOWN)
    state = _state()
    gate = evaluate_gate(op, state)
    doctor = DoctorVerdict(
        operation_id=op.operation_id,
        decision=DoctorDecision.HOLD,
        reasons=("missing phase",),
    )
    receipt, debt = close_dry_run(op, state, gate, doctor)
    assert receipt.promoted is False
    assert debt is not None
    assert debt.phase_space is state.phase_space
    assert receipt.debt_id == debt.debt_id
