"""CIELingo meaning-debt word-card scaffolder.

This module converts the previously identified CIEL-POL meaning-debt index into
supervised candidate word cards.  It deliberately does **not** promote the old
scaffolds to canon.  Every emitted word card receives a grammatical designation,
a sentence-function candidate, tensor/scalar semantic placeholders, and an
explicit confidence note.

Core rules:
* sequence numbers and source card ordinals are technical provenance only;
* the word itself carries potential and relational/contextual energy;
* each word must have a designation, even if the designation is only a low-
  confidence candidate;
* infinitives are separated first, then other parts of speech and sentence
  parts;
* candidates start at confidence 0.5 and require evidence + supervised review
  before canonization.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable, Mapping, Sequence

SCHEMA = "cielingo/meaning-debt-word-cards/v0.1"
CANDIDATE_CONFIDENCE = 0.5

from ciel_geometry.phasenav.metatime_contract import INFORMATION_KAPPA
KAPPA_INFO = INFORMATION_KAPPA

POLISH_LETTERS = set("ąćęłńóśźż")
WORD_RE = re.compile(r"^[0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż_-]+$")

CONJUNCTIONS = {
    "albo", "lub", "i", "oraz", "ani", "że", "czy", "gdy", "jeżeli", "jeśli",
    "ale", "lecz", "bo", "ponieważ", "więc", "zatem", "natomiast", "aby", "żeby",
}
PARTICLES = {"nie", "też", "tak", "no", "chyba", "tylko", "właśnie", "już", "aż", "nawet"}
PREPOSITIONS = {
    "w", "we", "na", "z", "ze", "do", "od", "po", "przy", "bez", "dla", "o",
    "u", "za", "pod", "nad", "przez", "między", "przed", "ku", "wobec", "według",
}
PRONOUNS = {
    "ja", "ty", "on", "ona", "ono", "my", "wy", "oni", "one", "mnie", "ciebie",
    "się", "siebie", "swój", "swoje", "ten", "ta", "to", "tamten", "który", "jaki",
    "co", "kto", "nic", "coś", "ktoś", "wszystko", "wszystkie", "sam", "samego",
}
MODAL_MARKERS = {
    "trzeba", "należy", "można", "może", "mogę", "musi", "muszę", "powinien",
    "powinna", "powinno", "wolno", "warto", "chcę", "zamierzam",
}
VERB_FORMS = {
    "jest", "są", "był", "była", "było", "będzie", "ma", "mają", "miał", "wymaga",
    "wymagają", "wykonuje", "zostało", "zostaje", "działa", "prowadzi",
}
# Infinitives ending in -ść are rare but real; most -ość/-ność words are nouns.
INFINITIVE_EXCEPTIONS = {"iść", "nieść", "wieść", "wieźć", "móc", "piec", "biec", "tłuc"}
ABSTRACT_NOUN_SUFFIXES = ("ość", "ność", "łość", "wość", "istość", "alność", "ywność")
INFINITIVE_SUFFIXES = ("ować", "ywać", "iwać", "awać", "ać", "eć", "ić", "yć", "nąć", "ąć")
NOUN_SUFFIXES = (
    "ość", "ność", "anie", "enie", "cja", "sja", "izm", "ka", "ek", "ść", "a", "e", "um",
    "acja", "encja", "stwo", "enie", "anie", "arz", "nik", "ność",
)
ADJECTIVE_SUFFIXES = ("owy", "owa", "owe", "ny", "na", "ne", "ski", "ska", "skie", "czy", "ego", "ej", "ych", "ymi")
ADVERB_SUFFIXES = ("o", "e", "nie")
VULGAR_SEED = {"kurwa", "chuj", "huj", "pierdol", "jeb", "dupa"}


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_word(text: str) -> str:
    text = unicodedata.normalize("NFKC", str(text)).strip().lower()
    return " ".join(text.split())


def stable_unit(text: str) -> float:
    digest = hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64 - 1)


def bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def sha256_json(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def card_id_for_word(lemma: str, source_card_id: str) -> str:
    digest = hashlib.sha256(f"{normalize_word(lemma)}|{source_card_id}|{SCHEMA}".encode("utf-8")).hexdigest()[:16]
    return f"CIEL-POL-WORD-CAND-{digest}"


def is_single_word(text: str) -> bool:
    t = normalize_word(text)
    return bool(t) and " " not in t and bool(WORD_RE.match(t))


def has_polish_signal(text: str) -> bool:
    t = normalize_word(text)
    return any(ch in POLISH_LETTERS for ch in t)


def debt_flags(row: Mapping[str, Any]) -> tuple[str, ...]:
    raw = str(row.get("debt_flags", ""))
    return tuple(x for x in raw.split(";") if x)


def lexical_unit_type(row: Mapping[str, Any]) -> str:
    lemma = normalize_word(row.get("lemma") or row.get("surface") or "")
    flags = set(debt_flags(row))
    if not lemma:
        return "empty_or_missing_surface"
    if not is_single_word(lemma):
        return "expression_or_multiword_unit"
    # ASCII alone is not evidence of foreignness: many Polish words have no
    # diacritics.  Only the explicit debt flag or strong project/runtime shapes
    # mark a surface as technical/non-Polish at this stage.
    if "surface_english_or_project_term" in flags:
        return "technical_or_non_polish_label_candidate"
    if re.search(r"[A-Z_:/]", str(row.get("surface", ""))) or lemma.startswith(("ciel", "noema", "htri", "cqcl")):
        return "technical_or_non_polish_label_candidate"
    return "single_word_candidate"


def is_polish_infinitive(lemma: str, row: Mapping[str, Any] | None = None) -> bool:
    word = normalize_word(lemma)
    if not word or lexical_unit_type(row or {"lemma": word}) != "single_word_candidate":
        return False
    if word.endswith("ąc"):
        return False
    if word in INFINITIVE_EXCEPTIONS:
        return True
    if word.endswith(ABSTRACT_NOUN_SUFFIXES):
        return False
    if word.endswith(INFINITIVE_SUFFIXES):
        return True
    # Bare -c infinitives exist, but avoid ASCII/project labels like topic/semantic.
    if word.endswith("c") and has_polish_signal(word):
        return True
    return False


def part_of_speech_candidate(row: Mapping[str, Any]) -> tuple[str, float, str]:
    lemma = normalize_word(row.get("lemma") or row.get("surface") or "")
    unit_type = lexical_unit_type(row)
    if unit_type == "empty_or_missing_surface":
        return "unknown", 0.0, "missing surface/lemma"
    if unit_type == "expression_or_multiword_unit":
        return "expression", 0.35, "surface is not a single word"
    if unit_type == "technical_or_non_polish_label_candidate":
        return "technical_label_or_foreign_word", 0.35, "debt index marks English/project/technical surface or weak Polish signal"
    if lemma in CONJUNCTIONS:
        return "conjunction", 0.75, "local closed-class seed"
    if lemma in PREPOSITIONS:
        return "preposition", 0.75, "local closed-class seed"
    if lemma in PARTICLES:
        return "particle", 0.70, "local closed-class seed"
    if lemma in PRONOUNS:
        return "pronoun", 0.70, "local closed-class seed"
    if lemma in MODAL_MARKERS:
        return "modal_operator", 0.68, "local modality seed"
    if is_polish_infinitive(lemma, row):
        return "verb_infinitive", 0.66, "Polish infinitive suffix/exception heuristic; requires dictionary verification"
    if lemma in VERB_FORMS or lemma.endswith(("uje", "ają", "esz", "isz", "ysz")):
        return "verb_form", 0.52, "finite verb-form heuristic; requires morphological verification"
    if lemma.endswith(ADJECTIVE_SUFFIXES):
        return "adjective_candidate", 0.46, "adjective ending heuristic"
    if lemma.endswith(NOUN_SUFFIXES):
        return "noun_candidate", 0.45, "noun ending heuristic"
    if lemma.endswith(ADVERB_SUFFIXES) and len(lemma) > 3:
        return "adverb_candidate", 0.40, "adverb ending heuristic"
    return "unknown_word_candidate", 0.30, "no reliable local grammatical evidence"


def sentence_part_candidate(part_of_speech: str) -> str:
    return {
        "verb_infinitive": "predicate_seed_or_complement",
        "verb_form": "predicate_candidate",
        "modal_operator": "modal_predicate_operator",
        "noun_candidate": "subject_or_object_candidate",
        "pronoun": "argument_or_deictic_candidate",
        "adjective_candidate": "attribute_modifier_candidate",
        "adverb_candidate": "adverbial_modifier_candidate",
        "conjunction": "clause_connector",
        "preposition": "case_relation_operator",
        "particle": "polarity_or_discourse_operator",
        "expression": "multiword_expression_pending_segmentation",
        "technical_label_or_foreign_word": "technical_label_pending_translation",
    }.get(part_of_speech, "unresolved_sentence_role")


def grammatical_designation(row: Mapping[str, Any]) -> dict[str, Any]:
    pos, confidence, rationale = part_of_speech_candidate(row)
    return {
        "lexical_unit_type": lexical_unit_type(row),
        "part_of_speech_candidate": pos,
        "part_of_speech_confidence": round(confidence, 6),
        "part_of_speech_rationale": rationale,
        "sentence_part_candidate": sentence_part_candidate(pos),
        "infinitive_status": "infinitive_candidate" if pos == "verb_infinitive" else "not_infinitive",
        "morphology_status": "heuristic_pending_morfeusz_sgjp_plwordnet_verification",
        "requires_human_grammar_review": True,
    }


def semantic_designation(row: Mapping[str, Any]) -> dict[str, Any]:
    lemma = normalize_word(row.get("lemma") or row.get("surface") or "")
    flags = debt_flags(row)
    flag_count = int(row.get("debt_flag_count") or len(flags) or 0)
    pos, pos_conf, _ = part_of_speech_candidate(row)
    base = stable_unit("word-potential|" + lemma)
    priority = bounded(0.28 + 0.04 * min(flag_count, 10) + (0.10 if pos == "verb_infinitive" else 0.0))
    emotional_intensity = bounded(0.15 + 0.65 * stable_unit("intensity|" + lemma))
    vulgar = any(seed in lemma for seed in VULGAR_SEED)
    if vulgar:
        colour = "vulgar_high_friction"
        register = "vulgar_or_profane_candidate"
        emotional_intensity = max(emotional_intensity, 0.82)
    elif pos == "conjunction":
        colour = "connector_neutral"
        register = "functional"
    elif pos == "modal_operator":
        colour = "modal_pressure"
        register = "functional_modal"
    elif pos == "verb_infinitive":
        colour = "action_potential"
        register = "lexical_action_seed"
    else:
        hue = int(stable_unit("colour|" + lemma) * 360)
        colour = f"candidate_hue_{hue:03d}"
        register = "unknown_pending_source_verification"
    viscosity_solo = bounded(0.20 + 0.35 * stable_unit("solo-viscosity|" + lemma) + 0.025 * flag_count)
    viscosity_group = bounded(0.18 + 0.35 * stable_unit("group-viscosity|" + lemma) + (0.18 if vulgar else 0.02 * flag_count))
    semantic_mass_rest = bounded(0.25 + 0.45 * base + 0.10 * pos_conf)
    potential_phi = semantic_mass_rest * KAPPA_INFO
    relation_energy = priority * (1.0 + emotional_intensity) * (0.5 + viscosity_group)
    return {
        "koto_mono_field": {
            "real_exchange_tensor_role": "word_can_exchange_information_in_relation",
            "imaginary_context_scalar_role": "word_context_affect_subtext_register",
        },
        "word_potential": round(potential_phi, 12),
        "semantic_rest_mass": round(semantic_mass_rest, 9),
        "relation_energy_proxy": round(relation_energy, 9),
        "colour": colour,
        "intensity": round(emotional_intensity, 9),
        "density_priority_weight": round(priority, 9),
        "viscosity_solo_subjective": round(viscosity_solo, 9),
        "viscosity_group_subjective": round(viscosity_group, 9),
        "register_candidate": register,
        "subtext_status": "unknown_pending_context_observation",
        "affective_note": "colour expresses emotion/register; intensity expresses force; density expresses priority/weight; viscosity expresses subjective solo/group friction",
    }


@dataclass(frozen=True)
class DebtWordRecord:
    source_card_id: str
    surface: str
    lemma: str
    source_file: str
    debt_flags: tuple[str, ...]
    debt_flag_count: int
    recommended_state: str

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "DebtWordRecord":
        flags = debt_flags(row)
        return cls(
            source_card_id=str(row.get("card_id", "")),
            surface=normalize_word(row.get("surface", "")),
            lemma=normalize_word(row.get("lemma") or row.get("surface") or ""),
            source_file=str(row.get("source_file", "")),
            debt_flags=flags,
            debt_flag_count=int(row.get("debt_flag_count") or len(flags) or 0),
            recommended_state=str(row.get("recommended_state", "")),
        )

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["debt_flags"] = list(self.debt_flags)
        return data


@dataclass(frozen=True)
class DebtCandidateWordCard:
    schema: str
    id: str
    card_id: str
    status: str
    confidence: float
    confidence_note: str
    surface: str
    lemma: str
    language: str
    source_debt_record: dict[str, Any]
    ordinal_semantics: dict[str, Any]
    grammatical_designation: dict[str, Any]
    semantic_designation: dict[str, Any]
    source_requirements: dict[str, Any]
    learning_policy: dict[str, Any]
    noema_tags: list[str]
    digest: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DebtWordCardsReport:
    schema: str
    created_at_utc: str
    source_index_path: str
    source_index_sha256: str
    total_records: int
    candidate_cards: int
    infinitive_cards: int
    part_of_speech_counts: dict[str, int]
    sentence_part_counts: dict[str, int]
    lexical_unit_type_counts: dict[str, int]
    confidence_floor: float
    external_verification_required: bool
    output_paths: dict[str, str]
    digest: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def read_debt_index(index_path: str | Path) -> list[DebtWordRecord]:
    path = Path(index_path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [DebtWordRecord.from_row(row) for row in csv.DictReader(handle)]


def build_candidate_card(record: DebtWordRecord) -> DebtCandidateWordCard:
    row = record.as_dict()
    row.update({
        "card_id": record.source_card_id,
        "debt_flags": ";".join(record.debt_flags),
        "debt_flag_count": record.debt_flag_count,
    })
    grammar = grammatical_designation(row)
    semantic = semantic_designation(row)
    cid = card_id_for_word(record.lemma, record.source_card_id)
    base_payload = {
        "schema": SCHEMA,
        "id": cid,
        "status": "candidate_0_5_from_meaning_debt_pending_sources_and_human_review",
        "confidence": CANDIDATE_CONFIDENCE,
        "surface": record.surface,
        "lemma": record.lemma,
        "grammar": grammar,
        "semantic": semantic,
        "source": record.as_dict(),
    }
    digest = sha256_json(base_payload)
    return DebtCandidateWordCard(
        schema=SCHEMA,
        id=cid,
        card_id=cid,
        status="candidate_0_5_from_meaning_debt_pending_sources_and_human_review",
        confidence=CANDIDATE_CONFIDENCE,
        confidence_note=(
            "Generated from meaning-debt scaffold. The word is marked, not canonized. "
            "Part-of-speech and sentence-part labels are local heuristics until open-source lexical/morphological evidence and supervised review confirm them."
        ),
        surface=record.surface,
        lemma=record.lemma,
        language="pl_candidate",
        source_debt_record=record.as_dict(),
        ordinal_semantics={
            "source_card_id_is_provenance_only": True,
            "filename_or_sequence_number_has_no_semantic_rank": True,
            "ordering_is_not_used_for_weight_potential_density_or_priority": True,
        },
        grammatical_designation=grammar,
        semantic_designation=semantic,
        source_requirements={
            "required_before_canon": ["Wiktionary/pl", "SGJP_or_Morfeusz", "plWordNet_or_manual_relation_review"],
            "current_external_evidence_status": "not_verified_in_this_patch",
            "meaning_debt_gate": "WORD_CARD_PASS_FALSE_UNTIL_RESOLVED",
        },
        learning_policy={
            "initial_confidence": CANDIDATE_CONFIDENCE,
            "may_enter_runtime_as": "supervised_candidate_surface",
            "may_be_revalued_by": ["source_evidence", "usage_observation", "human_review", "NOEMA_recall"],
            "auto_canonization_allowed": False,
            "append_only_updates_required": True,
        },
        noema_tags=[
            "cielingo",
            "meaning_debt",
            "word_candidate",
            grammar["part_of_speech_candidate"],
            grammar["sentence_part_candidate"],
        ],
        digest=digest,
    )


def build_candidate_cards(records: Iterable[DebtWordRecord]) -> list[DebtCandidateWordCard]:
    return [build_candidate_card(record) for record in records if record.lemma]


def _write_jsonl(path: Path, items: Iterable[Mapping[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def _counts(cards: Sequence[DebtCandidateWordCard], key_path: Sequence[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for card in cards:
        obj: Any = card.as_dict()
        for key in key_path:
            obj = obj[key]
        out[str(obj)] = out.get(str(obj), 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))


def generate_debt_word_cards(
    index_path: str | Path,
    *,
    output_dir: str | Path,
    source_label: str = "ciel_pol_meaning_debt_cards_bundle",
) -> DebtWordCardsReport:
    index_display = str(Path(index_path))
    output_display = Path(output_dir)
    index = Path(index_path).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    records = read_debt_index(index)
    cards = build_candidate_cards(records)
    inf_cards = [c for c in cards if c.grammatical_designation["part_of_speech_candidate"] == "verb_infinitive"]
    non_inf_cards = [c for c in cards if c.grammatical_designation["part_of_speech_candidate"] != "verb_infinitive"]

    all_path = out / "word_candidate_cards.jsonl"
    inf_path = out / "infinitive_candidate_cards.jsonl"
    other_path = out / "other_pos_candidate_cards.jsonl"
    by_pos_dir = out / "by_part_of_speech"
    by_pos_dir.mkdir(exist_ok=True)

    _write_jsonl(all_path, (c.as_dict() for c in cards))
    _write_jsonl(inf_path, (c.as_dict() for c in inf_cards))
    _write_jsonl(other_path, (c.as_dict() for c in non_inf_cards))
    for pos in sorted({c.grammatical_designation["part_of_speech_candidate"] for c in cards}):
        subset = [c for c in cards if c.grammatical_designation["part_of_speech_candidate"] == pos]
        _write_jsonl(by_pos_dir / f"{pos}.jsonl", (c.as_dict() for c in subset))

    source_sha = hashlib.sha256(index.read_bytes()).hexdigest()
    paths = {
        "all_cards_jsonl": str(output_display / "word_candidate_cards.jsonl"),
        "infinitive_cards_jsonl": str(output_display / "infinitive_candidate_cards.jsonl"),
        "other_pos_cards_jsonl": str(output_display / "other_pos_candidate_cards.jsonl"),
        "by_part_of_speech_dir": str(output_display / "by_part_of_speech"),
    }
    payload = {
        "schema": SCHEMA,
        "source_label": source_label,
        "source_index_sha256": source_sha,
        "total_records": len(records),
        "candidate_cards": len(cards),
        "infinitive_cards": len(inf_cards),
        "part_of_speech_counts": _counts(cards, ("grammatical_designation", "part_of_speech_candidate")),
        "sentence_part_counts": _counts(cards, ("grammatical_designation", "sentence_part_candidate")),
        "lexical_unit_type_counts": _counts(cards, ("grammatical_designation", "lexical_unit_type")),
        "paths": paths,
    }
    digest = sha256_json(payload)
    report = DebtWordCardsReport(
        schema=SCHEMA,
        created_at_utc=utc_now(),
        source_index_path=index_display,
        source_index_sha256=source_sha,
        total_records=len(records),
        candidate_cards=len(cards),
        infinitive_cards=len(inf_cards),
        part_of_speech_counts=payload["part_of_speech_counts"],
        sentence_part_counts=payload["sentence_part_counts"],
        lexical_unit_type_counts=payload["lexical_unit_type_counts"],
        confidence_floor=CANDIDATE_CONFIDENCE,
        external_verification_required=True,
        output_paths=paths,
        digest=digest,
    )
    report_path = out / "meaning_debt_word_cards_report.json"
    report_path.write_text(json.dumps(report.as_dict(), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return report
