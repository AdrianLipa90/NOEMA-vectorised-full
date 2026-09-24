"""Canonical weighting helpers for CIEL / NOEMA signals.

This module collects the reusable metrics that already exist across the canon
and folds them into one bounded weighting bundle. It is intentionally small and
pure so it can be reused from memory scorers, phase buses, and future retrieval
pipelines without pulling in heavier runtime dependencies.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any


def _bounded(value: Any, default: float = 0.5) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except Exception:
        return float(default)


def _mean(values: list[float], default: float = 0.5) -> float:
    if not values:
        return float(default)
    return sum(values) / len(values)


def _lookup(mapping: Mapping[str, Any], key: str) -> Any:
    if key in mapping:
        return mapping[key]
    for section in ("noema", "cqcl_quantum_variables", "orbital_state", "weights", "metrics"):
        nested = mapping.get(section)
        if isinstance(nested, Mapping) and key in nested:
            return nested[key]
    return None


def _first_float(mapping: Mapping[str, Any], *keys: str) -> float | None:
    for key in keys:
        value = _lookup(mapping, key)
        if value is None:
            continue
        try:
            return float(value)
        except Exception:
            continue
    return None


def _circular_alignment(phase_a: float | None, phase_b: float | None) -> float:
    if phase_a is None or phase_b is None:
        return 0.5
    delta = abs(float(phase_a) - float(phase_b)) % (2.0 * math.pi)
    delta = min(delta, 2.0 * math.pi - delta)
    return max(0.0, min(1.0, 1.0 - (delta / math.pi)))


def _semantic_mass_from_metadata(
    phase_metadata: Mapping[str, Any],
    semantic: Mapping[str, Any] | None,
) -> float:
    direct_values = [
        _bounded(phase_metadata[key])
        for key in ("semantic_mass", "salience", "confidence", "novelty")
        if _lookup(phase_metadata, key) is not None
    ]
    if direct_values:
        return _bounded(_mean(direct_values, default=0.5))

    scores: list[float] = []
    if semantic:
        labels = semantic.get("labels", [])
        tokens = semantic.get("tokens", [])
        relations = semantic.get("relations", [])
        scores.extend([
            min(1.0, 0.25 + 0.06 * len(labels) + 0.01 * len(tokens) + 0.08 * len(relations)),
            min(1.0, 0.30 + 0.02 * len(tokens) + 0.05 * len(labels)),
        ])
    scores.append(0.5)
    return _bounded(_mean(scores, default=0.5))


def _projection_confidence_from_metadata(
    phase_metadata: Mapping[str, Any],
    semantic: Mapping[str, Any] | None,
) -> float:
    direct_values = [
        _bounded(phase_metadata[key])
        for key in ("projection_confidence", "semantic_density", "confidence")
        if _lookup(phase_metadata, key) is not None
    ]
    if direct_values:
        return _bounded(_mean(direct_values, default=0.5))

    scores: list[float] = []
    if semantic:
        labels = semantic.get("labels", [])
        relations = semantic.get("relations", [])
        scores.append(min(1.0, 0.30 + 0.05 * len(labels) + 0.07 * len(relations)))
    scores.append(0.5)
    return _bounded(_mean(scores, default=0.5))


def _phase_navigation_similarity(phase_metadata: Mapping[str, Any]) -> float:
    direct = _first_float(phase_metadata, "phase_nav_similarity")
    if direct is not None:
        return _bounded(direct)

    lane = str(_lookup(phase_metadata, "phase_lane") or "").strip()
    lane_weights = {
        "phase_locked": 0.96,
        "phase_coupled": 0.82,
        "phase_tension": 0.58,
        "phase_saturated": 0.24,
    }
    if lane in lane_weights:
        return lane_weights[lane]
    return 0.5


def _affective_similarity(phase_metadata: Mapping[str, Any]) -> float:
    direct = _first_float(phase_metadata, "affective_similarity")
    if direct is not None:
        return _bounded(direct)

    emotion = str(_lookup(phase_metadata, "dominant_emotion") or _lookup(phase_metadata, "affect") or "").strip().lower()
    emotion_weights = {
        "love": 0.96,
        "warmth": 0.92,
        "joy": 0.88,
        "calm": 0.80,
        "neutral": 0.60,
        "curiosity": 0.72,
        "fear": 0.24,
        "anger": 0.30,
        "conflict": 0.20,
    }
    if emotion in emotion_weights:
        return emotion_weights[emotion]

    valence = _first_float(phase_metadata, "valence")
    arousal = _first_float(phase_metadata, "arousal")
    dominance = _first_float(phase_metadata, "dominance")
    if valence is not None or arousal is not None or dominance is not None:
        return _bounded(
            0.50
            + 0.25 * float(valence or 0.0)
            - 0.10 * abs(float(arousal or 0.0))
            + 0.05 * float(dominance or 0.0)
        )
    return 0.5


def _cqcl_signal(
    phase_metadata: Mapping[str, Any],
    semantic_mass: float,
    phase_alignment: float,
    projection_confidence: float,
) -> float:
    cqcl = _lookup(phase_metadata, "cqcl_quantum_variables")
    if isinstance(cqcl, Mapping):
        positive: list[float] = []
        if "semantic_mass" in cqcl:
            positive.append(_bounded(cqcl.get("semantic_mass")))
        if "phase_alignment" in cqcl:
            positive.append(_bounded(cqcl.get("phase_alignment")))
        if "phase_tension" in cqcl:
            positive.append(1.0 - _bounded(cqcl.get("phase_tension")))
        if "j_bus_total" in cqcl:
            positive.append(1.0 - _bounded(cqcl.get("j_bus_total")))
        if "collatz_reduce_ratio" in cqcl:
            positive.append(_bounded(cqcl.get("collatz_reduce_ratio")))
        if "collatz_expand_ratio" in cqcl:
            positive.append(1.0 - _bounded(cqcl.get("collatz_expand_ratio")))
        if "lexical_span_norm" in cqcl:
            positive.append(_bounded(cqcl.get("lexical_span_norm")))
        if "semantic_axes_norm" in cqcl:
            positive.append(_bounded(cqcl.get("semantic_axes_norm")))
        if "label_entropy_proxy" in cqcl:
            positive.append(1.0 - _bounded(cqcl.get("label_entropy_proxy")))
        if positive:
            return _bounded(_mean(positive, default=0.5))

    return _bounded(_mean([semantic_mass, phase_alignment, projection_confidence], default=0.5))


def _closure_score(phase_metadata: Mapping[str, Any]) -> float:
    direct = _first_float(phase_metadata, "closure_score", "closure_quality")
    if direct is not None:
        return _bounded(direct)

    penalty = _first_float(phase_metadata, "closure_penalty", "closure_cost")
    if penalty is not None:
        return _bounded(1.0 - penalty)
    return 0.5


def _coherence_index(phase_metadata: Mapping[str, Any]) -> float:
    direct = _first_float(phase_metadata, "coherence_index", "coherence", "htri_coherence")
    if direct is not None:
        return _bounded(direct)

    noema = _lookup(phase_metadata, "noema")
    if isinstance(noema, Mapping):
        direct = _first_float(noema, "coherence_surface", "evidence_coverage")
        if direct is not None:
            return _bounded(direct)
    return 0.5


def _htri_coherence(
    phase_metadata: Mapping[str, Any],
    phase_alignment: float,
    coherence_index: float,
) -> float:
    direct = _first_float(phase_metadata, "htri_coherence")
    if direct is not None:
        return _bounded(direct)
    return _bounded(_mean([phase_alignment, coherence_index], default=0.5))


def _euler_alignment(
    phase_metadata: Mapping[str, Any],
    closure_score: float,
    coherence_index: float,
) -> float:
    direct = _first_float(phase_metadata, "euler_alignment", "holonomy_quality")
    if direct is not None:
        return _bounded(direct)
    return _bounded(_mean([closure_score, coherence_index], default=0.5))


def _novelty(phase_metadata: Mapping[str, Any], semantic_mass: float) -> float:
    direct = _first_float(phase_metadata, "novelty")
    if direct is not None:
        return _bounded(direct)
    return _bounded(1.0 - semantic_mass)


def _contradiction_risk(
    phase_metadata: Mapping[str, Any],
    coherence_index: float,
    closure_score: float,
) -> float:
    direct = _first_float(phase_metadata, "contradiction_risk")
    if direct is not None:
        return _bounded(direct)

    labels = semantic_labels(phase_metadata)
    risk = max(0.0, 1.0 - coherence_index, 1.0 - closure_score)
    if "conflict" in labels:
        risk = max(risk, 0.45)
    phase_tension = _first_float(phase_metadata, "phase_tension")
    if phase_tension is not None:
        risk = max(risk, _bounded(phase_tension))
    return _bounded(risk)


def semantic_labels(phase_metadata: Mapping[str, Any]) -> list[str]:
    labels = _lookup(phase_metadata, "semantic_labels")
    if isinstance(labels, list):
        return [str(label).lower() for label in labels]
    return []


def canonical_weighting(
    *,
    semantic_mass: float = 0.5,
    phase_alignment: float = 0.5,
    coherence_index: float = 0.5,
    closure_score: float = 0.5,
    projection_confidence: float = 0.5,
    htri_coherence: float = 0.5,
    cqcl_signal: float = 0.5,
    phase_nav_similarity: float = 0.5,
    affective_similarity: float = 0.5,
    euler_alignment: float = 0.5,
    novelty: float = 0.5,
    contradiction_risk: float = 0.1,
    signal_count: float = 0.0,
) -> dict[str, float]:
    """Compose a bounded canonical weight bundle.

    The returned mapping keeps the individual metrics visible so callers can
    inspect the contributing signals while still using the final composite for
    ranking.
    """
    semantic_mass = _bounded(semantic_mass)
    phase_alignment = _bounded(phase_alignment)
    coherence_index = _bounded(coherence_index)
    closure_score = _bounded(closure_score)
    projection_confidence = _bounded(projection_confidence)
    htri_coherence = _bounded(htri_coherence)
    cqcl_signal = _bounded(cqcl_signal)
    phase_nav_similarity = _bounded(phase_nav_similarity)
    affective_similarity = _bounded(affective_similarity)
    euler_alignment = _bounded(euler_alignment)
    novelty = _bounded(novelty)
    contradiction_risk = _bounded(contradiction_risk)

    basis = {
        "semantic_mass": 0.20,
        "phase_alignment": 0.12,
        "coherence_index": 0.10,
        "closure_score": 0.10,
        "projection_confidence": 0.12,
        "htri_coherence": 0.10,
        "cqcl_signal": 0.08,
        "phase_nav_similarity": 0.06,
        "affective_similarity": 0.04,
        "euler_alignment": 0.06,
        "novelty": 0.02,
    }

    base = (
        basis["semantic_mass"] * semantic_mass
        + basis["phase_alignment"] * phase_alignment
        + basis["coherence_index"] * coherence_index
        + basis["closure_score"] * closure_score
        + basis["projection_confidence"] * projection_confidence
        + basis["htri_coherence"] * htri_coherence
        + basis["cqcl_signal"] * cqcl_signal
        + basis["phase_nav_similarity"] * phase_nav_similarity
        + basis["affective_similarity"] * affective_similarity
        + basis["euler_alignment"] * euler_alignment
        + basis["novelty"] * novelty
    )
    stability = _bounded(_mean([
        phase_alignment,
        coherence_index,
        closure_score,
        projection_confidence,
        htri_coherence,
        cqcl_signal,
        euler_alignment,
    ]))
    composite = base * (1.0 - 0.55 * contradiction_risk) * (0.90 + 0.10 * stability)
    composite = _bounded(composite)

    return {
        "semantic_mass": semantic_mass,
        "phase_alignment": phase_alignment,
        "coherence_index": coherence_index,
        "closure_score": closure_score,
        "projection_confidence": projection_confidence,
        "htri_coherence": htri_coherence,
        "cqcl_signal": cqcl_signal,
        "phase_nav_similarity": phase_nav_similarity,
        "affective_similarity": affective_similarity,
        "euler_alignment": euler_alignment,
        "novelty": novelty,
        "contradiction_risk": contradiction_risk,
        "stability": stability,
        "composite": composite,
        "signal_count": float(signal_count),
    }


def canonical_weighting_from_phase_metadata(
    phase_metadata: Mapping[str, Any],
    *,
    semantic: Mapping[str, Any] | None = None,
    phase: float | None = None,
) -> dict[str, float]:
    """Build canonical weights from phase metadata and optional semantic cues."""
    phase_metadata = phase_metadata or {}

    explicit_signal_count = sum(
        1
        for key in (
            "semantic_mass",
            "salience",
            "confidence",
            "novelty",
            "phase_alignment",
            "coherence_index",
            "coherence",
            "closure_score",
            "closure_quality",
            "closure_penalty",
            "closure_cost",
            "projection_confidence",
            "semantic_density",
            "htri_coherence",
            "cqcl_quantum_variables",
            "phase_lane",
            "phase_nav_similarity",
            "affective_similarity",
            "dominant_emotion",
            "affect",
            "valence",
            "arousal",
            "dominance",
            "euler_alignment",
            "holonomy_quality",
            "phi_sentence",
            "semantic_phase",
            "phase",
            "target_phase",
        )
        if _lookup(phase_metadata, key) is not None
    )

    semantic_mass = _semantic_mass_from_metadata(phase_metadata, semantic)
    projection_confidence = _projection_confidence_from_metadata(phase_metadata, semantic)

    target_phase = _first_float(phase_metadata, "target_phase", "phase", "semantic_phase")
    phase_reference = _first_float(phase_metadata, "phi_sentence", "phase_reference", "semantic_phase", "phase")
    phase_alignment = _first_float(phase_metadata, "phase_alignment")
    if phase_alignment is None:
        phase_alignment = _circular_alignment(target_phase if phase is None else phase, phase_reference)
    phase_alignment = _bounded(phase_alignment)

    coherence_index = _coherence_index(phase_metadata)
    closure_score = _closure_score(phase_metadata)
    htri_coherence = _htri_coherence(phase_metadata, phase_alignment, coherence_index)
    cqcl_signal = _cqcl_signal(phase_metadata, semantic_mass, phase_alignment, projection_confidence)
    phase_nav_similarity = _phase_navigation_similarity(phase_metadata)
    affective_similarity = _affective_similarity(phase_metadata)
    euler_alignment = _euler_alignment(phase_metadata, closure_score, coherence_index)
    novelty = _novelty(phase_metadata, semantic_mass)
    contradiction_risk = _contradiction_risk(phase_metadata, coherence_index, closure_score)

    return canonical_weighting(
        semantic_mass=semantic_mass,
        phase_alignment=phase_alignment,
        coherence_index=coherence_index,
        closure_score=closure_score,
        projection_confidence=projection_confidence,
        htri_coherence=htri_coherence,
        cqcl_signal=cqcl_signal,
        phase_nav_similarity=phase_nav_similarity,
        affective_similarity=affective_similarity,
        euler_alignment=euler_alignment,
        novelty=novelty,
        contradiction_risk=contradiction_risk,
        signal_count=float(explicit_signal_count),
    )
