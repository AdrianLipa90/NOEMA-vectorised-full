"""Promotion/Sophia adapter for governed NOEMA memory.

Promotion is evaluated *after* Return.  This module converts a ReturnReceipt
into channel-scoped `memory_governor` metadata understood by the existing
governed holonomic memory orchestrator.

It performs no consolidation itself.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from ciel_geometry.phasenav.gate_contracts import DoctorDecision, GateDecision, ReturnReceipt


@dataclass(frozen=True)
class PromotionPlan:
    operation_id: str
    decision: str
    channels: tuple[str, ...]
    reasons: tuple[str, ...]
    evidence: tuple[str, ...]
    memory_governor: Mapping[str, Any]

    @property
    def allows_durable_promotion(self) -> bool:
        return self.decision == "ALLOW_PROMOTION"


def build_promotion_plan(
    receipt: ReturnReceipt,
    *,
    channels: Sequence[str] = ("semantic", "procedural", "affective"),
    require_loop_coherence: bool = True,
    channel_thresholds: Mapping[str, float] | None = None,
) -> PromotionPlan:
    """Build a non-mutating channel promotion plan from a Return receipt."""

    selected = tuple(dict.fromkeys(str(channel) for channel in channels))
    reasons: list[str] = []

    if receipt.gate_decision is not GateDecision.OPEN:
        reasons.append(f"gate is {receipt.gate_decision.value}, not OPEN")
    if receipt.doctor_decision is not DoctorDecision.PASS:
        reasons.append(f"doctor is {receipt.doctor_decision.value}, not PASS")
    if receipt.actuator_status != "APPLIED":
        reasons.append(f"actuator status is {receipt.actuator_status}, not APPLIED")
    if not receipt.after_hash:
        reasons.append("missing after_hash")
    if not receipt.provenance:
        reasons.append("missing provenance")
    if receipt.debt_id:
        reasons.append(f"unresolved relational debt: {receipt.debt_id}")

    allow = not reasons
    decision = "ALLOW_PROMOTION" if allow else "HOLD_PROMOTION"

    governor: dict[str, Any] = {
        "status": "pnv_promotion_open" if allow else "pnv_promotion_hold",
        "require_loop_coherence": bool(require_loop_coherence),
        "receipt_id": receipt.receipt_id,
        "operation_id": receipt.operation_id,
        "gate_decision": receipt.gate_decision.value,
        "doctor_decision": receipt.doctor_decision.value,
        "actuator_status": receipt.actuator_status,
        "promotion_decision": decision,
    }
    if allow:
        governor["allowed_consolidations"] = list(selected)
        governor["blocked_consolidations"] = []
    else:
        governor["allowed_consolidations"] = []
        governor["blocked_consolidations"] = list(selected)
        governor["hold_reasons"] = list(reasons)

    if channel_thresholds is not None:
        # Threshold values remain explicit caller policy.  This adapter does
        # not invent replacement memory thresholds.
        governor["channel_thresholds"] = {
            str(key): float(value) for key, value in channel_thresholds.items()
        }

    return PromotionPlan(
        operation_id=receipt.operation_id,
        decision=decision,
        channels=selected,
        reasons=tuple(reasons),
        evidence=tuple(dict.fromkeys([*receipt.evidence, *receipt.provenance])),
        memory_governor=governor,
    )


def attach_promotion_governor(metadata: Mapping[str, Any] | None, plan: PromotionPlan) -> dict[str, Any]:
    """Return new metadata with the governed-orchestrator contract attached."""

    result = dict(metadata or {})
    result["memory_governor"] = dict(plan.memory_governor)
    return result


__all__ = ["PromotionPlan", "build_promotion_plan", "attach_promotion_governor"]
