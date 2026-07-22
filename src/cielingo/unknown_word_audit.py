"""CIELingo unknown-word audit surface.

The audit turns productive failure into a structured learning queue.  It reads
``unknown_word_candidate`` cards generated from the meaning-debt bundle and
classifies the reason why each word is unknown without promoting any word to
canon.

Rules:
* unknown is a valid state, not a failure terminal;
* sequence/card ordinals are provenance only and never semantic rank;
* every unknown receives a debt type, missing axis, next action and confidence;
* candidate_0_5 means supervised learning material, not WORD_CARD_PASS;
* external sources are queued, not assumed;
* Collatz learning cycle: ×3+1 expands candidate hypotheses so /2 can reduce them by source evidence and supervised review.

POLICY CHANGE (2026-07-11, Adrian, direct and explicit): "auto kanonizacja
jest WYMOGIEM, kazde slowo musi miec karte z atrybutami semantyki fazy
etc" (auto-canonization is a REQUIREMENT, every word must have a card
with phase/semantic attributes). This REVERSES the `auto_canonization_allowed
= False` boundary stated above and in every record this module produces —
recorded here transparently rather than silently changed. See
canonize_resolved_words() below: every word with real dictionary evidence
(resolve_source_lookup_queue()'s "source_found" status) now gets a
cards/words/WORD-*.noema.card.json card with a 36D PhaseNav phase vector,
written automatically, no supervised review gate. Known accuracy caveat
carried forward honestly: the domain-trust filter used for evidence
(wiktionary.org/sjp.pl/etc) confirms a TRUSTED SOURCE but not that the
result is actually about the target word (measured ~75% precision on an
8-word test batch) — auto-canonized cards inherit this risk.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


from dataclasses import asdict, dataclass
import datetime as dt
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, Sequence

from ciel_geometry.paths import P as _P

SCHEMA = "cielingo/unknown-word-audit/v0.2"
UNKNOWN_AUDIT_VERSION = "0.2.0"
DEFAULT_BATCH_SIZE = 100

PROJECT_TERMS = {
    "ciel", "noema", "htri", "cqcl", "orchorbital", "orbital", "collatz",
    "kuramoto", "tensor", "skalar", "semantic", "phase", "runtime", "source",
    "target", "pipeline", "vector", "holonomy", "holonomia", "kfo", "sot",
}
CONNECTOR_MISSED = {"niż", "jak", "jako", "oraz", "czyli", "wobec", "według", "aby", "żeby"}
QUANTIFIER_PRONOUNISH = {"mnogi", "wiele", "kilka", "każdy", "żaden", "pewien", "inny", "taki", "który"}
POSSIBLE_FOREIGN = {
    "target", "source", "runtime", "pipeline", "event", "query", "surface", "token",
    "vector", "sync", "bus", "phase", "shell", "commit", "branch", "patch",
}

POLISH_LETTERS = set("ąćęłńóśźż")
ADJ_INFLECTED_SUFFIXES = (
    "ego", "emu", "ej", "ą", "ym", "ymi", "ych", "imi", "iego", "iemu",
    "owych", "owymi", "alnych", "alnymi", "nej", "nym", "nymi",
)
NOUN_INFLECTED_SUFFIXES = (
    "ami", "ach", "owi", "em", "om", "ów", "ą", "ę", "u", "ie", "ią", "iami",
    "enia", "eniu", "aniem", "ania", "aniu", "ości", "nością", "nościami",
)
VERBAL_OR_PARTICIPLE_SUFFIXES = (
    "ąc", "any", "ana", "ane", "ony", "ona", "one", "ty", "ta", "te", "wszy",
    "łszy", "enie", "anie", "ujący", "ująca", "ujące", "iony", "iona", "ione",
)
ADVERBIAL_SUFFIXES = ("nie", "cie", "o")


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_word(value: Any) -> str:
    return " ".join(str(value or "").strip().lower().split())


def has_polish_signal(word: str) -> bool:
    return any(ch in POLISH_LETTERS for ch in normalize_word(word))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


@dataclass(frozen=True)
class UnknownWordAuditEntry:
    schema: str
    version: str
    surface: str
    lemma_candidate: str
    source_card_id: str
    source_file: str
    candidate_card_id: str
    classification_status: str
    debt_type: str
    missing_axis: str
    part_of_speech_candidate: str
    sentence_function_candidate: str
    inflection_status: str
    morphology_hint: str
    source_status: str
    confidence: float
    confidence_note: str
    semantic_potential: float
    density_priority_weight: float
    viscosity_solo_subjective: float
    viscosity_group_subjective: float
    affective_colour_candidate: str
    affective_intensity_candidate: float
    register_candidate: str
    next_action: str
    source_lookup_targets: tuple[str, ...]
    collatz_operator: str
    collatz_expand_targets: tuple[str, ...]
    collatz_reduce_targets: tuple[str, ...]
    collatz_learning_note: str
    productive_failure: bool = True
    auto_canonization_allowed: bool = False


@dataclass(frozen=True)
class UnknownCluster:
    schema: str
    cluster_key: str
    cluster_type: str
    count: int
    examples: tuple[str, ...]
    missing_axis: str
    next_action: str


@dataclass(frozen=True)
class UnknownWordAuditReport:
    schema: str
    generated_at: str
    unknown_count: int
    productive_failure_count: int
    by_debt_type: dict[str, int]
    by_missing_axis: dict[str, int]
    by_next_action: dict[str, int]
    review_batch_count: int
    review_batch_size: int
    source_lookup_count: int
    candidate_0_5_count: int
    unknown_is_productive: bool
    output_dir: str


def _card_semantic(card: Mapping[str, Any], key: str, default: float) -> float:
    sem = card.get("semantic_designation") or {}
    try:
        return float(sem.get(key, default))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/cielingo/unknown_word_audit.py:165 quiet except scope=_card_semantic reason=return default")
        return default


def _candidate_surface(card: Mapping[str, Any]) -> tuple[str, str]:
    surface = normalize_word(card.get("surface"))
    lemma = normalize_word(card.get("lemma") or surface)
    return surface, lemma


def _source_record(card: Mapping[str, Any]) -> Mapping[str, Any]:
    rec = card.get("source_debt_record")
    return rec if isinstance(rec, Mapping) else {}


def classify_unknown_word(card: Mapping[str, Any]) -> tuple[str, str, str, str, str, str, float, str, tuple[str, ...]]:
    """Return audit classification for an unknown candidate.

    Tuple fields: debt_type, missing_axis, pos, sentence_fn, inflection_status,
    morphology_hint, confidence, next_action, source_lookup_targets.
    """
    surface, lemma = _candidate_surface(card)
    source = _source_record(card)
    flags = set(source.get("debt_flags") or [])
    if isinstance(source.get("debt_flags"), str):
        flags = set(x for x in str(source.get("debt_flags")).split(";") if x)

    raw = " ".join([surface, lemma]).lower()

    if not lemma:
        return (
            "empty_or_missing_surface",
            "surface_lemma_axis",
            "unknown",
            "unresolved_sentence_role",
            "missing",
            "no surface/lemma available",
            0.05,
            "repair_source_card_surface_or_lemma",
            ("human_review",),
        )

    if " " in lemma or " " in surface:
        return (
            "multiword_expression_fragment",
            "segmentation_axis",
            "expression_fragment_candidate",
            "multiword_expression_pending_segmentation",
            "not_single_word",
            "contains whitespace; requires segmentation before POS classification",
            0.25,
            "segment_expression_then_reaudit",
            ("human_review", "Wiktionary/pl"),
        )

    if lemma in CONNECTOR_MISSED:
        return (
            "closed_class_missed",
            "closed_class_operator_axis",
            "connector_or_comparative_particle_candidate",
            "clause_or_comparison_operator",
            "uninflected_or_weakly_inflected",
            "known Polish closed-class item missing from local closed-class seeds",
            0.55,
            "add_to_closed_class_seed_after_source_check",
            ("Wiktionary/pl", "SGJP_or_Morfeusz"),
        )

    if lemma in QUANTIFIER_PRONOUNISH:
        return (
            "quantifier_pronoun_axis_missing",
            "quantifier_pronoun_axis",
            "quantifier_or_pronoun_candidate",
            "determiner_or_argument_modifier",
            "inflected_possible",
            "quantifier/pronoun-like word not covered by current heuristic",
            0.48,
            "verify_quantifier_pronoun_class_and_add_axis",
            ("Wiktionary/pl", "SGJP_or_Morfeusz", "plWordNet"),
        )

    if any(term in raw for term in PROJECT_TERMS) or "surface_english_or_project_term" in flags:
        return (
            "project_or_runtime_term_candidate",
            "project_namespace_axis",
            "project_term_or_foreign_technical_candidate",
            "technical_label_pending_translation_or_namespace",
            "not_polish_inflection_or_mixed",
            "project/runtime/foreign surface requires namespace rather than Polish POS canon",
            0.42,
            "route_to_project_term_lexicon_not_core_polish_word_card",
            ("project_glossary", "human_review"),
        )

    if lemma in POSSIBLE_FOREIGN or (re.fullmatch(r"[a-z0-9_-]+", lemma) and not has_polish_signal(lemma) and len(lemma) > 5):
        return (
            "foreign_or_technical_candidate",
            "language_detection_axis",
            "foreign_or_technical_word_candidate",
            "technical_or_borrowed_term_pending_language_detection",
            "unknown_language_or_borrowed",
            "ASCII/non-diacritic token with technical/foreign profile; Polish words without diacritics still need source check",
            0.36,
            "verify_language_and_register_before_polish_card",
            ("Wiktionary/pl", "human_review"),
        )

    if lemma.endswith(ADJ_INFLECTED_SUFFIXES):
        return (
            "unknown_inflected_form_candidate",
            "morphology_axis",
            "adjective_or_pronominal_inflected_form_candidate",
            "attribute_or_argument_modifier_candidate",
            "likely_inflected_form",
            "adjective/pronominal inflection suffix; needs lemma recovery",
            0.44,
            "send_to_morphology_lookup_for_lemma_recovery",
            ("SGJP_or_Morfeusz", "Wiktionary/pl"),
        )

    if lemma.endswith(VERBAL_OR_PARTICIPLE_SUFFIXES):
        return (
            "verbal_noun_or_participle_candidate",
            "verb_derivation_axis",
            "participle_or_verbal_noun_candidate",
            "predicate_derivative_or_modifier_candidate",
            "derived_or_inflected_form",
            "verbal noun/participle-like ending; needs derivational analysis",
            0.41,
            "send_to_morphology_and_derivation_lookup",
            ("SGJP_or_Morfeusz", "Wiktionary/pl"),
        )

    if lemma.endswith(NOUN_INFLECTED_SUFFIXES):
        return (
            "unknown_inflected_form_candidate",
            "case_inflection_axis",
            "noun_inflected_form_candidate",
            "subject_or_object_candidate_pending_case",
            "likely_case_inflected_form",
            "nominal case suffix; needs lemma and case recovery",
            0.43,
            "send_to_case_morphology_lookup_for_lemma_recovery",
            ("SGJP_or_Morfeusz", "Wiktionary/pl", "plWordNet"),
        )

    if lemma.endswith(ADVERBIAL_SUFFIXES) and len(lemma) > 4:
        return (
            "adverb_or_manner_axis_missing",
            "adverbial_axis",
            "adverb_or_manner_candidate",
            "adverbial_modifier_candidate",
            "possibly_uninflected_or_derived",
            "adverb-like ending not accepted by current heuristic due low evidence",
            0.38,
            "verify_adverbial_status_and_affective_register",
            ("Wiktionary/pl", "SGJP_or_Morfeusz"),
        )

    if has_polish_signal(lemma):
        return (
            "unknown_real_polish_word_candidate",
            "open_lexicon_axis",
            "unknown_polish_word_candidate",
            "unresolved_sentence_role",
            "unknown",
            "Polish diacritic signal but no local grammatical evidence",
            0.35,
            "lookup_in_polish_open_sources_then_reaudit",
            ("Wiktionary/pl", "SGJP_or_Morfeusz", "plWordNet"),
        )

    return (
        "source_required_before_classification",
        "source_evidence_axis",
        "unknown_word_candidate",
        "unresolved_sentence_role",
        "unknown",
        "no reliable local grammatical/morphological evidence",
        0.30,
        "queue_for_source_lookup_and_human_review",
        ("Wiktionary/pl", "SGJP_or_Morfeusz", "human_review"),
    )




def collatz_learning_cycle(debt_type: str, missing_axis: str) -> tuple[str, tuple[str, ...], tuple[str, ...], str]:
    """Return the Collatz-style learning cycle for an unknown word.

    The odd/unknown state is intentionally expanded by ``×3+1``: POS/lemma,
    morphology/source and affect/register hypotheses plus a hard no-canon
    boundary.  The expanded candidate can then be reduced by ``/2`` through
    evidence and supervised review.  This keeps failure productive without
    converting uncertainty into fake certainty.
    """
    expand = (
        "part_of_speech_or_sentence_function_hypothesis",
        f"missing_axis_hypothesis:{missing_axis}",
        f"debt_type_hypothesis:{debt_type}",
        "boundary:no_auto_canonization",
    )
    reduce = (
        "open_source_evidence_filter",
        "human_supervised_review_filter",
    )
    note = (
        "×3+1 expands the unknown into multiple explicit hypotheses plus one "
        "boundary condition; /2 reduces the candidate only after source evidence "
        "and supervised review. Expansion exists so reduction has structure."
    )
    return "expand_3_plus_1_then_reduce_by_2", expand, reduce, note

def audit_entry_from_card(card: Mapping[str, Any]) -> UnknownWordAuditEntry:
    surface, lemma = _candidate_surface(card)
    source = _source_record(card)
    debt_type, missing_axis, pos, sentence_fn, infl, morph, conf, action, targets = classify_unknown_word(card)
    sem = card.get("semantic_designation") or {}
    collatz_operator, collatz_expand_targets, collatz_reduce_targets, collatz_note = collatz_learning_cycle(debt_type, missing_axis)
    return UnknownWordAuditEntry(
        schema=SCHEMA,
        version=UNKNOWN_AUDIT_VERSION,
        surface=surface,
        lemma_candidate=lemma,
        source_card_id=str(source.get("source_card_id") or ""),
        source_file=str(source.get("source_file") or ""),
        candidate_card_id=str(card.get("id") or card.get("card_id") or ""),
        classification_status="audited_unknown_not_canon",
        debt_type=debt_type,
        missing_axis=missing_axis,
        part_of_speech_candidate=pos,
        sentence_function_candidate=sentence_fn,
        inflection_status=infl,
        morphology_hint=morph,
        source_status="source_required_before_promotion",
        confidence=round(float(conf), 6),
        confidence_note=(
            "Productive failure audit: unknown state is retained until source evidence "
            "and supervised review resolve the missing axis. This is not WORD_CARD_PASS."
        ),
        semantic_potential=round(_card_semantic(card, "word_potential", 0.0), 12),
        density_priority_weight=round(_card_semantic(card, "density_priority_weight", 0.5), 9),
        viscosity_solo_subjective=round(_card_semantic(card, "viscosity_solo_subjective", 0.5), 9),
        viscosity_group_subjective=round(_card_semantic(card, "viscosity_group_subjective", 0.5), 9),
        affective_colour_candidate=str(sem.get("colour") or "unknown_colour_pending_context"),
        affective_intensity_candidate=round(_card_semantic(card, "intensity", 0.0), 9),
        register_candidate=str(sem.get("register_candidate") or "unknown_pending_source_verification"),
        next_action=action,
        source_lookup_targets=tuple(targets),
        collatz_operator=collatz_operator,
        collatz_expand_targets=collatz_expand_targets,
        collatz_reduce_targets=collatz_reduce_targets,
        collatz_learning_note=collatz_note,
    )


def load_unknown_candidate_cards(repo_root: Path) -> list[dict[str, Any]]:
    repo_root = Path(repo_root)
    path = repo_root / "data" / "cielingo" / "debt_word_cards" / "by_part_of_speech" / "unknown_word_candidate.jsonl"
    return read_jsonl(path)


def count_by(entries: Sequence[UnknownWordAuditEntry], attr: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for entry in entries:
        key = str(getattr(entry, attr))
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))


def build_unknown_clusters(entries: Sequence[UnknownWordAuditEntry]) -> list[UnknownCluster]:
    grouped: dict[tuple[str, str], list[UnknownWordAuditEntry]] = {}
    for entry in entries:
        suffix = entry.lemma_candidate[-3:] if len(entry.lemma_candidate) >= 3 else entry.lemma_candidate
        key = (entry.debt_type, suffix)
        grouped.setdefault(key, []).append(entry)
    clusters: list[UnknownCluster] = []
    for (debt_type, suffix), rows in grouped.items():
        examples = tuple(e.lemma_candidate for e in rows[:10])
        clusters.append(
            UnknownCluster(
                schema=SCHEMA,
                cluster_key=f"{debt_type}|suffix:{suffix}",
                cluster_type=debt_type,
                count=len(rows),
                examples=examples,
                missing_axis=rows[0].missing_axis,
                next_action=rows[0].next_action,
            )
        )
    clusters.sort(key=lambda c: (-c.count, c.cluster_key))
    return clusters


def source_lookup_record(entry: UnknownWordAuditEntry) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "surface": entry.surface,
        "lemma_candidate": entry.lemma_candidate,
        "candidate_card_id": entry.candidate_card_id,
        "debt_type": entry.debt_type,
        "missing_axis": entry.missing_axis,
        "source_lookup_targets": list(entry.source_lookup_targets),
        "next_action": entry.next_action,
        "auto_canonization_allowed": False,
        "minimum_confidence_after_evidence": 0.5,
        "collatz_operator": entry.collatz_operator,
        "collatz_expand_targets": list(entry.collatz_expand_targets),
        "collatz_reduce_targets": list(entry.collatz_reduce_targets),
        "status": "queued_for_source_lookup",
    }


def candidate_0_5_record(entry: UnknownWordAuditEntry) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "surface": entry.surface,
        "lemma_candidate": entry.lemma_candidate,
        "candidate_card_id": entry.candidate_card_id,
        "status": "candidate_0_5_pending_source_and_supervised_review",
        "confidence": 0.5,
        "classification_status": entry.classification_status,
        "debt_type": entry.debt_type,
        "missing_axis": entry.missing_axis,
        "part_of_speech_candidate": entry.part_of_speech_candidate,
        "sentence_function_candidate": entry.sentence_function_candidate,
        "next_action": entry.next_action,
        "collatz_operator": entry.collatz_operator,
        "collatz_learning_note": entry.collatz_learning_note,
        "not_canon": True,
    }


def review_batches(entries: Sequence[UnknownWordAuditEntry], batch_size: int = DEFAULT_BATCH_SIZE) -> list[list[UnknownWordAuditEntry]]:
    return [list(entries[i : i + batch_size]) for i in range(0, len(entries), batch_size)]


def audit_unknown_words(repo_root: Path, *, batch_size: int = DEFAULT_BATCH_SIZE, output_dir: Path | None = None) -> UnknownWordAuditReport:
    repo_root = Path(repo_root)
    output_dir = output_dir or repo_root / "data" / "cielingo" / "unknown_word_audit"
    cards = load_unknown_candidate_cards(repo_root)
    entries = [audit_entry_from_card(card) for card in cards]
    entries.sort(key=lambda e: (e.debt_type, e.lemma_candidate, e.candidate_card_id))

    clusters = build_unknown_clusters(entries)
    batches = review_batches(entries, batch_size=batch_size)

    write_jsonl(output_dir / "unknown_words.audit.jsonl", (asdict(e) for e in entries))
    write_jsonl(output_dir / "unknown_clusters.jsonl", (asdict(c) for c in clusters))
    write_jsonl(output_dir / "source_lookup_queue.jsonl", (source_lookup_record(e) for e in entries))
    write_jsonl(output_dir / "promotion_candidates_0_5.jsonl", (candidate_0_5_record(e) for e in entries))

    review_dir = output_dir / "review_batches"
    review_dir.mkdir(parents=True, exist_ok=True)
    # Clear only generated review jsonl files to keep append-only upstream data intact.
    for old in review_dir.glob("batch_*.jsonl"):
        old.unlink()
    for idx, batch in enumerate(batches, start=1):
        write_jsonl(review_dir / f"batch_{idx:03d}.jsonl", (asdict(e) for e in batch))

    by_debt_type = count_by(entries, "debt_type")
    by_missing_axis = count_by(entries, "missing_axis")
    by_next_action = count_by(entries, "next_action")
    missing_axes = {
        "schema": SCHEMA,
        "generated_at": utc_now(),
        "unknown_count": len(entries),
        "unknown_is_productive": True,
        "by_debt_type": by_debt_type,
        "by_missing_axis": by_missing_axis,
        "by_next_action": by_next_action,
        "top_clusters": [asdict(c) for c in clusters[:25]],
        "collatz_learning_cycle": {
            "operator": "expand_3_plus_1_then_reduce_by_2",
            "meaning": "×3+1 expands unknowns into structured hypotheses; /2 reduces only after source evidence and supervised review.",
            "auto_canonization_allowed": False,
        },
        "interpretation": (
            "Unknown words expose missing axes: morphology, closed classes, project namespace, "
            "source evidence, segmentation, register and affect. No unknown is canonized here. "
            "Collatz expansion exists so reduction has structure."
        ),
    }
    write_json(output_dir / "missing_axes_report.json", missing_axes)

    report = UnknownWordAuditReport(
        schema=SCHEMA,
        generated_at=utc_now(),
        unknown_count=len(entries),
        productive_failure_count=sum(1 for e in entries if e.productive_failure),
        by_debt_type=by_debt_type,
        by_missing_axis=by_missing_axis,
        by_next_action=by_next_action,
        review_batch_count=len(batches),
        review_batch_size=batch_size,
        source_lookup_count=len(entries),
        candidate_0_5_count=len(entries),
        unknown_is_productive=True,
        output_dir=str(output_dir.relative_to(repo_root) if output_dir.is_relative_to(repo_root) else output_dir),
    )
    write_json(output_dir / "unknown_word_audit.report.json", asdict(report))
    return report


def resolve_source_lookup_queue(
    queue_path: Path,
    *,
    output_path: Path | None = None,
    offset: int = 0,
    limit: int | None = None,
) -> dict[str, Any]:
    """Consume source_lookup_queue.jsonl: for each queued word, actually
    search the web (ciel_geometry.web_search.search) and record what was
    found as evidence.

    Origin (2026-07-11): Adrian, direct — "pozwól CIELingo sprawdzać w
    sieci poszczególne słowa i ich sens... pozwól natywnie uzupełniać jej
    pewność i bibliotekę". The audit system above already classifies and
    QUEUES unknown words (source_lookup_queue.jsonl, 644 entries as of
    tonight) but nothing ever consumed that queue — this is the missing
    resolver step.

    Respects the queue's evidence boundary:
    - confidence rises toward each record's own `minimum_confidence_after_evidence`
      (0.5) when real evidence is found, capped there — never higher.
    - `auto_canonization_allowed` becomes True only for `source_found`
      records with trusted dictionary evidence. A source miss remains False.
    - a failed/empty search for one word does not stop the batch (matches
      the redigest's "signal and continue" pattern, not silent, not fatal).

    offset/limit: process the queue in resumable chunks (2026-07-11 —
    644-word queue, web search too slow to do in one call; each batch call
    passes the next offset explicitly, tracked by the caller).

    Returns summary stats. Writes resolved_lookups.jsonl (append) next to
    the queue.
    """
    from ciel_geometry.web_search import search as _web_search

    output_path = output_path or queue_path.parent / "resolved_lookups.jsonl"
    queue = read_jsonl(queue_path)
    if offset > 0:
        queue = queue[offset:]
    if limit is not None:
        queue = queue[:limit]

    resolved: list[dict[str, Any]] = []
    n_found = 0
    n_not_found = 0

    # Trusted dictionary/lexicon domains — a hit only counts as real
    # evidence if it actually comes from one of these, not just any web
    # result (found via a small test batch: generic queries returned
    # noise like Bing wallpaper pages and unrelated banking sites).
    _DICTIONARY_DOMAINS = ("wiktionary.org", "sjp.pl", "sjp.pwn.pl", "wsjp.pl")

    for record in queue:
        lemma = str(record.get("lemma_candidate") or record.get("surface") or "").strip()
        if not lemma:
            continue
        # `site:` restriction was tried first — this DDG backend doesn't
        # honour it (0/8 hits in testing), so filter by trusted domain
        # AFTER a plain query instead of restricting the query itself.
        query = f"{lemma} wiktionary słownik"
        hits = _web_search(query, max_results=5)
        trusted_hits = [h for h in hits if any(d in h.get("url", "") for d in _DICTIONARY_DOMAINS)]

        if trusted_hits:
            n_found += 1
            evidence_texts = [f"{h.get('title', '')}: {h.get('snippet', '')}" for h in trusted_hits if h.get("snippet")]
            resolved.append({
                **record,
                "status": "source_found",
                "confidence": record.get("minimum_confidence_after_evidence", 0.5),
                "evidence": evidence_texts[:3],
                "evidence_urls": [h.get("url", "") for h in trusted_hits],
                # Trusted source evidence is the explicit admission boundary;
                # automatic canonization is enabled after it is crossed.
                "auto_canonization_allowed": True,
                "collatz_reduce_targets": [
                    "open_source_evidence_filter",
                    "auto_canonization",
                ],
            })
        else:
            n_not_found += 1
            resolved.append({
                **record,
                "status": "source_not_found",
                "confidence": record.get("confidence", 0.3),  # unchanged, no evidence
                "evidence": [],
                "auto_canonization_allowed": False,
            })

    with output_path.open("a", encoding="utf-8") as fh:
        for r in resolved:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")

    return {
        "queue_size_processed": len(queue),
        "n_found": n_found,
        "n_not_found": n_not_found,
        "output_path": str(output_path),
    }


def _next_word_card_id(cards_dir: Path) -> int:
    """Highest existing WORD-NNNN id + 1 — same numbering scheme already
    used by cards/words/WORD-*.noema.card.json (34 cards as of tonight)."""
    highest = 0
    for p in cards_dir.glob("WORD-*.noema.card.json"):
        try:
            n = int(p.stem.split(".")[0].split("-")[1])
        except (IndexError, ValueError):
            continue
        highest = max(highest, n)
    return highest + 1


def canonize_resolved_words(
    resolved_path: Path,
    cards_dir: Path,
    *,
    limit: int | None = None,
) -> dict[str, Any]:
    """Auto-canonize every resolved word with real dictionary evidence into
    a cards/words/WORD-*.noema.card.json card carrying a 36D PhaseNav phase
    vector + semantic attributes.

    2026-07-11 policy change (see module docstring) — no supervised review
    gate, per Adrian's explicit "auto kanonizacja jest WYMOGIEM". Only
    processes status="source_found" records (real dictionary evidence);
    "source_not_found" records stay in the queue for a future retry, not
    canonized on no evidence.
    """
    from ciel_geometry.cielingo_phase_encoder import fast_encode_text
    # 2026-07-11, Adrian: "zacznij wpinac WSZYSTKO" — cielingo_core's real
    # runtime-card generator (operator bindings, consent/risk/residue
    # profiles) already existed and was even already called once by
    # auto_verify.py::generate_card_from_search(), but that call site
    # discards the result immediately after building it (dead code) and
    # this function's own cards never used it at all, writing a flatter
    # ad-hoc schema instead. Wire the real generator in additively.
    try:
        from cielingo_core.global_layer.card_generator import generate_runtime_card
    except ImportError as e:
        from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
        phase_signal_exception("unknown_word_audit.canonize_resolved_words:import_card_generator", e, operator_id="PAUSE")
        raise

    cards_dir.mkdir(parents=True, exist_ok=True)
    records = read_jsonl(resolved_path)
    if limit is not None:
        records = records[:limit]

    next_id = _next_word_card_id(cards_dir)
    written = []
    existing_lemmas: set[str] = set()
    for existing_path in cards_dir.glob("WORD-*.noema.card.json"):
        try:
            existing_card = json.loads(existing_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if existing_card.get("schema") == "cielingo/word-card/v1":
            existing_lemma = str(existing_card.get("name") or "").strip().casefold()
            if existing_lemma:
                existing_lemmas.add(existing_lemma)
    skipped_existing = 0

    for record in records:
        if record.get("status") != "source_found":
            continue
        lemma = str(record.get("lemma_candidate") or record.get("surface") or "").strip()
        if not lemma:
            continue
        if lemma.casefold() in existing_lemmas:
            skipped_existing += 1
            continue

        evidence_texts = record.get("evidence") or []
        encode_text = f"{lemma} " + " ".join(evidence_texts)
        phi = fast_encode_text(encode_text)

        card_id = f"WORD-{next_id:04d}"
        card = {
            "schema": "cielingo/word-card/v1",
            "card_id": card_id,
            "name": lemma,
            "type": "word",
            "root_meaning": (evidence_texts[0][:300] if evidence_texts else "auto-canonized, no evidence text"),
            "source": "web_lookup_auto_canonized",
            "confidence": record.get("confidence", 0.5),
            "debt_type": record.get("debt_type", ""),
            "missing_axis": record.get("missing_axis", ""),
            "part_of_speech_candidate": record.get("part_of_speech_candidate", ""),
            "register_candidate": record.get("register_candidate", ""),
            "phase_vector_36d": [round(float(x), 6) for x in phi],
            "evidence_urls": record.get("evidence_urls", []),
            "canonization_note": (
                "auto-canonized 2026-07-11 per Adrian's explicit policy change "
                "(auto_canonization_allowed boundary reversed) — not supervised-reviewed."
            ),
        }

        # Operator bindings / consent-memory-risk-residue profile from the
        # real CIELingo runtime-card generator — additive, batch-tolerant
        # (one word's generator failure shouldn't drop the whole batch, same
        # as evidence/lookup failures elsewhere in this loop).
        try:
            function_text = " ".join(filter(None, [
                str(record.get("part_of_speech_candidate", "")),
                evidence_texts[0][:200] if evidence_texts else "",
            ]))
            runtime_card = generate_runtime_card(
                card_id=card_id,
                slot_id=next_id,
                language_id=str(record.get("language_hint", "pl")),
                lemma=lemma,
                function=function_text,
            )
            card["runtime_card"] = runtime_card.to_dict()
        except Exception as e:
            from ciel_geometry.phasenav_exception_bridge import phase_signal_exception
            phase_signal_exception("unknown_word_audit.canonize_resolved_words:runtime_card", e, operator_id="PAUSE")
        path = cards_dir / f"{card_id}.noema.card.json"
        path.write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(card_id)
        existing_lemmas.add(lemma.casefold())

        # Append runtime card to CIELingo cards JSONL
        try:
            import logging as _elog
            runtime_card_path = Path(_P.DATA_FILES.CIELINGO_CARDS)
            with open(runtime_card_path, "a") as _f:
                _f.write(json.dumps(card, ensure_ascii=False) + "\n")
        except Exception as _e:
            import logging as _elog
            _elog.getLogger(__name__).debug("canonize_resolved_words: CIELingo cards JSONL write failed for %s: %s", card_id, _e)

        next_id += 1

    return {
        "n_canonized": len(written),
        "n_skipped_existing": skipped_existing,
        "card_ids": written,
    }


__all__ = [
    "SCHEMA",
    "UNKNOWN_AUDIT_VERSION",
    "UnknownWordAuditEntry",
    "UnknownCluster",
    "UnknownWordAuditReport",
    "load_unknown_candidate_cards",
    "classify_unknown_word",
    "audit_entry_from_card",
    "build_unknown_clusters",
    "collatz_learning_cycle",
    "audit_unknown_words",
    "resolve_source_lookup_queue",
    "canonize_resolved_words",
]
