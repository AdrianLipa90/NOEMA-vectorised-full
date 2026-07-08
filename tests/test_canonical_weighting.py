from __future__ import annotations

from ciel_geometry.weighting import canonical_weighting, canonical_weighting_from_phase_metadata
from CIEL_OMEGA_COMPLETE_SYSTEM.ciel_omega.memory.semantic_scorer import score_with_noema


def _full_metadata(**overrides):
    metadata = {
        "target_phase": 0.25,
        "phi_sentence": 0.24,
        "semantic_mass": 0.84,
        "phase_alignment": 0.90,
        "coherence_index": 0.88,
        "closure_score": 0.86,
        "projection_confidence": 0.91,
        "htri_coherence": 0.87,
        "phase_lane": "phase_locked",
        "affective_similarity": 0.79,
        "euler_alignment": 0.89,
        "novelty": 0.21,
        "contradiction_risk": 0.08,
        "semantic_labels": ["memory", "cqcl"],
        "cqcl_quantum_variables": {
            "semantic_mass": 0.84,
            "phase_alignment": 0.90,
            "phase_tension": 0.10,
            "j_bus_total": 0.18,
            "collatz_reduce_ratio": 0.72,
            "collatz_expand_ratio": 0.08,
            "lexical_span_norm": 0.65,
            "semantic_axes_norm": 0.62,
            "label_entropy_proxy": 0.12,
        },
    }
    metadata.update(overrides)
    return metadata


def test_canonical_weighting_is_bounded_and_prefers_clean_signals() -> None:
    good = canonical_weighting_from_phase_metadata(_full_metadata())
    bad = canonical_weighting_from_phase_metadata(
        _full_metadata(
            semantic_mass=0.12,
            phase_alignment=0.18,
            coherence_index=0.16,
            closure_score=0.14,
            projection_confidence=0.10,
            htri_coherence=0.12,
            phase_lane="phase_saturated",
            affective_similarity=0.18,
            euler_alignment=0.15,
            novelty=0.82,
            contradiction_risk=0.86,
            cqcl_quantum_variables={
                "semantic_mass": 0.12,
                "phase_alignment": 0.18,
                "phase_tension": 0.88,
                "j_bus_total": 0.84,
                "collatz_reduce_ratio": 0.12,
                "collatz_expand_ratio": 0.76,
                "lexical_span_norm": 0.20,
                "semantic_axes_norm": 0.18,
                "label_entropy_proxy": 0.82,
            },
        )
    )

    assert 0.0 <= good["composite"] <= 1.0
    assert 0.0 <= good["stability"] <= 1.0
    assert 0.0 <= bad["composite"] <= 1.0
    assert good["composite"] > bad["composite"]
    assert good["signal_count"] >= bad["signal_count"]


def test_canonical_weighting_responds_to_phase_lane_and_cqcl() -> None:
    unlocked = canonical_weighting(
        semantic_mass=0.58,
        phase_alignment=0.55,
        coherence_index=0.52,
        closure_score=0.50,
        projection_confidence=0.56,
        htri_coherence=0.53,
        cqcl_signal=0.40,
        phase_nav_similarity=0.24,
        affective_similarity=0.50,
        euler_alignment=0.52,
        novelty=0.40,
        contradiction_risk=0.25,
    )
    locked = canonical_weighting(
        semantic_mass=0.58,
        phase_alignment=0.90,
        coherence_index=0.88,
        closure_score=0.89,
        projection_confidence=0.91,
        htri_coherence=0.90,
        cqcl_signal=0.86,
        phase_nav_similarity=0.96,
        affective_similarity=0.74,
        euler_alignment=0.90,
        novelty=0.40,
        contradiction_risk=0.08,
    )

    assert locked["composite"] > unlocked["composite"]
    assert locked["phase_nav_similarity"] > unlocked["phase_nav_similarity"]
    assert locked["cqcl_signal"] > unlocked["cqcl_signal"]


def test_score_with_noema_exposes_canonical_weighting_bundle() -> None:
    result = score_with_noema(
        "CQCL memory weights phase nav coherence",
        _full_metadata(),
    )

    assert "weighting" in result
    assert "composite" in result["weighting"]
    assert 0.0 <= result["weighting"]["composite"] <= 1.0
    assert result["weighting"]["signal_count"] >= 3.0
    assert "phase_compatibility" in result["weights"]
    assert 0.0 <= result["weights"]["phase_compatibility"] <= 1.0

