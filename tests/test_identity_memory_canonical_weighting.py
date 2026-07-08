from __future__ import annotations

from ciel_omega.memory import IdentityField, IdentityMemory


def _trace_window(memory: IdentityMemory, phases: list[float], start_time: float = 0.0) -> None:
    for i, phase in enumerate(phases):
        memory.state.phase = phase
        memory.observe_identity_field(start_time + i)


def test_identity_memory_consolidation_exposes_canonical_weighting() -> None:
    identity = IdentityField(initial_phase=0.5)
    strong = IdentityMemory(identity)
    weak = IdentityMemory(identity)

    _trace_window(strong, [0.50, 0.51, 0.49, 0.50], start_time=0.0)
    _trace_window(weak, [2.30, 2.45, 2.60, 2.75], start_time=100.0)

    strong_score = strong.compute_consolidation_score(eba_quality=0.92)
    weak_score = weak.compute_consolidation_score(eba_quality=0.12)

    assert strong_score.canonical_weighting
    assert weak_score.canonical_weighting
    assert 0.0 <= strong_score.canonical_weighting['composite'] <= 1.0
    assert 0.0 <= weak_score.canonical_weighting['composite'] <= 1.0
    assert strong_score.canonical_weighting['composite'] > weak_score.canonical_weighting['composite']
    assert strong_score.compute_total() > weak_score.compute_total()
