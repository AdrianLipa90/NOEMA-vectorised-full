"""Associator diagnostics for the NOEMA PhaseNav Gate Fabric.

The generic associator measures whether a declared composition law depends on
parenthesization:

    A(x,y,z) = d(compose(compose(x,y),z), compose(x,compose(y,z)))

No claim is made that every PhaseNav operation is non-associative.  The first
concrete diagnostic here targets *lossy pairwise phase compression*, where
forgetting multiplicity can make grouping order materially change the result.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Generic, Sequence, TypeVar

from .pnv_precise import N, PI, angular_distance

T = TypeVar("T")


@dataclass(frozen=True)
class AssociatorMeasurement(Generic[T]):
    kind: str
    defect: float
    left: T
    right: T
    metric: str
    provenance: tuple[str, ...] = ()


def associator_defect(
    x: T,
    y: T,
    z: T,
    *,
    compose: Callable[[T, T], T],
    distance: Callable[[T, T], float],
    normalize_by: float = 1.0,
    kind: str = "RELATIONAL_ASSOCIATOR",
    metric: str = "declared_distance",
    provenance: Sequence[str] = (),
) -> AssociatorMeasurement[T]:
    """Measure parenthesization sensitivity for an explicitly supplied algebra."""

    if normalize_by <= 0.0 or not math.isfinite(normalize_by):
        raise ValueError("normalize_by must be a positive finite number")
    left = compose(compose(x, y), z)
    right = compose(x, compose(y, z))
    raw = float(distance(left, right))
    if raw < 0.0 or not math.isfinite(raw):
        raise ValueError("distance must return a finite non-negative value")
    defect = max(0.0, min(1.0, raw / normalize_by))
    return AssociatorMeasurement(
        kind=kind,
        defect=defect,
        left=left,
        right=right,
        metric=metric,
        provenance=tuple(str(item) for item in provenance),
    )


def _validate_phase36(values: Sequence[float]) -> tuple[float, ...]:
    result = tuple(float(value) % (2.0 * PI) for value in values)
    if len(result) != N:
        raise ValueError(f"expected {N} phase values; got {len(result)}")
    return result


def pairwise_circular_compress(a: Sequence[float], b: Sequence[float]) -> tuple[float, ...]:
    """Lossy equal-weight pair compression of two 36D phase states.

    The operation deliberately does not retain source multiplicity. It is
    useful as an associator probe for compression pipelines that repeatedly
    fold pairs into a single representative phase vector.
    """

    aa = _validate_phase36(a)
    bb = _validate_phase36(b)
    out: list[float] = []
    for x, y in zip(aa, bb):
        sx = math.sin(x) + math.sin(y)
        cx = math.cos(x) + math.cos(y)
        if abs(sx) <= 1e-15 and abs(cx) <= 1e-15:
            # Antipodal pair has no unique circular mean. Preserve a
            # deterministic midpoint but mark ambiguity via higher-level
            # evidence if this primitive is used operationally.
            out.append(((x + ((y - x + PI) % (2.0 * PI) - PI) / 2.0) % (2.0 * PI)))
        else:
            out.append(math.atan2(sx, cx) % (2.0 * PI))
    return tuple(out)


def compression_associator(
    a: Sequence[float],
    b: Sequence[float],
    c: Sequence[float],
    *,
    provenance: Sequence[str] = (),
) -> AssociatorMeasurement[tuple[float, ...]]:
    """Associator of lossy pairwise circular phase compression.

    `angular_distance` is RMS circular distance in radians; division by π
    normalizes the defect to [0,1].
    """

    aa = _validate_phase36(a)
    bb = _validate_phase36(b)
    cc = _validate_phase36(c)
    return associator_defect(
        aa,
        bb,
        cc,
        compose=pairwise_circular_compress,
        distance=angular_distance,
        normalize_by=PI,
        kind="PHASE_COMPRESSION_ASSOCIATOR",
        metric="rms_angular_distance_over_pi",
        provenance=provenance,
    )


__all__ = [
    "AssociatorMeasurement",
    "associator_defect",
    "pairwise_circular_compress",
    "compression_associator",
]
