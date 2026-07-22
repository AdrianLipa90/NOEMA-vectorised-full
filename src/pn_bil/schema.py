from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Literal

Decision = Literal["ALLOW", "WARN", "REVIEW", "QUARANTINE"]


@dataclass(frozen=True)
class CanonicalArtifact:
    path: str
    size_bytes: int
    sha256: str
    base64_sha256: str
    base64_length: int
    sample_base64_prefix: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FeatureSummary:
    byte_entropy: float
    byte_entropy_norm: float
    byte_zero_ratio: float
    byte_printable_ratio: float
    byte_high_ratio: float
    byte_histogram: list[float]
    base64_entropy: float
    base64_entropy_norm: float
    base64_padding_ratio: float
    base64_symbol_histogram: list[float]
    chunk_entropy_mean: float
    chunk_entropy_std: float
    chunk_entropy_max_delta: float
    collatz_seed: int
    collatz_steps: int
    collatz_reduce_count: int
    collatz_expand_count: int
    collatz_final: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PhaseVectorRecord:
    vector: list[float]
    semantic_type: str
    source: str
    operator: str
    route: dict[str, Any]
    metric_state: dict[str, float]
    projection: str
    confidence: float
    canon_status: str
    digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ImmuneProfile:
    label: str
    artifact: dict[str, Any]
    phase_vector: dict[str, Any]
    features: dict[str, Any]
    enrolled_at_utc: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ImmuneDecisionRecord:
    decision: Decision
    score: float
    nearest_label: str | None
    nearest_distance: float | None
    exact_sha256_match: bool
    reasons: list[str] = field(default_factory=list)
    candidate: dict[str, Any] = field(default_factory=dict)
    nearest_profile_digest: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
