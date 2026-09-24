"""CIELingo infinitivization + residual-set merge audit.

This stage operates after ``unknown_word_audit``.  It tries to convert unknown
word surfaces to infinitive/action seeds where the local morphology heuristic is
safe enough, merges each infinitive candidate with the existing unknown-state
record, and assigns every remaining word to an owned residual set.

It never claims canonical morphology.  All mappings are candidates requiring
SGJP/Morfeusz/Wiktionary/plWordNet or human review.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, Sequence

SCHEMA = "cielingo/infinitive-merge-audit/v0.1"
CANDIDATE_CONFIDENCE = 0.5
HEURISTIC_CONFIDENCE_LOW = 0.34

from ciel_geometry.phasenav.metatime_contract import INFORMATION_KAPPA
KAPPA_INFO = INFORMATION_KAPPA

DIRECT_INFINITIVE_EXCEPTIONS = {"iść", "nieść", "wieść", "wieźć", "móc", "piec", "biec", "tłuc", "być"}
ABSTRACT_NOUN_SUFFIXES = ("ość", "ność", "łość", "wość", "istość", "alność", "ywność")
INFINITIVE_SUFFIXES = ("ować", "ywać", "iwać", "awać", "ać", "eć", "ić", "yć", "nąć", "ąć")
FINITE_UJE_SUFFIXES = ("uję", "ujesz", "uje", "ujemy", "ujecie", "ują")
PAST_SUFFIXES = ("łem", "łam", "łeś", "łaś", "liśmy", "łyśmy", "liście", "łyście")
PARTICIPLE_SUFFIXES = ("ący", "ąca", "ące", "ących", "ącym", "ącego", "any", "ana", "ane", "ony", "ona", "one", "ty", "ta", "te")
NOMINALIZATION_SUFFIXES = ("anie", "enia", "enie", "aniu", "eniu", "ciem", "cie")
NOUN_CASE_SUFFIXES = ("owi", "ami", "ach", "ego", "emu", "ymi", "ych", "ów", "om", "ie", "u", "a", "ą", "ę")
ADJECTIVE_SUFFIXES = ("owy", "owa", "owe", "nego", "nej", "nymi", "nych", "ski", "ska", "skie")
TECHNICAL_MARKERS = ("ciel", "noema", "htri", "cqcl", "orchor", "collatz", "tensor", "semantic", "phase")


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_word(text: str) -> str:
    return " ".join(str(text).strip().lower().split())


def sha256_json(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


@dataclass(frozen=True)
class InfinitiveCandidate:
    schema: str
    source_surface: str
    source_card_id: str | None
    infinitive_candidate: str
    mapping_type: str
    confidence: float
    confidence_note: str
    morphology_state: str
    merge_status: str
    source_state: dict[str, Any]
    semantic_merge: dict[str, Any]
    next_action: str
    digest: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResidualAssignment:
    schema: str
    surface: str
    source_card_id: str | None
    residual_set_id: str
    residual_set_label: str
    assignment_reason: str
    confidence: float
    source_state: dict[str, Any]
    next_action: str
    digest: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OwnedResidualSet:
    schema: str
    set_id: str
    label: str
    criteria: str
    count: int
    action_policy: str
    members: list[str]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def read_unknown_entries(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    out: list[dict[str, Any]] = []
    with p.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def is_direct_infinitive(word: str) -> bool:
    w = normalize_word(word)
    if not w or w.endswith("ąc") or w.endswith(ABSTRACT_NOUN_SUFFIXES):
        return False
    return w in DIRECT_INFINITIVE_EXCEPTIONS or w.endswith(INFINITIVE_SUFFIXES)


def infinitivize_word(word: str) -> tuple[str | None, str, float, str]:
    """Return infinitive candidate, mapping type, confidence, note."""
    w = normalize_word(word)
    if not w:
        return None, "empty", 0.0, "empty surface"
    if is_direct_infinitive(w):
        return w, "already_infinitive", 0.78, "surface already looks like Polish infinitive; still requires dictionary confirmation"
    # -uję/-uje/-ują family usually maps to -ować: kontynuuje -> kontynuować.
    for suf in FINITE_UJE_SUFFIXES:
        if w.endswith(suf) and len(w) > len(suf) + 2:
            stem = w[: -len(suf)]
            # Polish orthographic simplification: pracuję -> pracować, kontynuuję -> kontynuować.
            if stem.endswith("u"):
                candidate = stem + "ować"
            else:
                candidate = stem + "ować"
            return candidate, "finite_u_family_to_ować", 0.48, "finite -uj- family heuristic; requires Morfeusz/SGJP confirmation"
    # Adverbial participle: działając -> działać, kontynuując -> kontynuować.
    if w.endswith("ując") and len(w) > 5:
        stem = w[:-4]
        return stem + "ować", "adverbial_participle_ując_to_ować", 0.46, "-ując participle heuristic"
    if w.endswith("ając") and len(w) > 5:
        stem = w[:-4]
        return stem + "ać", "adverbial_participle_ając_to_ać", 0.44, "-ając participle heuristic"
    # Active adjectival participles are too ambiguous locally: wskazujący may
    # map to wskazywać, kodujący to kodować, etc. Keep them in residual
    # participle sets until a morphology source resolves the lemma.
    for suf in ("ujący", "ująca", "ujące", "ujących", "ującym", "ującego", "ający", "ająca", "ające", "ających", "ającym", "ającego"):
        if w.endswith(suf):
            return None, "active_participle_needs_morphology", 0.0, "active participle detected; infinitive not safely inferred locally"
    # Verbal nouns: działanie -> działać, tworzenie -> tworzyć-ish is too risky.  Keep low-confidence.
    if w.endswith(("owanie", "owania", "owaniu", "owaniem")) and len(w) > 8:
        stem = re.sub(r"owaniem$|owaniu$|owania$|owanie$", "", w)
        return stem + "ować", "verbal_noun_owanie_to_ować", 0.45, "verbal noun -owanie heuristic"
    if w.endswith(("anie", "ania", "aniu", "aniem")) and len(w) > 6:
        stem = re.sub(r"aniem$|aniu$|ania$|anie$", "", w)
        return stem + "ać", "verbal_noun_anie_to_ać_low_conf", 0.32, "verbal noun -anie heuristic; high ambiguity"
    if w.endswith(("enie", "enia", "eniu", "eniem")) and len(w) > 6:
        return None, "verbal_noun_enie_needs_morphology", 0.0, "verbal noun -enie is too ambiguous for safe local infinitivization"
    for suf in PAST_SUFFIXES:
        if w.endswith(suf) and len(w) > len(suf) + 2:
            return None, "past_form_needs_morphology", 0.0, "past-tense form detected but infinitive cannot be safely inferred locally"
    return None, "not_infinitivized", 0.0, "no safe infinitive heuristic"


def merge_semantic_state(entry: Mapping[str, Any], infinitive: str, confidence: float) -> dict[str, Any]:
    sem = dict(entry.get("semantic") or {})
    rest_mass = float(sem.get("semantic_rest_mass", 0.0))
    density = float(sem.get("density_priority_weight", 0.0))
    relation_energy = float(sem.get("relation_energy_proxy", 0.0))
    merged_mass = bounded((rest_mass * 0.72) + (confidence * 0.18) + (density * 0.10))
    return {
        "infinitive_candidate": infinitive,
        "source_semantic_rest_mass": rest_mass,
        "merged_semantic_rest_mass": round(merged_mass, 9),
        "merged_word_potential": round(merged_mass * KAPPA_INFO, 12),
        "source_density_priority_weight": density,
        "source_relation_energy_proxy": relation_energy,
        "state_merge_confidence": round(confidence, 6),
        "merge_policy": "candidate_state_merge_no_canon",
    }


def build_infinitive_candidates(entries: Sequence[Mapping[str, Any]]) -> list[InfinitiveCandidate]:
    out: list[InfinitiveCandidate] = []
    for entry in entries:
        surface = normalize_word(entry.get("surface") or entry.get("lemma_candidate") or "")
        candidate, mapping_type, conf, note = infinitivize_word(surface)
        if candidate is None:
            continue
        merge = merge_semantic_state(entry, candidate, conf)
        payload = {"surface": surface, "candidate": candidate, "mapping_type": mapping_type, "source_card_id": entry.get("source_card_id")}
        out.append(
            InfinitiveCandidate(
                schema="cielingo/infinitive-candidate-merge/v0.1",
                source_surface=surface,
                source_card_id=entry.get("source_card_id"),
                infinitive_candidate=candidate,
                mapping_type=mapping_type,
                confidence=round(conf, 6),
                confidence_note=note,
                morphology_state="infinitive_candidate_pending_source_verification",
                merge_status="merged_with_unknown_state_as_candidate",
                source_state=dict(entry),
                semantic_merge=merge,
                next_action="verify_with_morfeusz_sgjp_then_merge_or_reject",
                digest=sha256_json(payload),
            )
        )
    return out


def residual_set_for_word(entry: Mapping[str, Any]) -> tuple[str, str, str, float, str]:
    w = normalize_word(entry.get("surface") or entry.get("lemma_candidate") or "")
    missing_axis = str(entry.get("missing_axis") or "unknown")
    status = str(entry.get("classification_status") or "unknown")
    if not w:
        return "empty_surface", "Empty/missing surface", "surface missing", 0.0, "repair_source_record"
    if any(w.startswith(prefix) for prefix in TECHNICAL_MARKERS):
        return "project_or_foreign_terms", "Project/foreign/technical terms", "explicit project/technical marker", 0.34, "route_to_project_term_or_translation_review"
    if w.endswith(("ący", "ąca", "ące", "ącym", "ącego", "ących")) or w.endswith("ąc"):
        return "participle_forms", "Participles and participle-like forms", "participle suffix", 0.42, "morphological_review_for_participle_or_infinitive"
    if w.endswith(("anie", "enie", "owania", "owanie", "eniu", "aniu", "ciem", "cie")):
        return "verbal_nouns", "Verbal nouns / nominalized actions", "nominalization suffix", 0.39, "lemmatize_to_action_seed_or_noun"
    if w.endswith(("ego", "emu", "ych", "ymi", "ej", "ą", "ę", "owi", "ach", "ami", "ów", "om", "u")) or missing_axis == "morphology_and_lemma":
        return "inflected_nominal_or_adjectival_forms", "Inflected nominal/adjectival forms", "case/adjective inflection suffix or morphology debt", 0.36, "lemma_lookup_sgjp_morfeusz"
    if w.endswith(ADJECTIVE_SUFFIXES):
        return "adjectival_forms", "Adjectival forms", "adjective-like suffix", 0.40, "verify_adjective_lemma"
    if w.endswith(("nie", "o")) and len(w) > 4:
        return "adverbial_forms", "Adverbial forms", "adverb-like suffix", 0.34, "verify_adverb_or_neuter_form"
    if missing_axis == "language_identity":
        return "language_identity_unknown", "Language identity unresolved", "language identity missing", 0.25, "check_wiktionary_and_sgjp"
    if missing_axis == "meaning_and_part_of_speech":
        return "pos_meaning_unknown", "Meaning and POS unresolved", "meaning/POS missing", 0.25, "check_wiktionary_sgjp_plwordnet"
    return "general_unknown_pool", "General unknown pool", "no stronger residual rule", 0.20, "human_review_or_source_lookup"


def build_residual_assignments(entries: Sequence[Mapping[str, Any]], candidates: Sequence[InfinitiveCandidate]) -> list[ResidualAssignment]:
    candidate_surfaces = {c.source_surface for c in candidates}
    out: list[ResidualAssignment] = []
    for entry in entries:
        surface = normalize_word(entry.get("surface") or entry.get("lemma_candidate") or "")
        if surface in candidate_surfaces:
            continue
        set_id, label, reason, conf, action = residual_set_for_word(entry)
        payload = {"surface": surface, "set": set_id, "source_card_id": entry.get("source_card_id")}
        out.append(
            ResidualAssignment(
                schema="cielingo/residual-word-assignment/v0.1",
                surface=surface,
                source_card_id=entry.get("source_card_id"),
                residual_set_id=set_id,
                residual_set_label=label,
                assignment_reason=reason,
                confidence=round(conf, 6),
                source_state=dict(entry),
                next_action=action,
                digest=sha256_json(payload),
            )
        )
    return out


def build_owned_residual_sets(assignments: Sequence[ResidualAssignment]) -> list[OwnedResidualSet]:
    meta = {
        "project_or_foreign_terms": ("Project/foreign/technical terms", "route to translation/project-term review"),
        "participle_forms": ("Participles and participle-like forms", "verify participle vs infinitive"),
        "verbal_nouns": ("Verbal nouns / nominalized actions", "decide action seed vs noun"),
        "inflected_nominal_or_adjectival_forms": ("Inflected nominal/adjectival forms", "lemma lookup in morphology source"),
        "adjectival_forms": ("Adjectival forms", "verify adjective lemma"),
        "adverbial_forms": ("Adverbial forms", "verify adverb vs neuter/adjective form"),
        "language_identity_unknown": ("Language identity unresolved", "check source language"),
        "pos_meaning_unknown": ("Meaning and POS unresolved", "dictionary and relation review"),
        "general_unknown_pool": ("General unknown pool", "manual/source review"),
        "empty_surface": ("Empty/missing surface", "repair source record"),
    }
    by_set: dict[str, list[str]] = {}
    for a in assignments:
        by_set.setdefault(a.residual_set_id, []).append(a.surface)
    out: list[OwnedResidualSet] = []
    for set_id, members in sorted(by_set.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        label, policy = meta.get(set_id, (set_id, "review"))
        out.append(
            OwnedResidualSet(
                schema="cielingo/owned-residual-set/v0.1",
                set_id=set_id,
                label=label,
                criteria="deterministic local suffix/status heuristic; not canonical morphology",
                count=len(members),
                action_policy=policy,
                members=sorted(members),
            )
        )
    return out


def write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def generate_infinitive_merge_audit(unknown_words_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    input_path = Path(unknown_words_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    entries = read_unknown_entries(input_path)
    candidates = build_infinitive_candidates(entries)
    residuals = build_residual_assignments(entries, candidates)
    sets = build_owned_residual_sets(residuals)

    write_jsonl(out / "infinitive_candidates.jsonl", (c.as_dict() for c in candidates))
    write_jsonl(out / "infinitive_state_merged.jsonl", (c.as_dict() for c in candidates))
    write_jsonl(out / "residual_assignments.jsonl", (r.as_dict() for r in residuals))
    write_jsonl(out / "owned_residual_sets.jsonl", (s.as_dict() for s in sets))

    by_inf: dict[str, int] = {}
    for c in candidates:
        by_inf[c.infinitive_candidate] = by_inf.get(c.infinitive_candidate, 0) + 1
    mapping_counts: dict[str, int] = {}
    for c in candidates:
        mapping_counts[c.mapping_type] = mapping_counts.get(c.mapping_type, 0) + 1
    residual_counts = {s.set_id: s.count for s in sets}
    report = {
        "schema": SCHEMA,
        "created_at_utc": utc_now(),
        "source_unknown_words_path": str(input_path),
        "input_unknown_count": len(entries),
        "infinitivized_count": len(candidates),
        "unique_infinitive_count": len(by_inf),
        "residual_count": len(residuals),
        "owned_residual_set_count": len(sets),
        "candidate_confidence_floor": CANDIDATE_CONFIDENCE,
        "mapping_type_counts": dict(sorted(mapping_counts.items())),
        "residual_set_counts": dict(sorted(residual_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "top_infinitive_candidates": sorted(by_inf.items(), key=lambda kv: (-kv[1], kv[0]))[:30],
        "outputs": {
            "infinitive_candidates": str(out / "infinitive_candidates.jsonl"),
            "infinitive_state_merged": str(out / "infinitive_state_merged.jsonl"),
            "residual_assignments": str(out / "residual_assignments.jsonl"),
            "owned_residual_sets": str(out / "owned_residual_sets.jsonl"),
        },
        "epistemic_boundary": "local heuristic infinitivization and residual grouping; no canonical morphology or external source lookup claimed",
    }
    report["digest"] = sha256_json(report)
    (out / "infinitive_merge_audit_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


__all__ = [
    "InfinitiveCandidate",
    "ResidualAssignment",
    "OwnedResidualSet",
    "infinitivize_word",
    "build_infinitive_candidates",
    "build_residual_assignments",
    "build_owned_residual_sets",
    "generate_infinitive_merge_audit",
]
