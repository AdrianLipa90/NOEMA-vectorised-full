from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.gate_contracts import (
    DoctorDecision,
    DoctorVerdict,
    GateDecision,
    GateResult,
    PhaseOperation,
)
from ciel_geometry.phasenav.phase_scheduler import ActionVector, ScheduledCandidate, select_min_action


def _candidate(op_id: str, cost: float, gate=GateDecision.OPEN, doctor=DoctorDecision.PASS):
    operation = PhaseOperation(
        operation_id=op_id,
        relation_type="test",
        source_id="state:test",
        mutation_class="READ_ONLY",
        evidence=("test:evidence",),
    )
    gate_result = GateResult(operation_id=op_id, decision=gate, score=1.0 if gate is GateDecision.OPEN else 0.0)
    doctor_result = DoctorVerdict(operation_id=op_id, decision=doctor)
    action = ActionVector(cost, cost, cost, cost, cost, cost, cost, cost, cost)
    return ScheduledCandidate(operation, gate_result, doctor_result, action)


def test_scheduler_selects_lowest_action_among_admissible_candidates():
    high = _candidate("op:high", 0.8)
    low = _candidate("op:low", 0.2)
    decision = select_min_action([high, low])
    assert decision.selected is low
    assert abs((decision.total_action or 0.0) - 0.2) < 1e-12
    assert decision.ranked[0][0] == "op:low"


def test_scheduler_cannot_override_closed_gate():
    cheap_but_closed = _candidate("op:closed", 0.0, gate=GateDecision.HOLD)
    expensive_open = _candidate("op:open", 0.7)
    decision = select_min_action([cheap_but_closed, expensive_open])
    assert decision.selected is expensive_open
    assert ("op:closed", "gate:HOLD") in decision.excluded


def test_scheduler_cannot_override_doctor_reject():
    cheap_rejected = _candidate("op:rejected", 0.0, doctor=DoctorDecision.REJECT)
    allowed = _candidate("op:allowed", 0.5)
    decision = select_min_action([cheap_rejected, allowed])
    assert decision.selected is allowed
    assert ("op:rejected", "doctor:REJECT") in decision.excluded


def test_scheduler_tie_break_is_deterministic_by_operation_id():
    b = _candidate("op:b", 0.3)
    a = _candidate("op:a", 0.3)
    decision = select_min_action([b, a])
    assert decision.selected is a
    assert [item[0] for item in decision.ranked] == ["op:a", "op:b"]


def test_no_admissible_candidate_returns_none():
    decision = select_min_action([_candidate("op:x", 0.1, gate=GateDecision.REJECT)])
    assert decision.selected is None
    assert decision.total_action is None
