"""CIELingo lexical holonomy surface.

This module establishes relations *between words*, not just vectors for cards.
It uses the local NOEMA/LNS language-card files as the primary surface and
keeps all external/open-source lexical resources as provenance descriptors until
an explicit verified dump/API import is provided.

Implemented relation layers:

* card-internal seed relations: near synonyms, antonyms, forms, examples
* batch relation CSV edges: supports/opposes/contains/etc. between concepts
* cross-card semantic proximity: shared axes, phase distance, vector distance
* per-word knowledge notes: confidence, provenance, verification state, review
  needs and recommended open-source sources
* guarded file access: the runtime can list/read its own language-card files
  under ``src/ciel_lingophysics_lns_repo_v2_3/data`` only.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping

from .lns_language_cards import DEFAULT_LNS_REL, LNSLanguageCard, load_all_language_cards

LEXICAL_HOLONOMY_SCHEMA = "cielingo/lexical-holonomy/v0.1"
OWN_CARD_ACCESS_SCHEMA = "cielingo/language-card-file-access/v0.1"
KNOWLEDGE_NOTE_SCHEMA = "cielingo/word-knowledge-note/v0.1"

# Descriptors only.  They are not treated as verified evidence unless a local
# dump/API proof is imported and attached to a word note.
OPEN_SOURCE_LEXICAL_SOURCES: tuple[dict[str, str], ...] = (
    {
        "source_id": "wiktionary_dump",
        "name": "Wiktionary dump",
        "role": "definitions, inflection tables, related terms, translations, usage examples",
        "license_hint": "Wikimedia free-content licensing; verify dump license at ingest time",
        "verification_status": "descriptor_only_not_imported",
    },
    {
        "source_id": "plwordnet_slowosiec",
        "name": "plWordNet / Słowosieć",
        "role": "Polish synsets and lexical-semantic relations",
        "license_hint": "verify concrete release license before redistribution/use",
        "verification_status": "descriptor_only_not_imported",
    },
    {
        "source_id": "sgjp_morfeusz",
        "name": "SGJP/Morfeusz-style Polish morphology source",
        "role": "lemma, inflection and morphosyntactic validation",
        "license_hint": "verify concrete package/dictionary license before ingest",
        "verification_status": "descriptor_only_not_imported",
    },
)

RELATION_WEIGHTS: Mapping[str, float] = {
    "synonym": 1.0,
    "near_synonym": 0.86,
    "bliskoznaczne": 0.86,
    "antonym": -0.92,
    "opposes": -0.88,
    "divergent": -0.62,
    "convergent": 0.64,
    "same_card_form": 0.78,
    "form_variant": 0.70,
    "same_axis": 0.54,
    "supports": 0.48,
    "requires": 0.44,
    "contains": 0.38,
    "inside": 0.36,
    "part_of": 0.34,
    "uses": 0.32,
    "expresses": 0.32,
    "symbol_of": 0.30,
    "relates_to": 0.25,
    "unknown_relation": 0.12,
}


@dataclass(frozen=True)
class LexicalUnit:
    """One surface word/form extracted from a language-card file."""

    lexical_id: str
    language: str
    surface: str
    lemma: str
    role: str
    card_id: str
    card_kind: str
    canonical_label: str
    source_path: str
    source_field: str
    semantic_axes: tuple[str, ...]
    semantic_mass: float
    phase_rad: float
    source_policy: str
    status: str

    def as_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["semantic_axes"] = list(self.semantic_axes)
        return out


@dataclass(frozen=True)
class LexicalHolonomyEdge:
    """Directed lexical relation with signed semantic weight."""

    source_lexical_id: str
    target_lexical_id: str
    source_surface: str
    target_surface: str
    language: str
    relation_type: str
    relation_family: str
    weight: float
    holonomy_phase_delta: float
    vector_distance: float | None
    evidence_kind: str
    evidence_path: str
    evidence_status: str
    supervision_required: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WordKnowledgeNote:
    """Per-word epistemic note for grammar/lexical supervision."""

    schema: str
    lexical_id: str
    surface: str
    lemma: str
    language: str
    card_id: str
    source_path: str
    source_policy: str
    local_evidence_count: int
    relation_count: int
    synonym_count: int
    antonym_count: int
    convergence_count: int
    divergence_count: int
    knowledge_confidence: float
    confidence_note: str
    verification_state: str
    open_source_sources_to_check: list[dict[str, str]]
    grammar_review_status: str
    correction_policy: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LanguageCardFileRef:
    """Guarded reference to one accessible language-card/source file."""

    schema: str
    path: str
    size_bytes: int
    sha256: str
    suffix: str
    role: str
    access_policy: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _repo_root(repo_root: str | Path = ".") -> Path:
    return Path(repo_root).resolve()


def _data_root(repo_root: str | Path = ".") -> Path:
    return _repo_root(repo_root) / DEFAULT_LNS_REL


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _norm_surface(text: str) -> str:
    return " ".join(str(text).strip().lower().split())


def _lexical_id(language: str, surface: str, card_id: str, source_field: str) -> str:
    payload = f"{language}|{_norm_surface(surface)}|{card_id}|{source_field}"
    return "lex:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _angle_delta(a: float, b: float) -> float:
    return abs(math.atan2(math.sin(a - b), math.cos(a - b)))


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _family(relation_type: str) -> str:
    r = relation_type.lower()
    if r in {"synonym", "near_synonym", "bliskoznaczne", "same_card_form", "form_variant"}:
        return "equivalence_or_similarity"
    if r in {"antonym", "opposes", "divergent"}:
        return "opposition_or_divergence"
    if r in {"convergent", "same_axis", "supports", "requires", "contains", "inside", "part_of", "uses", "expresses", "symbol_of", "relates_to"}:
        return "semantic_convergence"
    return "other_semantic_relation"


def _relation_weight(relation_type: str) -> float:
    return float(RELATION_WEIGHTS.get(relation_type.lower(), RELATION_WEIGHTS["unknown_relation"]))


def list_language_card_files(repo_root: str | Path = ".") -> list[LanguageCardFileRef]:
    """List files the CIELingo model may read for supervised grammar repair.

    Access is intentionally limited to the local LNS/NOEMA language-card data
    root.  This gives the model access to its own cards without granting a broad
    arbitrary filesystem reader.
    """
    root = _repo_root(repo_root)
    data_root = _data_root(root)
    refs: list[LanguageCardFileRef] = []
    allowed_suffixes = {".json", ".yaml", ".yml", ".csv", ".md", ".txt"}
    if not data_root.exists():
        return refs
    for path in sorted(p for p in data_root.rglob("*") if p.is_file() and p.suffix.lower() in allowed_suffixes):
        rel = path.relative_to(root)
        role = "language_card_source"
        if "concept_cards" in path.parts:
            role = "concept_card_source"
        elif "operator_cards" in path.parts:
            role = "operator_card_source"
        elif "noema" in path.parts:
            role = "noema_language_index"
        refs.append(
            LanguageCardFileRef(
                schema=OWN_CARD_ACCESS_SCHEMA,
                path=str(rel),
                size_bytes=path.stat().st_size,
                sha256=_sha256(path),
                suffix=path.suffix.lower(),
                role=role,
                access_policy="read_only_under_lns_data_root",
            )
        )
    return refs


def read_language_card_file(path: str | Path, repo_root: str | Path = ".", *, max_bytes: int = 256_000) -> str:
    """Read one own language-card file through a guarded path check."""
    root = _repo_root(repo_root)
    data_root = _data_root(root).resolve()
    target = (root / path).resolve()
    if data_root not in target.parents and target != data_root:
        raise ValueError(f"refusing to read outside CIELingo LNS data root: {path}")
    if not target.is_file():
        raise FileNotFoundError(str(path))
    if target.stat().st_size > max_bytes:
        raise ValueError(f"file too large for supervised card read: {path}")
    return target.read_text(encoding="utf-8", errors="replace")


def _concept_payload_by_card(repo_root: str | Path = ".") -> dict[str, tuple[Path, dict[str, Any]]]:
    root = _repo_root(repo_root)
    data_root = _data_root(root)
    out: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(data_root.glob("concept_cards/batch*/*.json")):
        if path.name.startswith("batch"):
            continue
        payload = _read_json(path)
        cid = str(payload.get("concept_id", path.stem))
        out[cid] = (path, payload)
    return out


def extract_lexical_units(repo_root: str | Path = ".") -> list[LexicalUnit]:
    """Extract lemmas, forms, near-synonyms and antonyms from card files."""
    cards = {(c.card_id, c.source_path): c for c in load_all_language_cards(repo_root)}
    root = _repo_root(repo_root)
    units: list[LexicalUnit] = []

    for card in cards.values():
        # LNSLanguageCard already normalizes labels but does not preserve the
        # source field.  Re-open concept cards when possible to keep that field.
        path = root / card.source_path
        if path.exists() and path.suffix == ".json" and "concept_cards" in path.parts:
            payload = _read_json(path)
            for language, lang_payload in payload.get("languages", {}).items():
                if not isinstance(lang_payload, dict):
                    continue
                field_map = {
                    "lemma": [lang_payload.get("lemma")],
                    "form_variant": lang_payload.get("forms_seed", []),
                    "near_synonym": lang_payload.get("near_synonyms_seed", []),
                    "antonym": lang_payload.get("antonyms_seed", []),
                }
                lemma = str(lang_payload.get("lemma") or card.canonical_label)
                for field, values in field_map.items():
                    for value in values or []:
                        surface = str(value).strip()
                        if not surface:
                            continue
                        units.append(
                            LexicalUnit(
                                lexical_id=_lexical_id(language, surface, card.card_id, field),
                                language=str(language),
                                surface=surface,
                                lemma=lemma,
                                role=field,
                                card_id=card.card_id,
                                card_kind=card.card_kind,
                                canonical_label=card.canonical_label,
                                source_path=card.source_path,
                                source_field=field,
                                semantic_axes=card.semantic_axes,
                                semantic_mass=card.semantic_mass,
                                phase_rad=card.phase_rad,
                                source_policy=card.source_policy,
                                status=card.status,
                            )
                        )
        else:
            # Operators/NOEMA index: use normalized labels as form candidates.
            for language, labels in card.languages.items():
                lemma = labels[0] if labels else card.canonical_label
                for i, surface in enumerate(labels):
                    field = "lemma" if i == 0 else "form_variant"
                    units.append(
                        LexicalUnit(
                            lexical_id=_lexical_id(language, surface, card.card_id, field),
                            language=str(language),
                            surface=str(surface),
                            lemma=str(lemma),
                            role=field,
                            card_id=card.card_id,
                            card_kind=card.card_kind,
                            canonical_label=card.canonical_label,
                            source_path=card.source_path,
                            source_field=field,
                            semantic_axes=card.semantic_axes,
                            semantic_mass=card.semantic_mass,
                            phase_rad=card.phase_rad,
                            source_policy=card.source_policy,
                            status=card.status,
                        )
                    )

    # Stable de-duplication by lexical_id.
    by_id: dict[str, LexicalUnit] = {}
    for unit in units:
        by_id.setdefault(unit.lexical_id, unit)
    return sorted(by_id.values(), key=lambda u: (u.language, u.card_id, u.role, u.surface))


def _index_units(units: Iterable[LexicalUnit]) -> tuple[dict[str, list[LexicalUnit]], dict[tuple[str, str], list[LexicalUnit]]]:
    by_card_lang: dict[str, list[LexicalUnit]] = {}
    by_surface_lang: dict[tuple[str, str], list[LexicalUnit]] = {}
    for unit in units:
        by_card_lang.setdefault(f"{unit.card_id}|{unit.language}", []).append(unit)
        by_surface_lang.setdefault((unit.language, _norm_surface(unit.surface)), []).append(unit)
    return by_card_lang, by_surface_lang


def _edge(
    src: LexicalUnit,
    dst: LexicalUnit,
    relation_type: str,
    *,
    evidence_kind: str,
    evidence_path: str,
    evidence_status: str,
    vector_distance: float | None = None,
) -> LexicalHolonomyEdge:
    weight = _relation_weight(relation_type)
    return LexicalHolonomyEdge(
        source_lexical_id=src.lexical_id,
        target_lexical_id=dst.lexical_id,
        source_surface=src.surface,
        target_surface=dst.surface,
        language=src.language,
        relation_type=relation_type,
        relation_family=_family(relation_type),
        weight=round(weight, 6),
        holonomy_phase_delta=round(_angle_delta(src.phase_rad, dst.phase_rad), 9),
        vector_distance=None if vector_distance is None else round(float(vector_distance), 9),
        evidence_kind=evidence_kind,
        evidence_path=evidence_path,
        evidence_status=evidence_status,
        supervision_required=evidence_status != "externally_verified",
    )


def _vector_distance(a: LexicalUnit, b: LexicalUnit, repo_root: str | Path = ".") -> float:
    """Cheap local lexical distance compatible with the 24D vector surface.

    The full 24D vectorizer is intentionally not called here: relation graph
    construction is O(n^2), so repeated phase-bus vectorization would turn the
    lexical holonomy pass into the bottleneck.  This proxy uses the dimensions
    that are already present on lexical units: mass, phase and axis overlap.
    """
    mass_delta = abs(float(a.semantic_mass) - float(b.semantic_mass))
    phase_delta_norm = _angle_delta(a.phase_rad, b.phase_rad) / math.pi
    axes_a, axes_b = set(a.semantic_axes), set(b.semantic_axes)
    if axes_a or axes_b:
        axis_distance = 1.0 - (len(axes_a & axes_b) / max(1, len(axes_a | axes_b)))
    else:
        axis_distance = 1.0
    return _bounded((mass_delta + phase_delta_norm + axis_distance) / 3.0)


def build_lexical_holonomy_edges(repo_root: str | Path = ".", *, max_cross_edges: int = 512) -> list[LexicalHolonomyEdge]:
    """Build lexical holonomy edges from cards, relation files and vector proximity."""
    root = _repo_root(repo_root)
    units = extract_lexical_units(root)
    by_card_lang, by_surface_lang = _index_units(units)
    edges: list[LexicalHolonomyEdge] = []

    # Card-internal relations: lemma -> forms/synonyms/antonyms.
    for key, local_units in by_card_lang.items():
        lemmas = [u for u in local_units if u.role == "lemma"] or local_units[:1]
        for lemma in lemmas:
            for unit in local_units:
                if lemma.lexical_id == unit.lexical_id:
                    continue
                if unit.role == "near_synonym":
                    relation = "near_synonym"
                elif unit.role == "antonym":
                    relation = "antonym"
                elif unit.role == "form_variant":
                    relation = "form_variant"
                else:
                    relation = "same_card_form"
                edges.append(
                    _edge(
                        lemma,
                        unit,
                        relation,
                        evidence_kind="language_card_seed_field",
                        evidence_path=unit.source_path,
                        evidence_status="local_seed_needs_external_verification",
                    )
                )
                # Make synonyms/forms bidirectional; antonyms are also symmetric.
                edges.append(
                    _edge(
                        unit,
                        lemma,
                        relation,
                        evidence_kind="language_card_seed_field",
                        evidence_path=unit.source_path,
                        evidence_status="local_seed_needs_external_verification",
                    )
                )

    # Batch CSV concept relations, projected onto lemmas of each language.
    data_root = _data_root(root)
    card_lang_lemmas: dict[tuple[str, str], list[LexicalUnit]] = {}
    for unit in units:
        if unit.role == "lemma":
            card_lang_lemmas.setdefault((unit.card_id, unit.language), []).append(unit)
    for rel_path in sorted(data_root.glob("concept_cards/batch*/*relations*.csv")):
        with rel_path.open("r", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                source = row.get("source") or ""
                target = row.get("target") or ""
                relation = row.get("relation_type") or "relates_to"
                status = row.get("status") or "draft_seed"
                languages = {lang for cid, lang in card_lang_lemmas if cid in {source, target}}
                for lang in languages:
                    for src in card_lang_lemmas.get((source, lang), []):
                        for dst in card_lang_lemmas.get((target, lang), []):
                            edges.append(
                                _edge(
                                    src,
                                    dst,
                                    relation,
                                    evidence_kind="batch_relation_csv",
                                    evidence_path=str(rel_path.relative_to(root)),
                                    evidence_status=status,
                                )
                            )

    # Cross-card semantic convergence/divergence from axes and phase/vector distance.
    lemma_units = [u for u in units if u.role == "lemma"]
    cross_count = 0
    for i, a in enumerate(lemma_units):
        for b in lemma_units[i + 1 :]:
            if cross_count >= max_cross_edges:
                break
            if a.language != b.language or a.card_id == b.card_id:
                continue
            shared_axes = set(a.semantic_axes).intersection(b.semantic_axes)
            phase_delta = _angle_delta(a.phase_rad, b.phase_rad)
            if shared_axes and phase_delta <= 1.25:
                dist = _vector_distance(a, b, root)
                rel = "convergent" if dist <= 0.38 else "same_axis"
            elif phase_delta >= 2.55 and not shared_axes:
                dist = _vector_distance(a, b, root)
                rel = "divergent" if dist >= 0.25 else "relates_to"
            else:
                continue
            for src, dst in ((a, b), (b, a)):
                edges.append(
                    _edge(
                        src,
                        dst,
                        rel,
                        evidence_kind="derived_phase_vector_axis_relation",
                        evidence_path="NOEMA/LNS local vector surface",
                        evidence_status="derived_needs_human_validation",
                        vector_distance=dist,
                    )
                )
            cross_count += 2
        if cross_count >= max_cross_edges:
            break

    # Remove exact duplicates, keep stable order.
    seen: set[tuple[str, str, str, str]] = set()
    dedup: list[LexicalHolonomyEdge] = []
    for edge in edges:
        key = (edge.source_lexical_id, edge.target_lexical_id, edge.relation_type, edge.evidence_path)
        if key not in seen:
            seen.add(key)
            dedup.append(edge)
    return sorted(dedup, key=lambda e: (e.language, e.source_surface, e.relation_type, e.target_surface, e.evidence_path))


def build_word_knowledge_notes(repo_root: str | Path = ".") -> list[WordKnowledgeNote]:
    """Build one epistemic note per lexical unit."""
    units = extract_lexical_units(repo_root)
    edges = build_lexical_holonomy_edges(repo_root)
    edge_by_src: dict[str, list[LexicalHolonomyEdge]] = {}
    edge_by_tgt: dict[str, list[LexicalHolonomyEdge]] = {}
    for e in edges:
        edge_by_src.setdefault(e.source_lexical_id, []).append(e)
        edge_by_tgt.setdefault(e.target_lexical_id, []).append(e)

    notes: list[WordKnowledgeNote] = []
    for unit in units:
        related = edge_by_src.get(unit.lexical_id, []) + edge_by_tgt.get(unit.lexical_id, [])
        rel_count = len(related)
        synonym_count = sum(1 for e in related if e.relation_type in {"synonym", "near_synonym", "form_variant", "same_card_form"})
        antonym_count = sum(1 for e in related if e.relation_type in {"antonym", "opposes"})
        convergence_count = sum(1 for e in related if e.weight > 0.0)
        divergence_count = sum(1 for e in related if e.weight < 0.0)
        local_evidence_count = 1 + rel_count
        base = 0.22
        if unit.role == "lemma":
            base += 0.16
        if unit.status not in {"unknown", "draft_unknown"}:
            base += 0.08
        base += min(0.24, 0.02 * rel_count)
        if "no_external_dictionary_import" in unit.source_policy or "seed" in unit.status:
            verification_state = "local_seed_unverified_externally"
            confidence_note = "Known from local CIELingo/NOEMA card seed; external lexical verification still required."
            grammar_review_status = "needs_supervised_review"
        else:
            verification_state = "local_source_policy_known"
            confidence_note = "Known from local card source; check source policy before canonical promotion."
            grammar_review_status = "review_recommended"
        confidence = _bounded(base)
        notes.append(
            WordKnowledgeNote(
                schema=KNOWLEDGE_NOTE_SCHEMA,
                lexical_id=unit.lexical_id,
                surface=unit.surface,
                lemma=unit.lemma,
                language=unit.language,
                card_id=unit.card_id,
                source_path=unit.source_path,
                source_policy=unit.source_policy,
                local_evidence_count=local_evidence_count,
                relation_count=rel_count,
                synonym_count=synonym_count,
                antonym_count=antonym_count,
                convergence_count=convergence_count,
                divergence_count=divergence_count,
                knowledge_confidence=round(confidence, 6),
                confidence_note=confidence_note,
                verification_state=verification_state,
                open_source_sources_to_check=[dict(x) for x in OPEN_SOURCE_LEXICAL_SOURCES],
                grammar_review_status=grammar_review_status,
                correction_policy="suggest_only_under_human_supervision; never overwrite source card automatically",
            )
        )
    return sorted(notes, key=lambda n: (n.language, n.surface, n.card_id))


def lexical_holonomy_report(
    repo_root: str | Path = ".",
    *,
    language: str | None = None,
    query: str = "",
    limit_edges: int | None = 256,
    limit_notes: int | None = 128,
) -> dict[str, Any]:
    """Return lexical holonomy report for CIELingo."""
    units = extract_lexical_units(repo_root)
    edges = build_lexical_holonomy_edges(repo_root)
    notes = build_word_knowledge_notes(repo_root)
    files = list_language_card_files(repo_root)

    def match_text(texts: Iterable[str]) -> bool:
        if not query:
            return True
        q = _norm_surface(query)
        return any(q in _norm_surface(t) for t in texts)

    if language:
        units = [u for u in units if u.language == language]
        edges = [e for e in edges if e.language == language]
        notes = [n for n in notes if n.language == language]
    if query:
        unit_ids = {u.lexical_id for u in units if match_text([u.surface, u.lemma, u.card_id, u.canonical_label])}
        note_ids = {n.lexical_id for n in notes if match_text([n.surface, n.lemma, n.card_id])}
        edge_ids = unit_ids | note_ids
        edges = [
            e
            for e in edges
            if e.source_lexical_id in edge_ids
            or e.target_lexical_id in edge_ids
            or match_text([e.source_surface, e.target_surface, e.relation_type])
        ]
        notes = [n for n in notes if n.lexical_id in edge_ids or match_text([n.surface, n.lemma, n.card_id])]
        units = [u for u in units if u.lexical_id in edge_ids or match_text([u.surface, u.lemma, u.card_id, u.canonical_label])]

    relation_counts: dict[str, int] = {}
    family_counts: dict[str, int] = {}
    for e in edges:
        relation_counts[e.relation_type] = relation_counts.get(e.relation_type, 0) + 1
        family_counts[e.relation_family] = family_counts.get(e.relation_family, 0) + 1
    confidence_values = [n.knowledge_confidence for n in notes]
    mean_conf = sum(confidence_values) / len(confidence_values) if confidence_values else 0.0

    digest_payload = {
        "schema": LEXICAL_HOLONOMY_SCHEMA,
        "unit_count": len(units),
        "edge_count": len(edges),
        "note_count": len(notes),
        "relation_counts": relation_counts,
        "language": language,
        "query": query,
    }
    digest = hashlib.sha256(json.dumps(digest_payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

    return {
        "schema": LEXICAL_HOLONOMY_SCHEMA,
        "source_role": "local_noema_lns_lexical_holonomy_surface",
        "epistemic_status": "local seed + derived relation surface; external lexical sources are descriptors unless imported",
        "language_filter": language,
        "query": query,
        "lexical_unit_count": len(units),
        "edge_count": len(edges),
        "word_note_count": len(notes),
        "own_language_card_file_count": len(files),
        "relation_counts": dict(sorted(relation_counts.items())),
        "relation_family_counts": dict(sorted(family_counts.items())),
        "mean_knowledge_confidence": round(mean_conf, 6),
        "open_source_sources": [dict(x) for x in OPEN_SOURCE_LEXICAL_SOURCES],
        "registry_digest": digest,
        "own_card_access": [f.as_dict() for f in files[:64]],
        "lexical_units": [u.as_dict() for u in units[:128]],
        "edges": [e.as_dict() for e in (edges[:limit_edges] if limit_edges is not None else edges)],
        "word_notes": [n.as_dict() for n in (notes[:limit_notes] if limit_notes is not None else notes)],
    }


def write_lexical_holonomy_report(path: str | Path, repo_root: str | Path = ".", **kwargs: Any) -> Path:
    report = lexical_holonomy_report(repo_root, **kwargs)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out
