from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.gate_contracts import DoctorDecision, GateDecision, ReturnReceipt
from ciel_sot_agent.pnv_promotion import attach_promotion_governor, build_promotion_plan


def _receipt(**overrides) -> ReturnReceipt:
    values = {
        "receipt_id": "return:test",
        "operation_id": "op:test",
        "before_hash": "a" * 64,
        "after_hash": "b" * 64,
        "gate_decision": GateDecision.OPEN,
        "doctor_decision": DoctorDecision.PASS,
        "actuator_status": "APPLIED",
        "promoted": False,
        "debt_id": None,
        "evidence": ("edge:source-target",),
        "provenance": ("source:test",),
    }
    values.update(overrides)
    return ReturnReceipt(**values)


def test_applied_open_pass_receipt_allows_channel_promotion():
    plan = build_promotion_plan(_receipt(), channels=("semantic", "procedural"))
    assert plan.allows_durable_promotion is True
    assert plan.decision == "ALLOW_PROMOTION"
    assert plan.memory_governor["allowed_consolidations"] == ["semantic", "procedural"]
    assert plan.memory_governor["blocked_consolidations"] == []
    assert plan.memory_governor["require_loop_coherence"] is True


def test_dry_run_receipt_cannot_promote():
    plan = build_promotion_plan(_receipt(actuator_status="DRY_RUN", after_hash="a" * 64))
    assert plan.allows_durable_promotion is False
    assert plan.decision == "HOLD_PROMOTION"
    assert "semantic" in plan.memory_governor["blocked_consolidations"]
    assert any("DRY_RUN" in reason for reason in plan.reasons)


def test_debt_blocks_promotion_even_if_other_checks_pass():
    plan = build_promotion_plan(_receipt(debt_id="debt:123"))
    assert plan.decision == "HOLD_PROMOTION"
    assert any("debt:123" in reason for reason in plan.reasons)


def test_thresholds_are_forwarded_not_invented():
    plan = build_promotion_plan(_receipt(), channel_thresholds={"semantic": 0.81})
    assert plan.memory_governor["channel_thresholds"] == {"semantic": 0.81}


def test_attach_governor_is_non_destructive_to_existing_metadata():
    plan = build_promotion_plan(_receipt())
    metadata = attach_promotion_governor({"origin": "test"}, plan)
    assert metadata["origin"] == "test"
    assert metadata["memory_governor"]["receipt_id"] == "return:test"
