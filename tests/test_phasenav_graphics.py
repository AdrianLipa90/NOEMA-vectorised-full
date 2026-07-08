from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


graphics = _load_module("ciel_geometry.phasenav.graphics", SRC_ROOT / "ciel_geometry" / "phasenav" / "graphics.py")


def test_build_relational_scene_projects_matrix() -> None:
    matrix = np.array(
        [
            [0.0, 0.8, -0.3],
            [0.8, 0.0, 0.5],
            [-0.3, 0.5, 0.0],
        ],
        dtype=np.float64,
    )
    scene = graphics.build_relational_scene(matrix, ["a", "b", "c"])

    assert scene.summary["node_count"] == 3
    assert scene.summary["edge_count"] >= 2
    assert len(scene.nodes) == 3
    assert len(scene.edges) >= 2
    assert scene.to_dict()["svg"].startswith("<svg")


def test_build_memory_scene_uses_similarity_edges() -> None:
    base = np.zeros(36, dtype=np.float64)
    base[0] = 1.0
    near = base.copy()
    near[1] = 0.1
    scene = graphics.build_memory_scene(
        [
            {"label": "mem-a", "score": 0.9, "vector": base.tolist()},
            {"label": "mem-b", "score": 0.8, "vector": near.tolist()},
        ]
    )

    assert scene.summary["node_count"] == 2
    assert len(scene.edges) == 1
    assert scene.edges[0].weight > 0.9


def test_build_operator_scene_has_full_operator_set() -> None:
    scene = graphics.build_operator_scene()

    assert scene.summary["operator_count"] == 36
    assert len(scene.nodes) == 36
    assert scene.summary["edge_count"] > 0


def test_graphics_bundle_returns_selected_scene(monkeypatch) -> None:
    fake_surface = {
        "phi": np.linspace(0.0, 1.0, 36, dtype=np.float64),
        "omega": np.linspace(1.0, 2.0, 36, dtype=np.float64),
        "g": np.eye(36, dtype=np.float64) * 0.25,
    }
    monkeypatch.setattr(graphics, "ensure_surface", lambda: fake_surface)
    monkeypatch.setattr(graphics, "read_surface_state", lambda surface: {"tick": 7, "coherence": 0.75, "phi_mean": 0.12, "tau_mean": 0.34})
    monkeypatch.setattr(
        graphics,
        "query_phase_memory",
        lambda query, top_k=8: [
            type("Row", (), {
                "slot": 1,
                "score": 0.92,
                "coherence": 0.81,
                "tick": 17,
                "phase_similarity": 0.9,
                "vector_similarity": 0.88,
                "flavor_similarity": 0.77,
                "event_hash_hex": "ab" * 32,
            })(),
            type("Row", (), {
                "slot": 2,
                "score": 0.83,
                "coherence": 0.79,
                "tick": 19,
                "phase_similarity": 0.85,
                "vector_similarity": 0.8,
                "flavor_similarity": 0.7,
                "event_hash_hex": "cd" * 32,
            })(),
        ],
    )

    bundle = graphics.build_phasenav_graphics_bundle(query="memory-test", surface=fake_surface)

    assert bundle["status"] == "ok"
    assert bundle["scene_counts"]["surface"]["nodes"] == 36
    assert bundle["scene_counts"]["memory"]["nodes"] == 2
    assert bundle["scene_counts"]["operators"]["nodes"] == 36
    assert bundle["scenes"]["surface"]["svg"].startswith("<svg")
