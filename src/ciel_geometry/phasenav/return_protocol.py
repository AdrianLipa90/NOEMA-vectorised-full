"""Return protocol for the PhaseNav Gate Fabric migration.

M2 implements only a dry-run closure: it hashes the pre-state, records Gate and
Doctor outcomes, and materializes unresolved debt when closure is not admissible.
No actuator is called here.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .gate_contracts import (
    DoctorDecision,
    DoctorVerdict,
    GateDecision,
    GateResult,
    PhaseOperation,
    RelationalState,
    ReturnReceipt,
    UnresolvedRelationalDebt,
)


def _stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def state_hash(state: RelationalState) -> str:
    return _stable_hash(asdict(state))


def close_dry_run(
    operation: PhaseOperation,
    state: RelationalState,
    gate: GateResult,
    doctor: DoctorVerdict,
) -> tuple[ReturnReceipt, UnresolvedRelationalDebt | None]:
    """Close a non-mutating migration cycle and emit an auditable receipt."""

    before = state_hash(state)
    closure_material = {
        "operation_id": operation.operation_id,
        "before_hash": before,
        "gate": gate.decision.value,
        "doctor": doctor.decision.value,
    }
    receipt_id = "return:" + _stable_hash(closure_material)[:24]

    admissible = gate.decision is GateDecision.OPEN and doctor.decision is DoctorDecision.PASS
    debt: UnresolvedRelationalDebt | None = None

    if not admissible:
        debt_id = "debt:" + _stable_hash({**closure_material, "reasons": [*gate.reasons, *doctor.reasons]})[:24]
        missing_provenance = tuple(
            reason.split(":", 1)[1].strip()
            for reason in gate.reasons
            if reason.startswith("missing provenance:")
        )
        debt = UnresolvedRelationalDebt(
            debt_id=debt_id,
            origin="pnv_return_dry_run",
            operation_id=operation.operation_id,
            failed_gate=gate.decision.value,
            phase36=state.phase36,
            phase_space=state.phase_space,
            associator_defect=state.associator_defect,
            closure_defect=state.holonomy_defect,
            missing_provenance=missing_provenance,
            failed_validation=tuple(doctor.reasons),
            candidate_returns=("re-evaluate-after-evidence",),
            reasons=tuple([*gate.reasons, *gate.hard_failures, *doctor.reasons]),
            metadata={"doctor_decision": doctor.decision.value},
        )
        debt_id_value: str | None = debt.debt_id
    else:
        debt_id_value = None

    # Dry-run leaves state unchanged by definition.
    receipt = ReturnReceipt(
        receipt_id=receipt_id,
        operation_id=operation.operation_id,
        before_hash=before,
        after_hash=before,
        gate_decision=gate.decision,
        doctor_decision=doctor.decision,
        actuator_status="DRY_RUN",
        promoted=False,
        debt_id=debt_id_value,
        evidence=tuple(dict.fromkeys([*gate.evidence, *doctor.evidence])),
        provenance=state.provenance,
        metadata={"mode": "PLAN_ONLY", "state_unchanged": True, "phase_space": state.phase_space.value},
    )
    return receipt, debt


__all__ = ["state_hash", "close_dry_run"]
