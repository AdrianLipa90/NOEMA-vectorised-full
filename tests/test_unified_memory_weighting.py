from __future__ import annotations

from pathlib import Path

from ciel_omega.memory.monolith.unified_memory import DataVector, RuleHeuristicsEngine, TMPKernel


def _strong_payload() -> dict[str, object]:
    return {
        "trusted_source": True,
        "novelty_hint": True,
        "semantic_mass": 0.86,
        "salience": 0.84,
        "confidence": 0.88,
        "coherence_index": 0.91,
        "closure_penalty": 0.08,
        "projection_confidence": 0.90,
        "phase_alignment": 0.89,
        "htri_coherence": 0.88,
        "phase_nav_similarity": 0.92,
        "affective_similarity": 0.80,
        "euler_alignment": 0.87,
        "novelty": 0.16,
        "semantic_labels": ["memory", "cqcl"],
        "cqcl_quantum_variables": {
            "semantic_mass": 0.86,
            "phase_alignment": 0.89,
            "phase_tension": 0.11,
            "j_bus_total": 0.14,
            "collatz_reduce_ratio": 0.74,
            "collatz_expand_ratio": 0.08,
            "lexical_span_norm": 0.62,
            "semantic_axes_norm": 0.57,
            "label_entropy_proxy": 0.12,
        },
    }


def _weak_payload() -> dict[str, object]:
    return {
        "contradiction_flag": True,
        "ethics_warning": True,
        "semantic_mass": 0.12,
        "salience": 0.10,
        "confidence": 0.14,
        "coherence_index": 0.16,
        "closure_penalty": 0.82,
        "projection_confidence": 0.18,
        "phase_alignment": 0.19,
        "htri_coherence": 0.15,
        "phase_nav_similarity": 0.22,
        "affective_similarity": 0.18,
        "euler_alignment": 0.20,
        "novelty": 0.80,
        "semantic_labels": ["conflict"],
        "cqcl_quantum_variables": {
            "semantic_mass": 0.12,
            "phase_alignment": 0.19,
            "phase_tension": 0.84,
            "j_bus_total": 0.79,
            "collatz_reduce_ratio": 0.10,
            "collatz_expand_ratio": 0.72,
            "lexical_span_norm": 0.18,
            "semantic_axes_norm": 0.12,
            "label_entropy_proxy": 0.86,
        },
    }


def test_rule_heuristics_engine_weight_blends_canonical_signals(tmp_path: Path) -> None:
    engine = RuleHeuristicsEngine(tmp_path)
    text = "Canonical weighting keeps the memory pipeline coherent."

    strong = engine.weight({
        "D_C": "context",
        "D_S": text,
        "D_A": ["link-a"],
        "D_M": _strong_payload(),
    })
    weak = engine.weight({
        "D_C": "context",
        "D_S": text,
        "D_A": ["link-a"],
        "D_M": _weak_payload(),
    })

    assert all(0.0 <= value <= 1.0 for value in strong.values())
    assert all(0.0 <= value <= 1.0 for value in weak.values())
    assert strong["W_L"] > weak["W_L"]
    assert strong["W_S"] > weak["W_S"]
    assert strong["W_K"] > weak["W_K"]
    assert strong["W_E"] > weak["W_E"]


def test_tmpkernel_exposes_canonical_weighting(tmp_path: Path) -> None:
    kernel = TMPKernel(tmp_path)
    data = DataVector(
        context="context",
        sense="Canonical weighting keeps the memory pipeline coherent.",
        associations=["link-a"],
        meta=_strong_payload(),
    )

    a1 = kernel.first_analysis(data)
    assert a1["verdict"] == "PASS"

    a2 = kernel.second_analysis(data, a1["D_TYPE"], a1["D_ATTR"])
    assert "canonical_weighting" in a2
    assert 0.0 <= a2["canonical_weighting"]["composite"] <= 1.0
    assert a2["canonical_weighting"]["stability"] >= 0.0

