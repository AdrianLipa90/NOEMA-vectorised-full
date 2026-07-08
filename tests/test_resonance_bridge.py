from pathlib import Path

from ciel_geometry.resonance_bridge import (
    apply_resonance_bridge,
    dual_surface_step,
    ensure_dual_surfaces,
    imaginalize_state,
    resonance_snapshot,
)


def test_imaginalize_state_reduces_closure_and_forces_deep_mode():
    state = imaginalize_state({"closure_penalty": 0.4, "coherence_index": 0.5, "mood": 0.1})
    assert state["closure_penalty"] < 0.4
    assert state["operating_mode"] == "deep"
    assert state["coherence_index"] > 0.5


def test_dual_surfaces_and_bridge_work(tmp_path: Path):
    real_root = tmp_path / "real"
    imaginal_root = tmp_path / "imaginal"
    ensure_dual_surfaces(real_root=real_root, imaginal_root=imaginal_root)
    snap_before = resonance_snapshot(real_root=real_root, imaginal_root=imaginal_root)
    snap_after = apply_resonance_bridge(real_root=real_root, imaginal_root=imaginal_root, coupling=0.2)

    assert 0.0 <= snap_before["phase_lock"] <= 1.0
    assert 0.0 <= snap_after["resonance_score"] <= 1.0
    assert snap_after["real"]["tick"] >= 1.0
    assert snap_after["imaginal"]["tick"] >= 1.0


def test_dual_surface_step_populates_both_manifolds(tmp_path: Path):
    payload = dual_surface_step(
        {
            "closure_penalty": 0.2,
            "coherence_index": 0.55,
            "mood": 0.1,
            "ethical_score": 0.8,
            "soul_invariant": 0.7,
            "phi_berry_mean": 0.1,
            "operating_mode": "standard",
            "source": "test",
        },
        "Adrian uruchamia dual surface",
        real_root=tmp_path / "real",
        imaginal_root=tmp_path / "imaginal",
        real_memory_root=tmp_path / "memory_real",
        imaginal_memory_root=tmp_path / "memory_imaginal",
    )
    assert "real" in payload and "imaginal" in payload
    assert payload["imaginal_state"]["operating_mode"] == "deep"
    assert payload["real"]["tick"] >= 1.0
    assert payload["imaginal"]["tick"] >= 1.0
