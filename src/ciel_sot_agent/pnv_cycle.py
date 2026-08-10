"""Reference PLAN_ONLY evaluation cycle for the consolidated NOEMA runtime.

This module connects the current architecture without introducing mutation:

    MegaSorter proposal
      -> PhaseOperation + RelationalState
      -> PhaseNav Gate Fabric
      -> Doctor
      -> dry-run ReturnReceipt / RelationalDebt
      -> PromotionPlan

The expected M2/M3 terminal state is promotion HOLD because no real Actuator
has run.  This is intentional and testable.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from ciel_geometry.phasenav.gate_contracts import (
    DoctorVerdict,
    GateResult,
    PhaseOperation,
    RelationalState,
    ReturnReceipt,
    UnresolvedRelationalDebt,
)
from ciel_geometry.phasenav.gate_fabric import GatePolicy, evaluate_gate
from ciel_geometry.phasenav.return_protocol import close_dry_run

from .pnv_doctor import evaluate_doctor
from .pnv_megasorter_bridge import MegaSorterEnvelope, proposal_to_candidate_operation
from .pnv_promotion import PromotionPlan, build_promotion_plan


@dataclass(frozen=True)
class PlanOnlyCycleResult:
    operation: PhaseOperation
    state: RelationalState
    gate: GateResult
    doctor: DoctorVerdict
    receipt: ReturnReceipt
    debt: UnresolvedRelationalDebt | None
    promotion: PromotionPlan

    @property
    def mutation_occurred(self) -> bool:
        return self.receipt.actuator_status == "APPLIED"


def evaluate_megasorter_candidate_cycle(
    proposal: Mapping[str, Any],
    envelope: MegaSorterEnvelope,
    *,
    diagnostic_snapshot: dict[str, Any] | None,
    sector: str = "generic",
    authority: tuple[str, ...] = (),
    gate_policy: GatePolicy | None = None,
) -> PlanOnlyCycleResult:
    """Run one complete non-mutating candidate cycle."""

    operation, state = proposal_to_candidate_operation(proposal, envelope)
    gate_kwargs: dict[str, Any] = {"authority": authority}
    if gate_policy is not None:
        gate_kwargs["policy"] = gate_policy
    gate = evaluate_gate(operation, state, **gate_kwargs)
    doctor = evaluate_doctor(operation, gate, diagnostic_snapshot, sector=sector)
    receipt, debt = close_dry_run(operation, state, gate, doctor)
    promotion = build_promotion_plan(receipt)
    return PlanOnlyCycleResult(
        operation=operation,
        state=state,
        gate=gate,
        doctor=doctor,
        receipt=receipt,
        debt=debt,
        promotion=promotion,
    )


__all__ = ["PlanOnlyCycleResult", "evaluate_megasorter_candidate_cycle"]
