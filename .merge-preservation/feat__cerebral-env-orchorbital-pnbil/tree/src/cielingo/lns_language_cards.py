"""NOEMA/LNS-backed language-card loader for CIELingo.

This module treats the embedded ``ciel_lingophysics_lns_repo_v2_3`` data as the
local NOEMA language-card surface.  It does not import external dictionaries and
it does not promote draft seed cards to canon.  It only exposes deterministic
inventory/search structures that runtime modules can consume.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

DEFAULT_LNS_REL = Path("src/ciel_lingophysics_lns_repo_v2_3/data")


@dataclass(frozen=True)
class LNSLanguageCard:
    """Normalized CIELingo language card.

    ``card_kind`` is deliberately coarse: concept/operator/noema.  The original
    schema/source path remains attached so later validators can apply stricter
    constraints without losing provenance.
    """

    card_id: str
    card_kind: str
    canonical_label: str
    source_path: str
    languages: dict[str, list[str]]
    semantic_axes: tuple[str, ...]
    semantic_mass: float
    phase_rad: float
    operator_hooks: tuple[str, ...]
    status: str
    source_policy: str
    noema_tags: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["semantic_axes"] = list(self.semantic_axes)
        out["operator_hooks"] = list(self.operator_hooks)
        out["noema_tags"] = list(self.noema_tags)
        return out


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _repo_root(path: str | Path = ".") -> Path:
    p = Path(path).resolve()
    if p == Path(".").resolve():
        return Path(__file__).resolve().parents[2]
    return p


def _data_root(repo_root: str | Path = ".") -> Path:
    root = _repo_root(repo_root)
    direct = root / DEFAULT_LNS_REL
    if direct.exists():
        return direct
    # Support running from source-package or tests.
    alt = Path(__file__).resolve().parents[2] / DEFAULT_LNS_REL
    return alt if alt.exists() else direct


def _labels_from_concept(card: dict[str, Any]) -> dict[str, list[str]]:
    labels: dict[str, list[str]] = {}
    for lang, payload in card.get("languages", {}).items():
        vals: list[str] = []
        lemma = payload.get("lemma")
        if lemma:
            vals.append(str(lemma))
        vals.extend(str(x) for x in payload.get("forms_seed", []) if x)
        vals.extend(str(x) for x in payload.get("near_synonyms_seed", []) if x)
        # preserve order and remove duplicates
        labels[lang] = list(dict.fromkeys(vals))
    return labels


def _labels_from_operator(card: dict[str, Any]) -> dict[str, list[str]]:
    surfaces = card.get("surfaces", {})
    labels: dict[str, list[str]] = {}
    for lang, payload in surfaces.items():
        vals: list[str] = []
        if isinstance(payload, dict):
            lemma = payload.get("lemma")
            if lemma:
                vals.append(str(lemma))
            vals.extend(str(x) for x in payload.get("forms", []) if x)
        elif isinstance(payload, list):
            vals.extend(str(x) for x in payload if x)
        elif isinstance(payload, str):
            vals.append(payload)
        labels[lang] = list(dict.fromkeys(vals))
    return labels



def _source_path_str(path: Path, repo_root: str | Path = ".") -> str:
    if not path.is_absolute():
        return str(path)
    try:
        return str(path.relative_to(_repo_root(repo_root)))
    except ValueError:
        return str(path)


def _phase_from_id(card_id: str) -> float:
    # Deterministic fallback phase in [0, 2π).  Used only when source card does
    # not carry an explicit phase seed.
    import math

    val = int(hashlib.sha256(card_id.encode("utf-8")).hexdigest()[:16], 16)
    return (val / float(16**16 - 1)) * (2.0 * math.pi)


def load_lns_concept_cards(repo_root: str | Path = ".") -> list[LNSLanguageCard]:
    data_root = _data_root(repo_root)
    base = data_root / "concept_cards"
    cards: list[LNSLanguageCard] = []
    for path in sorted(base.glob("batch*/*.json")):
        if path.name.startswith("batch"):
            continue
        payload = _read_json(path)
        cid = str(payload.get("concept_id", path.stem))
        source_rel = _source_path_str(path, repo_root)
        cards.append(
            LNSLanguageCard(
                card_id=cid,
                card_kind="concept",
                canonical_label=str(payload.get("canonical_label_en", path.stem)),
                source_path=source_rel,
                languages=_labels_from_concept(payload),
                semantic_axes=tuple(str(x) for x in payload.get("semantic_axes", [])),
                semantic_mass=float(payload.get("semantic_mass_seed", 0.0)),
                phase_rad=float(payload.get("phase_seed_rad", _phase_from_id(cid))),
                operator_hooks=tuple(str(x) for x in payload.get("operator_hooks", [])),
                status=str(payload.get("epistemic_status", "unknown")),
                source_policy=str(payload.get("source_policy", "unknown")),
                noema_tags=("cielingo", "lns", "language_card", "concept"),
            )
        )
    return cards


def load_lns_operator_cards(repo_root: str | Path = ".") -> list[LNSLanguageCard]:
    data_root = _data_root(repo_root)
    cards: list[LNSLanguageCard] = []
    core_path = data_root / "operator_cards" / "core_operators_5lang.json"
    if core_path.exists():
        payload = _read_json(core_path)
        for item in payload.get("operator_cards", []):
            cid = str(item.get("id", item.get("operator_id", "operator:unknown")))
            classes = item.get("class", [])
            if isinstance(classes, str):
                axes = (classes,)
            else:
                axes = tuple(str(x) for x in classes)
            cards.append(
                LNSLanguageCard(
                    card_id=cid,
                    card_kind="operator",
                    canonical_label=str(item.get("family", item.get("symbol", cid))),
                    source_path=_source_path_str(core_path, repo_root),
                    languages=_labels_from_operator(item),
                    semantic_axes=axes,
                    semantic_mass=1.0,
                    phase_rad=_phase_from_id(cid),
                    operator_hooks=(str(item.get("family", cid)),),
                    status="operator_seed",
                    source_policy=str(payload.get("license_note", "hand_curated_seed")),
                    noema_tags=("cielingo", "lns", "language_card", "operator", "core"),
                )
            )

    dyn_path = data_root / "operator_cards" / "dynamic_deictic_operators_5lang.json"
    if dyn_path.exists():
        payload = _read_json(dyn_path)
        for item in payload.get("cards", []):
            cid = str(item.get("operator_id", item.get("id", "operator:dynamic:unknown")))
            cards.append(
                LNSLanguageCard(
                    card_id=cid,
                    card_kind="operator",
                    canonical_label=str(item.get("canonical_operator", cid)),
                    source_path=_source_path_str(dyn_path, repo_root),
                    languages=_labels_from_operator(item),
                    semantic_axes=(str(item.get("semantic_axis", "dynamic_deictic")),),
                    semantic_mass=1.0,
                    phase_rad=float(item.get("phase", _phase_from_id(cid))),
                    operator_hooks=(str(item.get("canonical_operator", cid)),),
                    status="dynamic_deictic_seed",
                    source_policy="hand_curated_seed_no_external_dictionary_import",
                    noema_tags=("cielingo", "lns", "language_card", "operator", "dynamic_deictic"),
                )
            )
    return cards


def load_noema_index_language_cards(repo_root: str | Path = ".") -> list[LNSLanguageCard]:
    data_root = _data_root(repo_root)
    path = data_root / "noema" / "noema_index_seed_v2_2.json"
    if not path.exists():
        return []
    payload = _read_json(path)
    cards: list[LNSLanguageCard] = []
    for item in payload.get("cards", []):
        cid = str(item.get("id", item.get("canonical_ref", "noema:unknown")))
        labels = {
            str(lang): [str(v) for v in vals]
            for lang, vals in item.get("labels", {}).items()
            if isinstance(vals, list)
        }
        cards.append(
            LNSLanguageCard(
                card_id=cid,
                card_kind="noema",
                canonical_label=str(item.get("canonical_ref", cid)),
                source_path=_source_path_str(path, repo_root),
                languages=labels,
                semantic_axes=tuple(str(x) for x in item.get("domains", [])),
                semantic_mass=float(item.get("confidence", 0.0)),
                phase_rad=_phase_from_id(cid),
                operator_hooks=tuple(str(x) for x in item.get("operator_hooks", [])),
                status=str(item.get("status", payload.get("status", "draft_seed"))),
                source_policy="noema_index_seed_no_external_dictionary_import",
                noema_tags=("cielingo", "noema", "language_card", str(item.get("card_type", "unknown")).lower()),
            )
        )
    return cards


def load_all_language_cards(repo_root: str | Path = ".") -> list[LNSLanguageCard]:
    cards = [
        *load_lns_concept_cards(repo_root),
        *load_lns_operator_cards(repo_root),
        *load_noema_index_language_cards(repo_root),
    ]
    # Stable de-duplication by (card_id, source_path) while preserving source diversity.
    seen: set[tuple[str, str]] = set()
    out: list[LNSLanguageCard] = []
    for card in cards:
        key = (card.card_id, card.source_path)
        if key not in seen:
            seen.add(key)
            out.append(card)
    return out


def language_card_inventory(repo_root: str | Path = ".") -> dict[str, Any]:
    cards = load_all_language_cards(repo_root)
    by_kind: dict[str, int] = {}
    languages: dict[str, int] = {}
    for card in cards:
        by_kind[card.card_kind] = by_kind.get(card.card_kind, 0) + 1
        for lang in card.languages:
            languages[lang] = languages.get(lang, 0) + 1
    return {
        "schema": "cielingo/noema-language-card-inventory/v0.1",
        "source_role": "local_noema_lns_surface",
        "epistemic_status": "draft seed inventory; no external dictionary import; no USER007 SoT writeback claimed",
        "total_cards": len(cards),
        "by_kind": dict(sorted(by_kind.items())),
        "languages": dict(sorted(languages.items())),
        "cards": [c.as_dict() for c in cards],
    }


def search_language_cards(query: str, repo_root: str | Path = ".", *, limit: int = 20) -> list[dict[str, Any]]:
    terms = [t.lower() for t in query.split() if t.strip()]
    hits: list[tuple[float, LNSLanguageCard, list[str]]] = []
    for card in load_all_language_cards(repo_root):
        haystack_parts = [card.card_id, card.card_kind, card.canonical_label, *card.semantic_axes, *card.operator_hooks]
        for vals in card.languages.values():
            haystack_parts.extend(vals)
        haystack = " ".join(str(x).lower() for x in haystack_parts)
        matched = [term for term in terms if term in haystack]
        if matched:
            score = len(set(matched)) + 0.1 * card.semantic_mass + 0.01 * len(card.operator_hooks)
            hits.append((score, card, sorted(set(matched))))
    hits.sort(key=lambda row: (-row[0], row[1].card_id))
    return [
        {"score": round(score, 6), "matched_terms": matched, **card.as_dict()}
        for score, card, matched in hits[:limit]
    ]


__all__ = [
    "LNSLanguageCard",
    "load_lns_concept_cards",
    "load_lns_operator_cards",
    "load_noema_index_language_cards",
    "load_all_language_cards",
    "language_card_inventory",
    "search_language_cards",
]
