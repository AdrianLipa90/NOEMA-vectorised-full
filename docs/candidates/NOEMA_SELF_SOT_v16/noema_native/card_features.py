from __future__ import annotations

"""Deterministic feature frames for native crystal training (v16).

Feature frames are explicit training views over validated cards. They are not
Memory Home records, not CIELingoPhase36, and not NOEMA Vector36.

Two views are separated to avoid reconstruction-target leakage:
- STRUCTURAL: no definition/summary text; safe for routing/trajectory.
- RELATIONAL_SEMANTIC: hashed semantic text may be used for relation learning.

No third-party runtime dependencies.
"""

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from struct import pack
from typing import Iterable
import re

from .cards import KnowledgeCard, CardStatus

_TOKEN_RE = re.compile(r"[A-Za-z0-9_./+-]+")


def _lp(value: str) -> bytes:
    raw = value.encode("utf-8")
    return pack(">I", len(raw)) + raw


class FeatureView(str, Enum):
    STRUCTURAL = "STRUCTURAL"
    RELATIONAL_SEMANTIC = "RELATIONAL_SEMANTIC"


@dataclass(frozen=True)
class SparseLexical64:
    """Signed 64-bin lexical sketch, distinct from every 36D canonical type."""

    values: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.values) != 64:
            raise ValueError("SparseLexical64 requires 64 bins")
        if any(v not in (-1, 0, 1) for v in self.values):
            raise ValueError("lexical bins must be -1/0/+1")

    @classmethod
    def from_text(cls, text: str) -> "SparseLexical64":
        acc = [0] * 64
        for token in sorted(set(t.lower() for t in _TOKEN_RE.findall(text))):
            digest = sha256(token.encode()).digest()
            idx = int.from_bytes(digest[:2], "big") % 64
            sign = 1 if (digest[2] & 1) else -1
            acc[idx] += sign
        return cls(tuple(1 if x > 0 else (-1 if x < 0 else 0) for x in acc))

    @property
    def digest(self) -> str:
        return sha256(
            b"NOEMA-SPARSE-LEXICAL64-v1\0" + bytes(v + 1 for v in self.values)
        ).hexdigest()


@dataclass(frozen=True)
class CardFeatureFrameV1:
    card_id: str
    view: FeatureView
    card_type: str
    claim_status: str
    lane_affinity: tuple[int, ...]
    provenance_family: str
    lexical64: SparseLexical64 | None
    feature_receipt: str

    @property
    def digest(self) -> str:
        material = bytearray(b"NOEMA-CARD-FEATURE-FRAME-v1\0")
        for value in (
            self.card_id,
            self.view.value,
            self.card_type,
            self.claim_status,
            self.provenance_family,
            self.feature_receipt,
        ):
            material.extend(_lp(value))
        material.extend(bytes(self.lane_affinity))
        material.extend(
            bytes.fromhex(self.lexical64.digest) if self.lexical64 else b"\x00" * 32
        )
        return sha256(bytes(material)).hexdigest()


class CardFeatureFrameBuilder:
    VERSION = "card-feature-frame-builder-v1"

    @classmethod
    def build(cls, card: KnowledgeCard, view: FeatureView) -> CardFeatureFrameV1:
        if card.status not in {CardStatus.VALIDATED, CardStatus.PROMOTED}:
            raise ValueError("feature frame requires VALIDATED/PROMOTED card")
        family = card.provenance[0].source_id
        lexical = None
        if view is FeatureView.RELATIONAL_SEMANTIC:
            text = " ".join([
                card.canonical_name,
                card.definition,
                card.summary,
                *card.constraints,
            ])
            lexical = SparseLexical64.from_text(text)
        material = "|".join([
            cls.VERSION,
            card.card_id,
            view.value,
            card.digest,
            family,
            lexical.digest if lexical else "NO_LEXICAL",
        ]).encode()
        receipt = sha256(material).hexdigest()
        return CardFeatureFrameV1(
            card.card_id,
            view,
            card.card_type.value,
            card.claim_status.value,
            card.lane_affinity.values,
            family,
            lexical,
            receipt,
        )

    @classmethod
    def build_many(
        cls, cards: Iterable[KnowledgeCard], view: FeatureView
    ) -> tuple[CardFeatureFrameV1, ...]:
        return tuple(sorted((cls.build(c, view) for c in cards), key=lambda f: f.card_id))


def structural_distance(a: CardFeatureFrameV1, b: CardFeatureFrameV1) -> float:
    if a.view is not FeatureView.STRUCTURAL or b.view is not FeatureView.STRUCTURAL:
        raise ValueError("structural_distance requires STRUCTURAL views")
    lane = sum(abs(x - y) for x, y in zip(a.lane_affinity, b.lane_affinity)) / 24.0
    type_penalty = 0.0 if a.card_type == b.card_type else 1.0
    claim_penalty = 0.0 if a.claim_status == b.claim_status else 0.25
    source_penalty = 0.0 if a.provenance_family == b.provenance_family else 0.5
    return lane + type_penalty + claim_penalty + source_penalty


def relational_distance(a: CardFeatureFrameV1, b: CardFeatureFrameV1) -> float:
    if (
        a.view is not FeatureView.RELATIONAL_SEMANTIC
        or b.view is not FeatureView.RELATIONAL_SEMANTIC
    ):
        raise ValueError("relational_distance requires RELATIONAL_SEMANTIC views")
    av = a.lexical64.values
    bv = b.lexical64.values
    active = sum(1 for x, y in zip(av, bv) if x or y)
    mismatch = sum(1 for x, y in zip(av, bv) if x != y)
    lexical = mismatch / max(1, active)
    structural = (
        sum(abs(x - y) for x, y in zip(a.lane_affinity, b.lane_affinity)) / 24.0
        + (0 if a.card_type == b.card_type else 1.0)
        + (0 if a.provenance_family == b.provenance_family else 0.5)
    )
    return lexical + structural


OBJECTIVE_FEATURE_POLICY = {
    "lane_routing": FeatureView.STRUCTURAL,
    "trajectory": FeatureView.STRUCTURAL,
    "relation": FeatureView.RELATIONAL_SEMANTIC,
    "contradiction": FeatureView.RELATIONAL_SEMANTIC,
    "reconstruction": None,
}
