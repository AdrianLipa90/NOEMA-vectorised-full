"""Guarded Actuator boundary for the NOEMA PhaseNav architecture.

This module does NOT implement a side effect. It only proves that a proposed
mutation has crossed the required boundaries and emits an immutable permit
bound to the operation and pre-state hash.

A concrete substrate adapter may be added later, but it must require this
permit rather than accepting a raw mutation request.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Iterable

from ciel_geometry.phasenav.gate_contracts import (
    DoctorDecision,
    DoctorVerdict,
    GateDecision,
    GateResult,
    PhaseOperation,
    RelationalState,
)
from ciel_geometry.phasenav.return_protocol import state_hash


class ActuationDenied(RuntimeError):
    pass


@dataclass(frozen=True)
class ActuationPermit:
    permit_id: str
    operation_id: str
    before_hash: str
    mutation_class: str
    authority: tuple[str, ...]
    evidence: tuple[str, ...]
    gate_score: float | None
    reversible: bool
    return_required: bool
    status: str = "PREPARED_NOT_APPLIED"


def _stable_permit_id(payload: dict) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str, separators=(",", ":"))
    return "permit:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def prepare_actuation(
    operation: PhaseOperation,
    state: RelationalState,
    gate: GateResult,
    doctor: DoctorVerdict,
    *,
    authority: Iterable[str],
    require_reversible: bool = True,
) -> ActuationPermit:
    """Authorize, but do not execute, one concrete mutation."""

    if not operation.mutates:
        raise ActuationDenied("Actuator accepts mutation operations only")
    if gate.operation_id != operation.operation_id or doctor.operation_id != operation.operation_id:
        raise ActuationDenied("Gate/Doctor verdict is not bound to this operation")
    if operation.source_id != state.identity:
        raise ActuationDenied("operation source does not match pre-state identity")
    if gate.decision is not GateDecision.OPEN:
        raise ActuationDenied(f"Gate decision is {gate.decision.value}, not OPEN")
    if doctor.decision is not DoctorDecision.PASS:
        raise ActuationDenied(f"Doctor decision is {doctor.decision.value}, not PASS")
    if not operation.evidence:
        raise ActuationDenied("mutation has no explicit evidence")
    if not state.provenance:
        raise ActuationDenied("pre-state has no provenance")
    if not operation.return_required:
        raise ActuationDenied("mutation must require Return closure")
    if require_reversible and not operation.reversible:
        raise ActuationDenied("current Actuator policy requires reversible mutation")

    supplied = tuple(dict.fromkeys(str(item) for item in authority))
    supplied_set = set(supplied)
    missing = tuple(req for req in operation.authority_requirements if req not in supplied_set)
    if missing:
        raise ActuationDenied("missing authority: " + ", ".join(missing))

    before = state_hash(state)
    payload = {
        "operation_id": operation.operation_id,
        "before_hash": before,
        "mutation_class": operation.mutation_class,
        "authority": supplied,
        "evidence": operation.evidence,
        "gate_decision": gate.decision.value,
        "gate_score": gate.score,
        "doctor_decision": doctor.decision.value,
        "reversible": operation.reversible,
        "return_required": operation.return_required,
    }
    return ActuationPermit(
        permit_id=_stable_permit_id(payload),
        operation_id=operation.operation_id,
        before_hash=before,
        mutation_class=operation.mutation_class,
        authority=supplied,
        evidence=operation.evidence,
        gate_score=gate.score,
        reversible=operation.reversible,
        return_required=operation.return_required,
    )


__all__ = ["ActuationDenied", "ActuationPermit", "prepare_actuation"]
