"""CIELingo Stage 0 radical cards and EN/JA language-slot entries.

This module is intentionally small and dependency-free. It validates the
Stage 0 data contract without pretending that Japanese draft entries have
native-speaker validation.

Core distinction:
- RadicalCard: global semantic radical / invariant axis.
- LanguageSlotEntry: language-local realization of a slot with local holonomy.
- AlignmentRecord: non-identity correspondence between language entries.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable
import json


VALID_SOURCE_BINDINGS = {
    "SOURCE",
    "ARTIFACT_GROUNDED",
    "PROXY_VERIFIED",
    "HYPOTHESIS",
    "SIMULATION",
    "INTERPRETATION",
    "POETIC_SYMBOLIC",
    "UNKNOWN",
}

VALID_ENTRY_STATUS = {
    "present",
    "candidate",
    "draft",
    "in_blanco_open",
    "in_blanco_stable",
    "in_blanco_validated",
    "needs_native_review",
    "rejected",
}

VALID_ALIGNMENT_TYPES = {
    "exact_formal",
    "near_functional",
    "broad_overlap",
    "idiomatic_equivalent",
    "cultural_analogue",
    "false_friend",
    "untranslatable_residue",
    "slot_correspondence",
}


@dataclass(frozen=True)
class RadicalCard:
    slot_id: int
    radical_id: str
    label: str
    primitive_family: list[str]
    gloss: str
    relation_axes: list[str] = field(default_factory=list)
    runtime_axes: list[str] = field(default_factory=list)
    source_binding: str = "ARTIFACT_GROUNDED"
    validation_status: str = "draft"
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RadicalCard":
        return cls(**data)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not isinstance(self.slot_id, int) or self.slot_id <= 0:
            issues.append("slot_id must be a positive integer")
        if not self.radical_id:
            issues.append("radical_id is required")
        if not self.label:
            issues.append("label is required")
        if not self.primitive_family:
            issues.append("primitive_family must be non-empty")
        if self.source_binding == "SOURCE":
            issues.append("radical cards must not default to SOURCE")
        if self.source_binding not in VALID_SOURCE_BINDINGS:
            issues.append(f"invalid source_binding: {self.source_binding}")
        if not (0.0 <= float(self.confidence) <= 1.0):
            issues.append("confidence must be in [0, 1]")
        return issues


@dataclass(frozen=True)
class LanguageSlotEntry:
    slot_id: int
    language_id: str
    entry_id: str
    lemma: str | None
    surface_forms: list[str]
    pos: str
    status: str
    lexical_register: str = "neutral"
    grammar_profile: dict[str, Any] = field(default_factory=dict)
    j_functionals: dict[str, float] = field(default_factory=dict)
    residue: dict[str, Any] = field(default_factory=dict)
    source_binding: str = "ARTIFACT_GROUNDED"
    validation_status: str = "draft"
    confidence: float = 0.0
    needs_native_review: bool = False
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LanguageSlotEntry":
        return cls(**data)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not isinstance(self.slot_id, int) or self.slot_id <= 0:
            issues.append("slot_id must be a positive integer")
        if self.language_id not in {"en", "ja"}:
            issues.append("this seed supports only en/ja entries")
        if not self.entry_id:
            issues.append("entry_id is required")
        if self.status not in VALID_ENTRY_STATUS:
            issues.append(f"invalid status: {self.status}")
        if self.status.startswith("in_blanco"):
            if self.lemma is not None or self.surface_forms:
                issues.append("in_blanco entry must not force lemma/surface_forms")
        else:
            if not self.lemma:
                issues.append("non-blank entry requires lemma")
            if not self.surface_forms:
                issues.append("non-blank entry requires surface_forms")
        if self.source_binding == "SOURCE":
            issues.append("language slot entries must not default to SOURCE")
        if self.source_binding not in VALID_SOURCE_BINDINGS:
            issues.append(f"invalid source_binding: {self.source_binding}")
        if not (0.0 <= float(self.confidence) <= 1.0):
            issues.append("confidence must be in [0, 1]")
        for key, value in self.j_functionals.items():
            if not (0.0 <= float(value) <= 1.0):
                issues.append(f"j_functional {key} must be in [0, 1]")
        if self.language_id == "ja" and not self.needs_native_review:
            issues.append("Japanese seed entries must explicitly require native review")
        return issues


@dataclass(frozen=True)
class AlignmentRecord:
    alignment_id: str
    slot_id: int
    universal_anchor: str
    members: list[dict[str, Any]]
    alignment_type: str = "slot_correspondence"
    alignment_strength: float = 0.0
    residue_notes: list[str] = field(default_factory=list)
    source_binding: str = "ARTIFACT_GROUNDED"
    validation_status: str = "draft"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AlignmentRecord":
        return cls(**data)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.alignment_id:
            issues.append("alignment_id is required")
        if not isinstance(self.slot_id, int) or self.slot_id <= 0:
            issues.append("slot_id must be a positive integer")
        if not self.universal_anchor:
            issues.append("universal_anchor is required")
        if self.alignment_type not in VALID_ALIGNMENT_TYPES:
            issues.append(f"invalid alignment_type: {self.alignment_type}")
        if not (0.0 <= float(self.alignment_strength) <= 1.0):
            issues.append("alignment_strength must be in [0, 1]")
        if self.source_binding == "SOURCE":
            issues.append("alignment records must not default to SOURCE")
        langs = {m.get("language_id") for m in self.members}
        if not {"en", "ja"}.issubset(langs):
            issues.append("alignment must include en and ja members in this seed")
        for member in self.members:
            if member.get("equivalence_type") == "identity":
                issues.append("alignment member must not claim semantic identity")
        return issues


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    return rows


def load_radicals(path: str | Path) -> list[RadicalCard]:
    return [RadicalCard.from_dict(row) for row in read_jsonl(path)]


def load_language_entries(path: str | Path) -> list[LanguageSlotEntry]:
    return [LanguageSlotEntry.from_dict(row) for row in read_jsonl(path)]


def load_alignments(path: str | Path) -> list[AlignmentRecord]:
    return [AlignmentRecord.from_dict(row) for row in read_jsonl(path)]


def validate_all(
    radical_path: str | Path,
    en_path: str | Path,
    ja_path: str | Path,
    alignment_path: str | Path,
) -> dict[str, Any]:
    radicals = load_radicals(radical_path)
    en_entries = load_language_entries(en_path)
    ja_entries = load_language_entries(ja_path)
    alignments = load_alignments(alignment_path)

    issues: list[dict[str, Any]] = []
    for collection_name, objects in [
        ("radicals", radicals),
        ("en_entries", en_entries),
        ("ja_entries", ja_entries),
        ("alignments", alignments),
    ]:
        for obj in objects:
            for issue in obj.validate():
                issues.append({
                    "collection": collection_name,
                    "id": getattr(obj, "radical_id", getattr(obj, "entry_id", getattr(obj, "alignment_id", "?"))),
                    "issue": issue,
                })

    radical_slots = {r.slot_id for r in radicals}
    en_slots = {e.slot_id for e in en_entries}
    ja_slots = {e.slot_id for e in ja_entries}
    alignment_slots = {a.slot_id for a in alignments}

    for slot_id in sorted((en_slots | ja_slots | alignment_slots) - radical_slots):
        issues.append({"collection": "cross_reference", "id": slot_id, "issue": "slot missing from radicals"})
    for slot_id in sorted(radical_slots - en_slots):
        issues.append({"collection": "en_entries", "id": slot_id, "issue": "missing English entry"})
    for slot_id in sorted(radical_slots - ja_slots):
        issues.append({"collection": "ja_entries", "id": slot_id, "issue": "missing Japanese entry"})
    for slot_id in sorted(radical_slots - alignment_slots):
        issues.append({"collection": "alignments", "id": slot_id, "issue": "missing alignment record"})

    return {
        "ok": not issues,
        "counts": {
            "radicals": len(radicals),
            "en_entries": len(en_entries),
            "ja_entries": len(ja_entries),
            "alignments": len(alignments),
        },
        "issues": issues,
    }
