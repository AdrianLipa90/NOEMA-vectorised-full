from __future__ import annotations

import math

from ciel_sot_agent.interoception import (
    SCHEMA,
    VECTOR_ORDER,
    build_interoceptive_readout,
    interoceptive_delta,
)
from ciel_sot_agent.phase_snapshots import build_qualisensing_snapshot


def _state(**overrides):
    state = {
        "cycle_index": 7,
        "dominant_emotion": "calm",
        "mood": 0.25,
        "soul_invariant": 0.40,
        "ethical_score": 0.90,
        "htri_coherence": 0.80,
        "jokeheal_mnemonic_pressure": 0.20,
        "jokeheal_symbolic_pull": 0.60,
        "jokeheal_recurrence_pressure": 0.30,
        "identity_phase": math.pi / 2.0,
        "phi_berry_mean": math.pi / 2.0,
        "bridge_target_phase": math.pi / 2.0,
        "memory_projection_confidence": 0.70,
        "lingo_noema_confidence": 0.75,
        "gate_confidence": 0.95,
        "closure_penalty": 0.10,
        "coherence_index": 0.88,
        "lingo_factual_validation_required": 0,
    }
    state.update(overrides)
    return state


def test_interoception_uses_existing_four_layers_only():
    readout = build_interoceptive_readout(_state())
    assert readout.schema == SCHEMA
    assert readout.source_layers == (
        "M5_affective",
        "M6_relational",
        "M9_holonomic",
        "M11_metacognitive",
    )
    assert readout.affective_triad == (0.25, 0.40, 0.90)
    assert readout.relational_triad == (0.20, 0.60, 0.30)
    assert readout.holonomic_triad == (math.pi / 2.0,) * 3
    assert readout.metacognitive_triad == (0.70, 0.75, 0.95)
    assert readout.vector_order == VECTOR_ORDER
    assert len(readout.state_vector) == len(VECTOR_ORDER)


def test_holonomic_triad_uses_phase_native_circular_resultant():
    readout = build_interoceptive_readout(_state())
    assert math.isclose(readout.phase_R, 1.0, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(readout.phase_psi, math.pi / 2.0, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(readout.berry_identity_offset, 0.0, abs_tol=1e-12)


def test_digest_is_deterministic_and_changes_with_boundary_state():
    a = build_interoceptive_readout(_state())
    b = build_interoceptive_readout(_state())
    c = build_interoceptive_readout(_state(mood=-0.25))
    assert a.source_digest == b.source_digest
    assert a.interoceptive_id == b.interoceptive_id
    assert a.source_digest != c.source_digest
    assert a.interoceptive_id != c.interoceptive_id


def test_metacognitive_confidences_are_bounded_without_rewriting_raw_affect():
    readout = build_interoceptive_readout(
        _state(
            mood=-3.0,
            soul_invariant=2.5,
            memory_projection_confidence=4.0,
            lingo_noema_confidence=-2.0,
            gate_confidence=1.4,
        )
    )
    assert readout.affective_triad[0] == -3.0
    assert readout.affective_triad[1] == 2.5
    assert readout.metacognitive_triad == (1.0, 0.0, 1.0)


def test_delta_reports_change_without_assigning_semantics():
    previous = build_interoceptive_readout(_state())
    current = build_interoceptive_readout(_state(mood=0.35, jokeheal_symbolic_pull=0.80))
    delta = interoceptive_delta(current, previous)
    assert delta["schema"] == "CIEL_INTEROCEPTIVE_DELTA_V1"
    assert delta["from"] == previous.interoceptive_id
    assert delta["to"] == current.interoceptive_id
    assert delta["l2"] > 0.0
    assert len(delta["delta"]) == len(VECTOR_ORDER)


def test_qualisensing_snapshot_contains_interoceptive_readout():
    snapshot = build_qualisensing_snapshot(_state(), phase_snapshot_id="phase:test")
    nested = snapshot.interoceptive_readout
    assert nested["schema"] == SCHEMA
    assert nested["source_layers"] == (
        "M5_affective",
        "M6_relational",
        "M9_holonomic",
        "M11_metacognitive",
    )
    assert nested["interoceptive_id"].startswith("intero:7:")
