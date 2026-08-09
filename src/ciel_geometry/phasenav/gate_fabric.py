"""Initial PhaseNav Gate Fabric evaluator.

This module is deliberately non-actuating. It evaluates whether a typed
PhaseOperation is admissible for a RelationalState and returns OPEN/HOLD/REJECT
with explicit evidence.

The scalar weights and thresholds below are implementation parameters for the
M2 migration slice, not physical constants. They must be calibrated against
real repository/runtime observations before promotion to a canonical policy.

Coordinate-space invariant: equal dimensionality is insufficient. A cosine
comparison is only permitted when state and operation declare the same
PhaseSpace. Cross-space execution requires an explicit projection operator.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .gate_contracts import GateDecision, GateResult, PhaseOperation, RelationalState


@dataclass(frozen=True)
class GatePolicy:
    phase_weight: float = 0.35
    order_weight: float = 0.25
    holonomy_weight: float = 0.15
    associator_weight: float = 0.15
    conflict_weight: float = 0.10
    open_threshold: float = 0.72
    hold_threshold: float = 0.45

    def __post_init__(self) -> None:
        total = (
            self.phase_weight
            + self.order_weight
            + self.holonomy_weight
            + self.associator_weight
            + self.conflict_weight
        )
        if not np.isclose(total, 1.0):
            raise ValueError(f"gate weights must sum to 1.0; got {total}")
        if not 0.0 <= self.hold_threshold <= self.open_threshold <= 1.0:
            raise ValueError("expected 0 <= hold_threshold <= open_threshold <= 1")


DEFAULT_GATE_POLICY = GatePolicy()


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _phase_similarity(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    av = np.asarray(a, dtype=np.float64)
    bv = np.asarray(b, dtype=np.float64)
    an = float(np.linalg.norm(av))
    bn = float(np.linalg.norm(bv))
    if an <= 1e-12 or bn <= 1e-12:
        return 0.0
    cosine = float(np.dot(av, bv) / (an * bn))
    return _clamp01(0.5 * (cosine + 1.0))


def _missing(required: Iterable[str], actual: Iterable[str]) -> tuple[str, ...]:
    actual_set = {str(item) for item in actual}
    return tuple(sorted(str(item) for item in required if str(item) not in actual_set))


def evaluate_gate(
    operation: PhaseOperation,
    state: RelationalState,
    *,
    authority: Iterable[str] = (),
    policy: GatePolicy = DEFAULT_GATE_POLICY,
) -> GateResult:
    """Evaluate one operation without performing it.

    Hard failures are structural/authority violations and produce REJECT.
    Missing information or a missing cross-space projection produces HOLD.
    Otherwise the bounded relational score selects OPEN/HOLD/REJECT.
    """

    reasons: list[str] = []
    hard_failures: list[str] = []
    evidence: list[str] = list(operation.evidence)
    blocking_unknowns: list[str] = []

    if operation.source_id != state.identity:
        hard_failures.append(
            f"source mismatch: operation source={operation.source_id!r} state={state.identity!r}"
        )

    missing_authority = _missing(operation.authority_requirements, authority)
    if missing_authority:
        hard_failures.append("missing authority: " + ", ".join(missing_authority))

    missing_provenance = _missing(operation.provenance_requirements, state.provenance)
    if missing_provenance:
        blocking_unknowns.append("missing provenance: " + ", ".join(missing_provenance))

    if operation.phase_signature36 is None:
        blocking_unknowns.append("operation has no 36D phase signature")
    if state.phase36 is None:
        blocking_unknowns.append("state has no 36D phase vector")

    spaces_match = (
        operation.phase_signature36 is not None
        and state.phase36 is not None
        and operation.phase_signature_space is state.phase_space
    )
    if operation.phase_signature36 is not None and state.phase36 is not None and not spaces_match:
        blocking_unknowns.append(
            "phase-space mismatch requires explicit projection: "
            f"state={state.phase_space.value} operation={operation.phase_signature_space.value}"
        )

    if operation.mutates and not operation.evidence:
        blocking_unknowns.append("mutating operation has no explicit evidence")
    if operation.mutates and not state.provenance:
        blocking_unknowns.append("mutating operation targets state without provenance")

    unknown_metrics: list[str] = []
    for name, value in (
        ("order_parameter", state.order_parameter),
        ("holonomy_defect", state.holonomy_defect),
        ("associator_defect", state.associator_defect),
        ("conflict", state.conflict),
    ):
        if value is None:
            unknown_metrics.append(name)

    # Missing quality metrics do not block pure read-only observations, but a
    # mutation must not silently treat unknown as coherent.
    if operation.mutates and unknown_metrics:
        blocking_unknowns.append("unknown mutation metrics: " + ", ".join(unknown_metrics))

    if hard_failures:
        return GateResult(
            operation_id=operation.operation_id,
            decision=GateDecision.REJECT,
            score=None,
            reasons=tuple(reasons),
            hard_failures=tuple(hard_failures),
            metrics={},
            evidence=tuple(evidence),
        )

    phase_similarity = (
        _phase_similarity(state.phase36, operation.phase_signature36)
        if spaces_match and state.phase36 is not None and operation.phase_signature36 is not None
        else 0.0
    )

    order = _clamp01(state.order_parameter if state.order_parameter is not None else 0.5)
    holonomy_quality = 1.0 - _clamp01(state.holonomy_defect if state.holonomy_defect is not None else 0.5)
    associator_quality = 1.0 - _clamp01(
        state.associator_defect if state.associator_defect is not None else 0.5
    )
    conflict_quality = 1.0 - _clamp01(state.conflict if state.conflict is not None else 0.5)

    score = _clamp01(
        policy.phase_weight * phase_similarity
        + policy.order_weight * order
        + policy.holonomy_weight * holonomy_quality
        + policy.associator_weight * associator_quality
        + policy.conflict_weight * conflict_quality
    )

    metrics = {
        "phase_similarity": phase_similarity,
        "phase_space_match": 1.0 if spaces_match else 0.0,
        "order_parameter": order,
        "holonomy_quality": holonomy_quality,
        "associator_quality": associator_quality,
        "conflict_quality": conflict_quality,
        "gate_score": score,
    }

    if blocking_unknowns:
        reasons.extend(blocking_unknowns)
        decision = GateDecision.HOLD
    elif score >= policy.open_threshold:
        decision = GateDecision.OPEN
        reasons.append("relational score meets OPEN threshold")
    elif score >= policy.hold_threshold:
        decision = GateDecision.HOLD
        reasons.append("relational score is inside HOLD band")
    else:
        decision = GateDecision.REJECT
        reasons.append("relational score is below HOLD threshold")

    return GateResult(
        operation_id=operation.operation_id,
        decision=decision,
        score=score,
        reasons=tuple(reasons),
        hard_failures=(),
        metrics=metrics,
        evidence=tuple(evidence),
    )


__all__ = ["GatePolicy", "DEFAULT_GATE_POLICY", "evaluate_gate"]
