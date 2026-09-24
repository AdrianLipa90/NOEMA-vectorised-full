from __future__ import annotations

import hashlib
import math
from typing import Any

from .features import clamp01
from .schema import CanonicalArtifact, FeatureSummary, PhaseVectorRecord

PHASENAV_24D_COMPONENTS = [
    "semantic_mass",
    "semantic_phase_sin",
    "semantic_phase_cos",
    "htri_phase_sin",
    "htri_phase_cos",
    "phase_alignment",
    "phase_tension",
    "collatz_reduce_ratio",
    "collatz_expand_ratio",
    "collatz_balance",
    "j_phase_cost",
    "j_semantic_cost",
    "j_collatz_cost",
    "j_bus_total",
    "cqcl_semantic_mass",
    "cqcl_phase_alignment",
    "cqcl_j_bus_total",
    "lexical_span_norm",
    "semantic_axes_norm",
    "label_entropy_proxy",
    "htri_oscillator_norm",
    "card_kind_operator",
    "noema_provenance_norm",
    "kappa_potential",
]


def sha_to_unit_interval(hex_digest: str, start: int = 0, length: int = 8) -> float:
    part = hex_digest[start : start + length]
    if not part:
        return 0.0
    return int(part, 16) / float(16**len(part) - 1)


def angle_from_digest(hex_digest: str, start: int = 0) -> float:
    return 2.0 * math.pi * sha_to_unit_interval(hex_digest, start=start, length=12)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def euclidean_distance(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def normalised_distance(a: list[float], b: list[float]) -> float:
    # Max distance in [0,1]^24 is sqrt(24)
    return clamp01(euclidean_distance(a, b) / math.sqrt(len(a)))


def phase_vector_digest(vector: list[float], artifact_sha256: str) -> str:
    serial = artifact_sha256 + ":" + ",".join(f"{x:.12f}" for x in vector)
    return hashlib.sha256(serial.encode("utf-8")).hexdigest()


def build_phase_vector(artifact: CanonicalArtifact, features: FeatureSummary) -> PhaseVectorRecord:
    artifact_angle = angle_from_digest(artifact.sha256, 0)
    b64_angle = angle_from_digest(artifact.base64_sha256, 0)

    semantic_phase_sin = (math.sin(artifact_angle) + 1.0) / 2.0
    semantic_phase_cos = (math.cos(artifact_angle) + 1.0) / 2.0
    htri_phase_sin = (math.sin(b64_angle) + 1.0) / 2.0
    htri_phase_cos = (math.cos(b64_angle) + 1.0) / 2.0

    # Alignment in [0,1] from phase delta.
    delta = abs(math.atan2(math.sin(artifact_angle - b64_angle), math.cos(artifact_angle - b64_angle)))
    phase_alignment = 1.0 - (delta / math.pi)
    phase_tension = 1.0 - phase_alignment

    route_total = max(1, features.collatz_reduce_count + features.collatz_expand_count)
    reduce_ratio = features.collatz_reduce_count / route_total
    expand_ratio = features.collatz_expand_count / route_total
    balance = 1.0 - abs(reduce_ratio - expand_ratio)

    size_norm = clamp01(math.log2(max(1, artifact.size_bytes)) / 32.0)
    lexical_span_norm = clamp01(math.log2(max(1, artifact.base64_length)) / 34.0)
    semantic_axes_norm = clamp01(
        0.4 * features.byte_entropy_norm
        + 0.3 * features.base64_entropy_norm
        + 0.3 * (1.0 - features.chunk_entropy_std)
    )
    label_entropy_proxy = clamp01((features.byte_entropy_norm + features.base64_entropy_norm) / 2.0)
    oscillator_norm = sha_to_unit_interval(artifact.sha256, start=12, length=8)
    provenance_norm = sha_to_unit_interval(artifact.sha256, start=24, length=8)

    j_phase_cost = phase_tension
    j_semantic_cost = clamp01(
        0.45 * features.byte_entropy_norm
        + 0.25 * features.chunk_entropy_max_delta
        + 0.15 * features.byte_zero_ratio
        + 0.15 * features.base64_padding_ratio
    )
    j_collatz_cost = clamp01(features.collatz_steps / 512.0)
    j_bus_total = clamp01((j_phase_cost + j_semantic_cost + j_collatz_cost) / 3.0)

    cqcl_semantic_mass = clamp01(0.6 * size_norm + 0.4 * label_entropy_proxy)
    cqcl_phase_alignment = phase_alignment
    cqcl_j_bus_total = j_bus_total

    card_kind_operator = 0.25  # binary artefact/self-profile operator lane
    kappa_potential = clamp01(1.0 - j_bus_total)

    vector = [
        size_norm,
        semantic_phase_sin,
        semantic_phase_cos,
        htri_phase_sin,
        htri_phase_cos,
        phase_alignment,
        phase_tension,
        reduce_ratio,
        expand_ratio,
        balance,
        j_phase_cost,
        j_semantic_cost,
        j_collatz_cost,
        j_bus_total,
        cqcl_semantic_mass,
        cqcl_phase_alignment,
        cqcl_j_bus_total,
        lexical_span_norm,
        semantic_axes_norm,
        label_entropy_proxy,
        oscillator_norm,
        card_kind_operator,
        provenance_norm,
        kappa_potential,
    ]
    vector = [clamp01(float(x)) for x in vector]
    digest = phase_vector_digest(vector, artifact.sha256)

    route = {
        "collatz_seed": features.collatz_seed,
        "steps": features.collatz_steps,
        "reduce_count": features.collatz_reduce_count,
        "expand_count": features.collatz_expand_count,
        "final": features.collatz_final,
        "dominant": "reduce" if reduce_ratio >= expand_ratio else "expand",
    }
    metric_state = {
        "norm": math.sqrt(sum(x * x for x in vector)),
        "phase_alignment": phase_alignment,
        "phase_tension": phase_tension,
        "j_bus_total": j_bus_total,
    }
    projection = (
        "binary-artifact/self-candidate"
        if j_bus_total < 0.45
        else "binary-artifact/review-candidate"
    )
    confidence = clamp01(1.0 - j_bus_total)
    canon_status = "candidate"

    return PhaseVectorRecord(
        vector=vector,
        semantic_type="binary_artifact",
        source="canonical_byte_base64_surface",
        operator="pn_bis_vectorize_v0_3",
        route=route,
        metric_state=metric_state,
        projection=projection,
        confidence=confidence,
        canon_status=canon_status,
        digest=digest,
    )


def vector_with_labels(vector: list[float]) -> dict[str, float]:
    if len(vector) != len(PHASENAV_24D_COMPONENTS):
        raise ValueError("expected 24D vector")
    return dict(zip(PHASENAV_24D_COMPONENTS, vector))


def seed_from_sha256(hex_digest: str) -> int:
    # Keep the seed bounded but digest-derived.
    return max(1, int(hex_digest[:16], 16) % 1_000_003)
