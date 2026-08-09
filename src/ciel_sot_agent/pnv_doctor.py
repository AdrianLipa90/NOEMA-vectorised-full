"""Doctor adapter for the PhaseNav Gate Fabric migration.

The existing RH controller remains the diagnostic evidence source.  This
adapter converts its result plus a GateResult into the common DoctorVerdict
contract without performing any mutation.
"""
from __future__ import annotations

from typing import Any

from ciel_geometry.phasenav.gate_contracts import (
    DoctorDecision,
    DoctorVerdict,
    GateDecision,
    GateResult,
    PhaseOperation,
)


def evaluate_doctor(
    operation: PhaseOperation,
    gate: GateResult,
    snapshot: dict[str, Any] | None,
    *,
    sector: str = "generic",
) -> DoctorVerdict:
    reasons: list[str] = []
    checks: dict[str, str] = {"gate": gate.decision.value}
    evidence: list[str] = list(gate.evidence)

    if gate.decision is GateDecision.REJECT:
        return DoctorVerdict(
            operation_id=operation.operation_id,
            decision=DoctorDecision.REJECT,
            reasons=("PhaseNav gate rejected the operation", *gate.reasons, *gate.hard_failures),
            checks=checks,
            evidence=tuple(evidence),
        )

    if gate.decision is GateDecision.HOLD:
        return DoctorVerdict(
            operation_id=operation.operation_id,
            decision=DoctorDecision.HOLD,
            reasons=("PhaseNav gate held the operation", *gate.reasons),
            checks=checks,
            evidence=tuple(evidence),
        )

    if not isinstance(snapshot, dict) or not snapshot:
        return DoctorVerdict(
            operation_id=operation.operation_id,
            decision=DoctorDecision.UNKNOWN,
            reasons=("No diagnostic snapshot supplied",),
            checks=checks,
            evidence=tuple(evidence),
        )

    try:
        from integration.Orbital.main.rh_control import RHController

        rh = RHController().evaluate_snapshot(snapshot, sector=sector)
    except Exception as exc:
        return DoctorVerdict(
            operation_id=operation.operation_id,
            decision=DoctorDecision.UNKNOWN,
            reasons=(f"RH diagnostic unavailable: {type(exc).__name__}: {exc}",),
            checks=checks,
            evidence=tuple(evidence),
        )

    checks.update(
        {
            "rh_mode": rh.mode,
            "rh_severity": rh.severity,
            "effective_rh": f"{rh.effective_rh:.6f}",
            "mutation_class": operation.mutation_class,
        }
    )
    evidence.append(f"rh_control:{rh.mode}")
    reasons.extend(rh.notes)

    # The legacy RH policy already permits diagnostics in high-risk mode.  The
    # migration therefore distinguishes read-only inspection from mutation.
    if rh.severity == "high" and operation.mutates:
        decision = DoctorDecision.REJECT
        reasons.append("high RH severity forbids mutation")
    elif rh.severity == "medium" and operation.mutates:
        decision = DoctorDecision.HOLD
        reasons.append("medium RH severity holds mutation for local correction")
    else:
        decision = DoctorDecision.PASS
        reasons.append("diagnostic policy permits this operation class")

    return DoctorVerdict(
        operation_id=operation.operation_id,
        decision=decision,
        reasons=tuple(reasons),
        checks=checks,
        evidence=tuple(evidence),
    )


__all__ = ["evaluate_doctor"]
