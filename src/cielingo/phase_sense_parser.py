"""CIELingo phase-sense parser.

This layer parses surface words into phase-sense objects before output
inference consumes them.  It is intentionally local and deterministic:

* token -> own CIELingo/NOEMA language-card match;
* matched card -> 24D vector + tensor-scalar context field;
* unknown token -> guarded candidate phase with explicit low confidence;
* every token carries a phase-sense note for supervised grammar repair.

The parser does not overwrite cards, does not claim external dictionary proof,
and does not perform external NOEMA SoT writeback.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable, Mapping

from .lexical_holonomy import (
    WordKnowledgeNote,
    build_word_knowledge_notes,
    extract_lexical_units,
)
from .lns_language_cards import LNSLanguageCard, load_all_language_cards, search_language_cards
from .tensor_scalar_field import TensorScalarWordState, tensor_scalar_state_from_card
from .vector_surface import CIELingoVector, VECTOR_DIM, vectorize_card

PHASE_SENSE_SCHEMA = "cielingo/phase-sense-parser/v0.1"
TOKEN_RE = re.compile(r"[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", re.UNICODE)


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).strip().lower()
    return " ".join(text.split())


def _stable_unit(text: str) -> float:
    digest = hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64 - 1)


def _phase(text: str) -> float:
    return round(_stable_unit("phase|" + text) * 2.0 * math.pi, 9)


def _digest_payload(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def tokenize_surface(text: str) -> list[str]:
    """Tokenize surface text without importing a heavyweight NLP stack."""
    return [m.group(0) for m in TOKEN_RE.finditer(text)]


@dataclass(frozen=True)
class PhaseSenseToken:
    """One word parsed into a phase-sense state."""

    schema: str
    position: int
    surface: str
    normalized: str
    language_hint: str | None
    matched: bool
    card_id: str | None
    card_kind: str | None
    canonical_label: str | None
    source_path: str | None
    lexical_id: str | None
    semantic_axes: list[str]
    semantic_mass: float
    phase_rad: float
    phase_sense_label: str
    vector_digest: str | None
    field_digest: str | None
    tensor_trace: float | None
    scalar_density: float
    scalar_viscosity: float
    scalar_saturation: float
    semantic_time_resistance: float
    semantic_time_thinning: float
    knowledge_confidence: float
    confidence_note: str
    parse_status: str
    supervision_required: bool
    suggested_repair: str | None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PhaseSenseReport:
    """Aggregate parse result for a text sample."""

    schema: str
    source_role: str
    epistemic_status: str
    input_text_sha256: str
    language_hint: str | None
    token_count: int
    matched_token_count: int
    unknown_token_count: int
    matched_ratio: float
    mean_semantic_mass: float
    mean_density: float
    mean_viscosity: float
    mean_saturation: float
    mean_semantic_time_resistance: float
    mean_semantic_time_thinning: float
    mean_knowledge_confidence: float
    dominant_phase_rad: float
    phase_sense_digest: str
    tokens: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _card_index(repo_root: str | Path = ".") -> dict[tuple[str, str], LNSLanguageCard]:
    return {(card.card_id, card.source_path): card for card in load_all_language_cards(repo_root)}


def _note_index(repo_root: str | Path = ".") -> dict[str, list[WordKnowledgeNote]]:
    out: dict[str, list[WordKnowledgeNote]] = {}
    for note in build_word_knowledge_notes(repo_root):
        out.setdefault(note.lexical_id, []).append(note)
    return out


def _best_note(notes: Iterable[WordKnowledgeNote]) -> WordKnowledgeNote | None:
    items = list(notes)
    if not items:
        return None
    return max(items, key=lambda n: (n.knowledge_confidence, n.relation_count, n.local_evidence_count))


def _match_token(
    token: str,
    *,
    repo_root: str | Path,
    language_hint: str | None,
    cards: Mapping[tuple[str, str], LNSLanguageCard],
) -> tuple[LNSLanguageCard | None, str | None, str | None]:
    """Return matched card plus lexical id/source status for a token."""
    q = _norm(token)
    # Prefer exact own-card lexical units over fuzzy search hits, but do not let
    # antonym/back-reference forms steal the primary lemma.
    role_priority = {
        "lemma": 0,
        "form_variant": 1,
        "near_synonym": 2,
        "synonym": 2,
        "example": 3,
        "antonym": 9,
    }
    exact_candidates = []
    for unit in extract_lexical_units(repo_root):
        if language_hint and unit.language != language_hint:
            continue
        if q in {_norm(unit.surface), _norm(unit.lemma)}:
            card = cards.get((unit.card_id, unit.source_path))
            if card is not None:
                exact_candidates.append((role_priority.get(unit.role, 5), unit.role, unit.card_id, unit, card))
    if exact_candidates:
        _prio, _role, _cid, unit, card = sorted(exact_candidates, key=lambda x: x[:3])[0]
        return card, unit.lexical_id, "own_card_exact"
    # Fall back to NOEMA/LNS surface search.
    hits = search_language_cards(token, repo_root, limit=8)
    if language_hint:
        hits = [h for h in hits if language_hint in h.get("languages", {})] or hits
    for hit in hits:
        card = cards.get((str(hit["card_id"]), str(hit["source_path"])))
        if card is not None:
            return card, None, "noema_lns_surface_search"
    return None, None, None


def phase_sense_for_token(
    token: str,
    *,
    position: int,
    repo_root: str | Path = ".",
    language_hint: str | None = None,
    cards: Mapping[tuple[str, str], LNSLanguageCard] | None = None,
    notes: Mapping[str, list[WordKnowledgeNote]] | None = None,
) -> PhaseSenseToken:
    """Parse one token into a phase-sense token."""
    card_map = cards if cards is not None else _card_index(repo_root)
    note_map = notes if notes is not None else _note_index(repo_root)
    card, lexical_id, match_status = _match_token(token, repo_root=repo_root, language_hint=language_hint, cards=card_map)
    norm = _norm(token)
    if card is None:
        phase = _phase(f"unknown|{language_hint or '*'}|{norm}")
        density = round(0.18 + 0.22 * _stable_unit("density|" + norm), 9)
        viscosity = round(0.55 + 0.30 * _stable_unit("viscosity|" + norm), 9)
        saturation = round(0.12 + 0.18 * _stable_unit("saturation|" + norm), 9)
        resistance = round(min(1.0, density * (0.75 + viscosity) * (0.65 + saturation) + 0.18), 9)
        thinning = round(max(0.0, 0.18 * (1.0 - resistance)), 9)
        return PhaseSenseToken(
            schema=PHASE_SENSE_SCHEMA,
            position=position,
            surface=token,
            normalized=norm,
            language_hint=language_hint,
            matched=False,
            card_id=None,
            card_kind=None,
            canonical_label=None,
            source_path=None,
            lexical_id=None,
            semantic_axes=[],
            semantic_mass=0.0,
            phase_rad=phase,
            phase_sense_label="unknown_surface_candidate_phase",
            vector_digest=None,
            field_digest=None,
            tensor_trace=None,
            scalar_density=density,
            scalar_viscosity=viscosity,
            scalar_saturation=saturation,
            semantic_time_resistance=resistance,
            semantic_time_thinning=thinning,
            knowledge_confidence=0.0,
            confidence_note="Unknown to local CIELingo card surface; needs supervised card or external lexical evidence.",
            parse_status="unmatched_needs_supervised_language_card",
            supervision_required=True,
            suggested_repair="create_or_link_language_card_under_supervision",
        )

    vector: CIELingoVector = vectorize_card(card)
    field: TensorScalarWordState = tensor_scalar_state_from_card(card)
    note = _best_note(note_map.get(lexical_id or "", []))
    if note is not None:
        confidence = float(note.knowledge_confidence)
        confidence_note = note.confidence_note
    else:
        confidence = float(field.knowledge_confidence)
        confidence_note = "Matched through CIELingo card; no exact per-word note attached to this token."
    return PhaseSenseToken(
        schema=PHASE_SENSE_SCHEMA,
        position=position,
        surface=token,
        normalized=norm,
        language_hint=language_hint,
        matched=True,
        card_id=card.card_id,
        card_kind=card.card_kind,
        canonical_label=card.canonical_label,
        source_path=card.source_path,
        lexical_id=lexical_id,
        semantic_axes=list(card.semantic_axes),
        semantic_mass=round(float(card.semantic_mass), 9),
        phase_rad=round(float(card.phase_rad), 9),
        phase_sense_label="card_bound_phase_sense",
        vector_digest=vector.vector_digest,
        field_digest=str(field.noema_document["field_digest"]),
        tensor_trace=field.tensor_trace,
        scalar_density=field.scalar_context.density,
        scalar_viscosity=field.scalar_context.viscosity,
        scalar_saturation=field.scalar_context.saturation,
        semantic_time_resistance=field.scalar_context.semantic_time_resistance,
        semantic_time_thinning=field.scalar_context.semantic_time_thinning,
        knowledge_confidence=round(confidence, 9),
        confidence_note=confidence_note,
        parse_status=match_status or "matched",
        supervision_required=confidence < 0.62,
        suggested_repair="external_verify_or_supervised_grammar_review" if confidence < 0.62 else None,
    )


def parse_text_to_phase_sense(
    text: str,
    repo_root: str | Path = ".",
    *,
    language_hint: str | None = "pl",
) -> dict[str, Any]:
    """Parse text into phase-sense tokens and aggregate scalar/phase metrics."""
    tokens = tokenize_surface(text)
    cards = _card_index(repo_root)
    notes = _note_index(repo_root)
    parsed = [
        phase_sense_for_token(
            tok,
            position=i,
            repo_root=repo_root,
            language_hint=language_hint,
            cards=cards,
            notes=notes,
        )
        for i, tok in enumerate(tokens)
    ]
    count = len(parsed)
    matched = sum(1 for t in parsed if t.matched)

    def mean(attr: str) -> float:
        if not parsed:
            return 0.0
        return round(sum(float(getattr(t, attr)) for t in parsed) / len(parsed), 9)

    sin_sum = sum(math.sin(t.phase_rad) for t in parsed)
    cos_sum = sum(math.cos(t.phase_rad) for t in parsed)
    dominant = math.atan2(sin_sum, cos_sum) if parsed else 0.0
    if dominant < 0:
        dominant += 2.0 * math.pi
    digest_payload = [
        {
            "position": t.position,
            "surface": t.surface,
            "card_id": t.card_id,
            "phase": t.phase_rad,
            "field_digest": t.field_digest,
        }
        for t in parsed
    ]
    report = PhaseSenseReport(
        schema="cielingo/phase-sense-report/v0.1",
        source_role="local_cielingo_word_to_phase_sense_parser",
        epistemic_status="local parser over own language cards; unknown words remain supervised candidates",
        input_text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        language_hint=language_hint,
        token_count=count,
        matched_token_count=matched,
        unknown_token_count=count - matched,
        matched_ratio=round(matched / count, 9) if count else 0.0,
        mean_semantic_mass=mean("semantic_mass"),
        mean_density=mean("scalar_density"),
        mean_viscosity=mean("scalar_viscosity"),
        mean_saturation=mean("scalar_saturation"),
        mean_semantic_time_resistance=mean("semantic_time_resistance"),
        mean_semantic_time_thinning=mean("semantic_time_thinning"),
        mean_knowledge_confidence=mean("knowledge_confidence"),
        dominant_phase_rad=round(dominant, 9),
        phase_sense_digest=_digest_payload(digest_payload),
        tokens=[t.as_dict() for t in parsed],
    )
    return report.as_dict()


def write_phase_sense_report(path: str | Path, report: Mapping[str, Any]) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


__all__ = [
    "PHASE_SENSE_SCHEMA",
    "PhaseSenseToken",
    "PhaseSenseReport",
    "tokenize_surface",
    "phase_sense_for_token",
    "parse_text_to_phase_sense",
    "write_phase_sense_report",
]
