"""Minimal canonical precise PhaseNav 36D phase kernel.

Consolidated from `AdrianLipa90/noema-phasenav-core` pnv_runtime and kept
mathematically compatible with `M_sentence_phase_precise`.

This module intentionally contains only the substrate-neutral phase primitives
needed by NOEMA, Octopus RAG and MegaSorter.  It does not write the shared
surface and does not carry mutation authority.
"""
from __future__ import annotations

import decimal
import math

N = 36
PI = math.pi
TAU = 2.0 * PI
KAPPA = math.log(2.0) / (24.0 * PI)
L3 = 7
L4 = 2
L5 = 5
L_RATIO = L4 / L3
ALPHA_M = 1.0 / ((L3 * L4) ** 2 - L3**2 - L4 * L5 + L4**2 * KAPPA)
_Q_PRIMES = (3, 5, 7, 11, 13, 17)

# Decimal forms come from the audited precise encoder in noema-phasenav-core.
_LN2_OVER_12 = decimal.Decimal("0.05776226504666210911810267678818141")
_TAU_DECIMAL = decimal.Decimal("6.2831853071795864769252867665590057")

SOURCE = "noema-phasenav-core:ciel_geometry.phasenav.pnv_runtime:M_sentence_phase_precise"
ENCODER_ID = "PHASENAV_PNV_RUNTIME_CANON_PRECISE_V1"


def collatz_hash(text: str) -> int:
    """Deterministic Collatz indexing hash used by the canonical PNV encoder."""

    h = int.from_bytes(str(text).encode("utf-8"), "big") % (2**61 - 1)
    for _ in range(13):
        h = h // 2 if h % 2 == 0 else 3 * h + 1
        h %= 2**61 - 1
    return h


def phase_precise(h_int: int, axis: int) -> float:
    """Compute `(h * ln(2)/12 * (axis+1)) mod 2π` at Decimal precision."""

    if not 0 <= int(axis) < N:
        raise ValueError(f"axis must be in [0, {N - 1}]")
    with decimal.localcontext() as ctx:
        ctx.prec = 38
        exact_factor = int(h_int) * (int(axis) + 1)
        return float((decimal.Decimal(exact_factor) * _LN2_OVER_12) % _TAU_DECIMAL)


def _quark_prime(k: int) -> int:
    return _Q_PRIMES[(max(1, int(k)) - 1) % len(_Q_PRIMES)]


def phase36_from_id(entity_id: object) -> tuple[float, ...]:
    """Canonical PNV36 phase vector for a numeric or symbolic concept id."""

    try:
        k = max(1, int(str(entity_id).lstrip("Ff")))
    except (ValueError, TypeError):
        h = collatz_hash(str(entity_id).lower())
        return tuple(round(phase_precise(h, axis), 10) for axis in range(N))

    qk = _quark_prime(k)
    values: list[float] = []
    for axis in range(N):
        phase = (
            KAPPA * TAU
            + ALPHA_M * TAU * (axis % L3)
            + L_RATIO * TAU * (axis // L3)
            + (qk % L5) * TAU / L3
        ) % TAU
        values.append(round(phase, 10))
    return tuple(values)


def sentence_phase_precise(text: str) -> tuple[float, ...]:
    """Exact compatibility layer for `M_sentence_phase_precise(text)`.

    Tokenization intentionally follows the source function: lowercase and
    whitespace split.  Consumers that need another tokenizer must declare it
    before calling this primitive rather than silently changing the encoder.
    """

    words = str(text).lower().split()
    if not words:
        return phase36_from_id("1")

    sums_s = [0.0] * N
    sums_c = [0.0] * N
    for word in words:
        h = collatz_hash(word)
        for axis in range(N):
            phase = phase_precise(h, axis)
            sums_s[axis] += math.sin(phase)
            sums_c[axis] += math.cos(phase)

    count = len(words)
    return tuple(math.atan2(sums_s[i] / count, sums_c[i] / count) % TAU for i in range(N))


def order_parameter(phase36: tuple[float, ...] | list[float]) -> float:
    values = tuple(float(value) for value in phase36)
    if len(values) != N:
        raise ValueError(f"order_parameter expects {N} phases; got {len(values)}")
    s = sum(math.sin(value) for value in values)
    c = sum(math.cos(value) for value in values)
    return math.hypot(s, c) / N


def angular_distance(a: tuple[float, ...] | list[float], b: tuple[float, ...] | list[float]) -> float:
    aa = tuple(float(value) for value in a)
    bb = tuple(float(value) for value in b)
    if len(aa) != N or len(bb) != N:
        raise ValueError(f"angular_distance expects two {N}D phase vectors")
    acc = 0.0
    for x, y in zip(aa, bb):
        delta = (x - y) % TAU
        if delta > PI:
            delta = TAU - delta
        acc += delta * delta
    return math.sqrt(acc / N)


def circular_alignment(a: tuple[float, ...] | list[float], b: tuple[float, ...] | list[float]) -> float:
    """Per-axis circular phase agreement in [0, 1]."""

    aa = tuple(float(value) for value in a)
    bb = tuple(float(value) for value in b)
    if len(aa) != N or len(bb) != N:
        raise ValueError(f"circular_alignment expects two {N}D phase vectors")
    mean_cos = sum(math.cos(x - y) for x, y in zip(aa, bb)) / N
    return max(0.0, min(1.0, 0.5 * (mean_cos + 1.0)))


def semantic_mass(k: int, phase36: tuple[float, ...] | list[float]) -> float:
    """`m_k = κ(1 + α_M k) + (L4/L3) R_k`."""

    kk = max(1, int(k))
    return round(KAPPA * (1.0 + ALPHA_M * kk) + L_RATIO * order_parameter(phase36), 10)


def descriptor() -> dict[str, float | int | str]:
    return {
        "source": SOURCE,
        "encoder": ENCODER_ID,
        "dimensions": N,
        "kappa": KAPPA,
        "alpha_m": ALPHA_M,
        "L3": L3,
        "L4": L4,
        "L5": L5,
        "L_ratio": L_RATIO,
    }


__all__ = [
    "N",
    "PI",
    "TAU",
    "KAPPA",
    "ALPHA_M",
    "L3",
    "L4",
    "L5",
    "L_RATIO",
    "SOURCE",
    "ENCODER_ID",
    "collatz_hash",
    "phase_precise",
    "phase36_from_id",
    "sentence_phase_precise",
    "order_parameter",
    "angular_distance",
    "circular_alignment",
    "semantic_mass",
    "descriptor",
]
