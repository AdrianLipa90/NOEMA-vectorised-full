from __future__ import annotations

import math
from collections import Counter

from .schema import FeatureSummary

B64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


def clamp01(x: float) -> float:
    if math.isnan(x) or math.isinf(x):
        return 0.0
    return max(0.0, min(1.0, x))


def shannon_entropy_from_counts(counts: list[int] | tuple[int, ...]) -> float:
    total = sum(counts)
    if total <= 0:
        return 0.0
    entropy = 0.0
    for c in counts:
        if c:
            p = c / total
            entropy -= p * math.log2(p)
    return entropy


def byte_histogram(data: bytes) -> list[float]:
    if not data:
        return [0.0] * 256
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    n = len(data)
    return [c / n for c in counts]


def base64_histogram(b64: str) -> list[float]:
    if not b64:
        return [0.0] * len(B64_ALPHABET)
    counts = Counter(b64)
    n = len(b64)
    return [counts.get(ch, 0) / n for ch in B64_ALPHABET]


def chunked(data: bytes, chunk_size: int = 4096) -> list[bytes]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)] or [b""]


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / len(values))


def max_delta(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return max(abs(values[i] - values[i - 1]) for i in range(1, len(values)))


def collatz_summary(seed: int, max_steps: int = 512) -> tuple[int, int, int, int]:
    """Return steps, reduce_count, expand_count, final value.

    The route is bounded and deterministic. It is a routing signal, not a proof
    of any physical claim.
    """
    n = max(1, seed)
    steps = reduce_count = expand_count = 0
    while n != 1 and steps < max_steps:
        if n % 2 == 0:
            n //= 2
            reduce_count += 1
        else:
            n = 3 * n + 1
            expand_count += 1
        steps += 1
    return steps, reduce_count, expand_count, n


def extract_features(data: bytes, b64: str, seed: int) -> FeatureSummary:
    bh = byte_histogram(data)
    byte_counts = [int(round(v * len(data))) for v in bh] if data else [0] * 256
    byte_entropy = shannon_entropy_from_counts(byte_counts)
    byte_entropy_norm = clamp01(byte_entropy / 8.0)

    b64_hist = base64_histogram(b64)
    b64_counts = [int(round(v * len(b64))) for v in b64_hist] if b64 else [0] * len(B64_ALPHABET)
    b64_entropy = shannon_entropy_from_counts(b64_counts)
    b64_entropy_norm = clamp01(b64_entropy / 6.022367813)  # log2(65)

    n = len(data) or 1
    zero_ratio = data.count(0) / n if data else 0.0
    printable_ratio = sum(1 for b in data if 32 <= b <= 126) / n if data else 0.0
    high_ratio = sum(1 for b in data if b >= 128) / n if data else 0.0
    padding_ratio = b64.count("=") / len(b64) if b64 else 0.0

    chunk_entropies = []
    for chunk in chunked(data):
        hist = byte_histogram(chunk)
        counts = [int(round(v * len(chunk))) for v in hist] if chunk else [0] * 256
        chunk_entropies.append(clamp01(shannon_entropy_from_counts(counts) / 8.0))

    steps, red, exp, final = collatz_summary(seed)

    return FeatureSummary(
        byte_entropy=byte_entropy,
        byte_entropy_norm=byte_entropy_norm,
        byte_zero_ratio=clamp01(zero_ratio),
        byte_printable_ratio=clamp01(printable_ratio),
        byte_high_ratio=clamp01(high_ratio),
        byte_histogram=bh,
        base64_entropy=b64_entropy,
        base64_entropy_norm=b64_entropy_norm,
        base64_padding_ratio=clamp01(padding_ratio),
        base64_symbol_histogram=b64_hist,
        chunk_entropy_mean=clamp01(mean(chunk_entropies)),
        chunk_entropy_std=clamp01(std(chunk_entropies)),
        chunk_entropy_max_delta=clamp01(max_delta(chunk_entropies)),
        collatz_seed=seed,
        collatz_steps=steps,
        collatz_reduce_count=red,
        collatz_expand_count=exp,
        collatz_final=final,
    )
