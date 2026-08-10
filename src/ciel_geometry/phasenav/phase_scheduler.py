"""Gate-constrained minimum-action scheduler for PhaseNav.

The scheduler never changes admissibility. It only ranks candidates that have
already received Gate OPEN and Doctor PASS.

Cost terms and weights are explicit project parameters. They are not physical
constants and should be calibrated empirically for each runtime domain.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .gate_contracts import DoctorDecision, DoctorVerdict, GateDecision, GateResult, PhaseOperation


@dataclass(frozen=True)
class ActionVector:
    phase_displacement: float
    dependency_disruption: float
    holonomy_defect: float
    associator_defect: float
    conflict: float
    mutation_cost: float
    information_loss: float
    rollback_cost: float
    compute_cost: float

    def __post_init__(self) -> None:
        for name, value in self.as_dict().items():
            if not 0.0 <= float(value) <= 1.0:
                raise ValueError(f"{name} must be in [0,1], got {value}")

    def as_dict(self) -> dict[str, float]:
        return {
            "phase_displacement": float(self.phase_displacement),
            "dependency_disruption": float(self.dependency_disruption),
            "holonomy_defect": float(self.holonomy_defect),
            "associator_defect": float(self.associator_defect),
            "conflict": float(self.conflict),
            "mutation_cost": float(self.mutation_cost),
            "information_loss": float(self.information_loss),
            "rollback_cost": float(self.rollback_cost),
            "compute_cost": float(self.compute_cost),
        }


@dataclass(frozen=True)
class SchedulerPolicy:
    weights: Mapping[str, float]

    def __post_init__(self) -> None:
        expected = set(ActionVector(0, 0, 0, 0, 0, 0, 0, 0, 0).as_dict())
        actual = set(self.weights)
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            raise ValueError(f"scheduler weight keys mismatch; missing={missing}, extra={extra}")
        if any(float(value) < 0.0 for value in self.weights.values()):
            raise ValueError("scheduler weights must be non-negative")
        total = sum(float(value) for value in self.weights.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"scheduler weights must sum to 1.0; got {total}")


DEFAULT_POLICY = SchedulerPolicy(
    weights={
        "phase_displacement": 0.18,
        "dependency_disruption": 0.16,
        "holonomy_defect": 0.11,
        "associator_defect": 0.10,
        "conflict": 0.13,
        "mutation_cost": 0.10,
        "information_loss": 0.10,
        "rollback_cost": 0.07,
        "compute_cost": 0.05,
    }
)


@dataclass(frozen=True)
class ScheduledCandidate:
    operation: PhaseOperation
    gate: GateResult
    doctor: DoctorVerdict
    action: ActionVector


@dataclass(frozen=True)
class SchedulerDecision:
    selected: ScheduledCandidate | None
    total_action: float | None
    ranked: tuple[tuple[str, float], ...]
    excluded: tuple[tuple[str, str], ...]


def action_total(action: ActionVector, policy: SchedulerPolicy = DEFAULT_POLICY) -> float:
    terms = action.as_dict()
    return sum(float(policy.weights[name]) * terms[name] for name in terms)


def select_min_action(
    candidates: Sequence[ScheduledCandidate],
    *,
    policy: SchedulerPolicy = DEFAULT_POLICY,
) -> SchedulerDecision:
    """Choose minimum action among candidates that are already admissible."""

    admissible: list[tuple[ScheduledCandidate, float]] = []
    excluded: list[tuple[str, str]] = []

    for candidate in candidates:
        op_id = candidate.operation.operation_id
        if candidate.gate.operation_id != op_id or candidate.doctor.operation_id != op_id:
            excluded.append((op_id, "verdict_binding_mismatch"))
            continue
        if candidate.gate.decision is not GateDecision.OPEN:
            excluded.append((op_id, f"gate:{candidate.gate.decision.value}"))
            continue
        if candidate.doctor.decision is not DoctorDecision.PASS:
            excluded.append((op_id, f"doctor:{candidate.doctor.decision.value}"))
            continue
        admissible.append((candidate, action_total(candidate.action, policy)))

    # Deterministic tie-break: lower total action, then operation id.
    admissible.sort(key=lambda item: (item[1], item[0].operation.operation_id))
    ranked = tuple((candidate.operation.operation_id, total) for candidate, total in admissible)
    if not admissible:
        return SchedulerDecision(
            selected=None,
            total_action=None,
            ranked=ranked,
            excluded=tuple(excluded),
        )

    selected, total = admissible[0]
    return SchedulerDecision(
        selected=selected,
        total_action=total,
        ranked=ranked,
        excluded=tuple(excluded),
    )


__all__ = [
    "ActionVector",
    "SchedulerPolicy",
    "DEFAULT_POLICY",
    "ScheduledCandidate",
    "SchedulerDecision",
    "action_total",
    "select_min_action",
]
