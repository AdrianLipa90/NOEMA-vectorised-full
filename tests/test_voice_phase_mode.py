from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import numpy as np


VOICE_PATH = Path(__file__).resolve().parents[1] / "src" / "ciel_geometry" / "voice.py"


def _load_voice_module():
    package = sys.modules.get("ciel_geometry")
    if package is None:
        package = types.ModuleType("ciel_geometry")
        package.__path__ = [str(VOICE_PATH.parent)]  # type: ignore[attr-defined]
        sys.modules["ciel_geometry"] = package

    weighting = sys.modules.get("ciel_geometry.weighting")
    if weighting is None:
        weighting = types.ModuleType("ciel_geometry.weighting")
        weighting.canonical_weighting_from_phase_metadata = lambda _meta: {}
        sys.modules["ciel_geometry.weighting"] = weighting

    spec = importlib.util.spec_from_file_location("ciel_geometry.voice", VOICE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    module.__package__ = "ciel_geometry"
    sys.modules["ciel_geometry.voice"] = module
    spec.loader.exec_module(module)
    return module


voice = _load_voice_module()


def _base_weights() -> dict[str, float]:
    return {
        "semantic_mass": 0.5,
        "phase_alignment": 0.5,
        "coherence_index": 0.5,
        "closure_score": 0.5,
        "projection_confidence": 0.5,
        "htri_coherence": 0.5,
        "cqcl_signal": 0.5,
        "phase_nav_similarity": 0.5,
        "affective_similarity": 0.5,
        "euler_alignment": 0.5,
        "novelty": 0.5,
        "contradiction_risk": 0.5,
        "stability": 0.5,
        "composite": 0.5,
        "signal_count": 0.0,
    }


def test_mode_from_surface_uses_derived_repair_signal(monkeypatch) -> None:
    monkeypatch.setattr(
        voice,
        "canonical_weighting_from_phase_metadata",
        lambda _meta: {
            **_base_weights(),
            "coherence_index": 0.12,
            "closure_score": 0.10,
            "projection_confidence": 0.18,
            "htri_coherence": 0.15,
            "phase_nav_similarity": 0.24,
            "affective_similarity": 0.20,
            "novelty": 0.44,
            "contradiction_risk": 0.91,
            "stability": 0.14,
            "composite": 0.16,
        },
    )

    surface = {
        "coh": 0.18,
        "gravity": [0.0, 0.04, 0.2, 0.0],
        "flavor": [0.0, 0.0, 0.0, 0.2, 0.1, 0.9],
        "attractor": "unknown",
        "attractor_err": 88.0,
    }

    assert voice.mode_from_surface(surface) == "repair"


def test_mode_from_surface_uses_derived_consolidate_signal(monkeypatch) -> None:
    monkeypatch.setattr(
        voice,
        "canonical_weighting_from_phase_metadata",
        lambda _meta: {
            **_base_weights(),
            "semantic_mass": 0.88,
            "phase_alignment": 0.79,
            "coherence_index": 0.81,
            "closure_score": 0.78,
            "projection_confidence": 0.92,
            "htri_coherence": 0.86,
            "phase_nav_similarity": 0.68,
            "affective_similarity": 0.74,
            "euler_alignment": 0.83,
            "novelty": 0.17,
            "contradiction_risk": 0.08,
            "stability": 0.84,
            "composite": 0.82,
        },
    )

    surface = {
        "coh": 0.87,
        "gravity": [0.0, 0.09, 9.4, 31.5],
        "flavor": [0.0, 0.0, 0.0, 0.7, 0.4, 0.12],
        "attractor": "locked",
        "attractor_err": 7.0,
    }

    assert voice.mode_from_surface(surface) == "consolidate"


def test_query_to_vector_is_deterministic_and_36d() -> None:
    first = voice._query_to_vector("phase nav audit")
    second = voice._query_to_vector("phase nav audit")
    empty = voice._query_to_vector("   ")

    assert first.shape == (voice.QUERY_VECTOR_DIM,)
    assert second.shape == (voice.QUERY_VECTOR_DIM,)
    assert empty.shape == (voice.QUERY_VECTOR_DIM,)
    np.testing.assert_allclose(first, second)
    np.testing.assert_allclose(empty, voice.DEFAULT_OPERATOR_VECTOR)
