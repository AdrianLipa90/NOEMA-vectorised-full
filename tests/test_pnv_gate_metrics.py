from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.gate_contracts import GateDecision, PhaseOperation, PhaseSpace, RelationalState
from ciel_geometry.phasenav.gate_fabric import evaluate_gate


def _state(space: PhaseSpace, phase: tuple[float, ...]) -> RelationalState:
    return RelationalState(
        identity="state:test",
        kind="test",
        phase36=phase,
        phase_space=space,
        order_parameter=1.0,
        holonomy_defect=0.0,
        associator_defect=0.0,
        conflict=0.0,
        provenance=("source:test",),
    )


def _op(space: PhaseSpace, phase: tuple[float, ...], *, evidence=("source:test",)) -> PhaseOperation:
    return PhaseOperation(
        operation_id="op:test",
        relation_type="inspect",
        source_id="state:test",
        phase_signature36=phase,
        phase_signature_space=space,
        mutation_class="READ_ONLY",
        evidence=evidence,
    )


def test_read_only_operation_without_evidence_is_held():
    phase = tuple([0.0] * 36)
    gate = evaluate_gate(
        _op(PhaseSpace.PNV_PRECISE_PHASE_36, phase, evidence=()),
        _state(PhaseSpace.PNV_PRECISE_PHASE_36, phase),
    )
    assert gate.decision is GateDecision.HOLD
    assert "operation has no explicit evidence" in gate.reasons


def test_angle_space_uses_circular_metric():
    # 0 and 2π-ε are nearly identical on S¹ even though raw coordinate values differ strongly.
    epsilon = 1e-4
    a = tuple([0.0] * 36)
    b = tuple([2.0 * math.pi - epsilon] * 36)
    gate = evaluate_gate(
        _op(PhaseSpace.PNV_PRECISE_PHASE_36, b),
        _state(PhaseSpace.PNV_PRECISE_PHASE_36, a),
    )
    assert gate.metrics["phase_metric_circular"] == 1.0
    assert gate.metrics["phase_metric_cosine"] == 0.0
    assert gate.metrics["phase_similarity"] > 0.999999


def test_operator_signature_space_uses_cosine_metric():
    a = tuple([1.0] + [0.0] * 35)
    b = tuple([1.0] + [0.0] * 35)
    gate = evaluate_gate(
        _op(PhaseSpace.OPERATOR_SIGNATURE_36, b),
        _state(PhaseSpace.OPERATOR_SIGNATURE_36, a),
    )
    assert gate.metrics["phase_metric_cosine"] == 1.0
    assert gate.metrics["phase_metric_circular"] == 0.0
    assert gate.metrics["phase_similarity"] == 1.0


def test_unregistered_card_vector_metric_holds_instead_of_guessing():
    phase = tuple([0.2] * 36)
    gate = evaluate_gate(
        _op(PhaseSpace.CARD_VECTOR_36, phase),
        _state(PhaseSpace.CARD_VECTOR_36, phase),
    )
    assert gate.decision is GateDecision.HOLD
    assert any("no registered gate metric" in reason for reason in gate.reasons)
