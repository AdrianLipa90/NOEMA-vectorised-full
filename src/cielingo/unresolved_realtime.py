"""CIELingo real-time unresolved-word protocol.

This module turns unknown phase-sense tokens into an append-only unresolved
stream and, when local source evidence is available, creates supervised
candidate word cards with initial confidence 0.5.

Design constraints:
* no automatic canonization;
* no network access or live external claims;
* card sequence numbers and filenames are technical only;
* every candidate carries potential, relation energy and scalar context notes;
* learning is revaluation over evidence, not silent overwrite.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable, Mapping, Sequence

from .phase_sense_parser import parse_text_to_phase_sense

UNRESOLVED_SCHEMA = "cielingo/unresolved-realtime/v0.1"
CANDIDATE_SCHEMA = "cielingo/word-candidate-card/v0.1"
DEFAULT_RUNTIME_REL = Path("runtime/cielingo/unresolved")
DEFAULT_EVIDENCE_REL = Path("data/cielingo/source_evidence")
CANDIDATE_CONFIDENCE = 0.5
KAPPA_INFO = math.log(2.0) / (24.0 * math.pi)
WORD_RE = re.compile(r"[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", re.UNICODE)


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_utc() -> str:
    return dt.datetime.now(dt.UTC).date().isoformat()


def normalize_word(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).strip().lower()
    return " ".join(text.split())


def stable_unit(text: str) -> float:
    digest = hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64 - 1)


def sha256_json(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def safe_slug(text: str) -> str:
    norm = normalize_word(text)
    norm = re.sub(r"[^0-9a-ząćęłńóśźż_-]+", "_", norm, flags=re.IGNORECASE).strip("_")
    return norm or "unknown"


@dataclass(frozen=True)
class UnresolvedWordEvent:
    schema: str
    event_id: str
    observed_at_utc: str
    surface: str
    normalized: str
    language_hint: str | None
    source_role: str
    input_text_sha256: str
    token_position: int
    local_parse_status: str
    phase_rad: float
    scalar_density: float
    scalar_viscosity: float
    scalar_saturation: float
    semantic_time_resistance: float
    context_before: str
    context_after: str
    status: str
    candidate_card_id: str | None
    confidence_floor: float
    supervision_required: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceEvidence:
    source_id: str
    source_kind: str
    source_name: str
    license_hint: str
    retrieval_mode: str
    lemma: str
    language: str | None
    definition: str
    part_of_speech: str | None
    synonyms: tuple[str, ...]
    antonyms: tuple[str, ...]
    register: str | None
    emotional_colour: str | None
    emotional_intensity: float | None
    evidence_confidence: float
    evidence_digest: str

    def as_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["synonyms"] = list(self.synonyms)
        out["antonyms"] = list(self.antonyms)
        return out


@dataclass(frozen=True)
class CandidateWordCard:
    schema: str
    card_id: str
    status: str
    surface: str
    lemma: str
    language: str | None
    created_at_utc: str
    confidence: float
    confidence_note: str
    source_evidence: list[dict[str, Any]]
    meaning_candidate: dict[str, Any]
    scalar_context: dict[str, float | str]
    potential: dict[str, float]
    relation_energy: dict[str, float | str]
    lexical_relations: dict[str, list[str]]
    correction_policy: str
    learning_policy: str
    noema_payload: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RealtimeUnresolvedReport:
    schema: str
    created_at_utc: str
    input_text_sha256: str
    token_count: int
    unresolved_count: int
    candidate_count: int
    unresolved_event_paths: list[str]
    candidate_card_paths: list[str]
    daily_dump_path: str
    report_digest: str
    notes: list[str]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def runtime_root(repo_root: str | Path = ".") -> Path:
    return Path(repo_root).resolve() / DEFAULT_RUNTIME_REL


def evidence_root(repo_root: str | Path = ".") -> Path:
    return Path(repo_root).resolve() / DEFAULT_EVIDENCE_REL


def _jsonl_records(paths: Iterable[Path]) -> Iterable[dict[str, Any]]:
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                yield json.loads(line)


def load_source_evidence(repo_root: str | Path = ".") -> list[SourceEvidence]:
    """Load local source-evidence descriptors.

    The repo may contain downloaded/open-source dictionary extracts later. This
    function only reads local JSONL; it never fetches from the network.
    """
    base = evidence_root(repo_root)
    paths = sorted(base.glob("*.jsonl"))
    evidence: list[SourceEvidence] = []
    for raw in _jsonl_records(paths):
        lemma = normalize_word(str(raw.get("lemma") or raw.get("surface") or ""))
        definition = str(raw.get("definition") or raw.get("meaning") or "").strip()
        if not lemma or not definition:
            continue
        source_id = str(raw.get("source_id") or raw.get("source_name") or "local_source")
        digest_payload = {k: raw.get(k) for k in sorted(raw)}
        evidence.append(
            SourceEvidence(
                source_id=source_id,
                source_kind=str(raw.get("source_kind", "open_source_descriptor")),
                source_name=str(raw.get("source_name", source_id)),
                license_hint=str(raw.get("license_hint", "unknown_check_before_canon")),
                retrieval_mode=str(raw.get("retrieval_mode", "local_jsonl_no_network")),
                lemma=lemma,
                language=str(raw.get("language")) if raw.get("language") else None,
                definition=definition,
                part_of_speech=str(raw.get("part_of_speech")) if raw.get("part_of_speech") else None,
                synonyms=tuple(normalize_word(str(x)) for x in raw.get("synonyms", []) if str(x).strip()),
                antonyms=tuple(normalize_word(str(x)) for x in raw.get("antonyms", []) if str(x).strip()),
                register=str(raw.get("register")) if raw.get("register") else None,
                emotional_colour=str(raw.get("emotional_colour")) if raw.get("emotional_colour") else None,
                emotional_intensity=float(raw.get("emotional_intensity", 0.0)) if raw.get("emotional_intensity") is not None else None,
                evidence_confidence=float(raw.get("evidence_confidence", 0.5)),
                evidence_digest=hashlib.sha256(json.dumps(digest_payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest(),
            )
        )
    return evidence


def source_candidates_for_word(
    word: str,
    repo_root: str | Path = ".",
    *,
    language_hint: str | None = None,
) -> list[SourceEvidence]:
    norm = normalize_word(word)
    out: list[SourceEvidence] = []
    for ev in load_source_evidence(repo_root):
        if language_hint and ev.language and ev.language != language_hint:
            continue
        forms = {ev.lemma, *ev.synonyms}
        if norm in forms:
            out.append(ev)
    return sorted(out, key=lambda e: (e.evidence_confidence, e.source_name), reverse=True)


def _context_window(tokens: Sequence[str], pos: int, radius: int = 4) -> tuple[str, str]:
    before = " ".join(tokens[max(0, pos - radius):pos])
    after = " ".join(tokens[pos + 1:pos + 1 + radius])
    return before, after


def unresolved_events_from_text(
    text: str,
    repo_root: str | Path = ".",
    *,
    language_hint: str | None = "pl",
    source_role: str = "runtime_text_sample",
) -> list[UnresolvedWordEvent]:
    report = parse_text_to_phase_sense(text, repo_root, language_hint=language_hint)
    tokens = [str(t.get("surface", "")) for t in report.get("tokens", [])]
    out: list[UnresolvedWordEvent] = []
    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    now = utc_now()
    for tok in report.get("tokens", []):
        if tok.get("matched"):
            continue
        surface = str(tok.get("surface", ""))
        norm = normalize_word(surface)
        pos = int(tok.get("position", 0))
        before, after = _context_window(tokens, pos)
        event_base = {
            "surface": surface,
            "normalized": norm,
            "language_hint": language_hint,
            "input_text_sha256": text_hash,
            "token_position": pos,
            "source_role": source_role,
        }
        event_id = "unresolved:" + sha256_json(event_base)[:24]
        out.append(
            UnresolvedWordEvent(
                schema=UNRESOLVED_SCHEMA,
                event_id=event_id,
                observed_at_utc=now,
                surface=surface,
                normalized=norm,
                language_hint=language_hint,
                source_role=source_role,
                input_text_sha256=text_hash,
                token_position=pos,
                local_parse_status=str(tok.get("parse_status", "unknown")),
                phase_rad=float(tok.get("phase_rad", 0.0)),
                scalar_density=float(tok.get("scalar_density", 0.0)),
                scalar_viscosity=float(tok.get("scalar_viscosity", 0.0)),
                scalar_saturation=float(tok.get("scalar_saturation", 0.0)),
                semantic_time_resistance=float(tok.get("semantic_time_resistance", 0.0)),
                context_before=before,
                context_after=after,
                status="unresolved_observed_realtime",
                candidate_card_id=None,
                confidence_floor=0.0,
                supervision_required=True,
            )
        )
    return out


def _append_jsonl(path: Path, records: Iterable[Mapping[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("a", encoding="utf-8") as handle:
        for rec in records:
            handle.write(json.dumps(dict(rec), sort_keys=True, ensure_ascii=False) + "\n")
            count += 1
    return count


def _candidate_card_id(word: str, language_hint: str | None, evidence: Sequence[SourceEvidence]) -> str:
    payload = {
        "word": normalize_word(word),
        "language": language_hint,
        "evidence": [e.evidence_digest for e in evidence],
        "schema": CANDIDATE_SCHEMA,
    }
    return "cielingo:candidate:" + sha256_json(payload)[:24]


def _source_summary(evidence: Sequence[SourceEvidence]) -> str:
    if not evidence:
        return "No local source evidence; keep unresolved and do not create candidate card."
    names = ", ".join(dict.fromkeys(e.source_name for e in evidence))
    return f"Candidate assembled from local source evidence descriptors: {names}. Confidence fixed at 0.5 pending review."


def build_candidate_word_card(
    event: UnresolvedWordEvent,
    evidence: Sequence[SourceEvidence],
) -> CandidateWordCard | None:
    """Build a supervised candidate card when evidence exists.

    Returns None if no local evidence is available. This prevents the system
    from hallucinating definitions solely from surface form.
    """
    if not evidence:
        return None
    lemma = evidence[0].lemma or event.normalized
    definitions = [e.definition for e in evidence[:5]]
    synonyms = sorted({x for e in evidence for x in e.synonyms})
    antonyms = sorted({x for e in evidence for x in e.antonyms})
    colour = evidence[0].emotional_colour or "neutral_unknown"
    intensity_vals = [e.emotional_intensity for e in evidence if e.emotional_intensity is not None]
    intensity = sum(float(x) for x in intensity_vals) / len(intensity_vals) if intensity_vals else 0.0
    # Density is priority/weight; unresolved words with external evidence are
    # important enough to be learned, but still non-canonical.
    density = min(1.0, max(0.5, event.scalar_density + 0.18 + 0.04 * min(5, len(evidence))))
    # Viscosity remains subjective and is split into solo/group estimates.
    viscosity_solo = min(1.0, max(0.0, event.scalar_viscosity))
    viscosity_group = min(1.0, max(0.0, event.scalar_viscosity + 0.08 * len(set(e.source_name for e in evidence))))
    saturation = min(1.0, max(event.scalar_saturation, 0.28 + 0.04 * len(definitions)))
    semantic_mass_rest = round(density * (0.65 + saturation) * (0.75 + 0.25 * CANDIDATE_CONFIDENCE), 9)
    potential_phi = round(semantic_mass_rest * KAPPA_INFO, 12)
    relation_energy = round(semantic_mass_rest * (1.0 + viscosity_solo + viscosity_group) * (0.5 + intensity), 9)
    card_id = _candidate_card_id(event.normalized, event.language_hint, evidence)
    noema_payload = {
        "source": "cielingo_realtime_unresolved_checker",
        "status": "candidate_only_not_canon",
        "event_id": event.event_id,
        "word_digest": hashlib.sha256(event.normalized.encode("utf-8")).hexdigest(),
        "source_evidence_digests": [e.evidence_digest for e in evidence],
    }
    return CandidateWordCard(
        schema=CANDIDATE_SCHEMA,
        card_id=card_id,
        status="candidate_0_5_pending_supervised_review",
        surface=event.surface,
        lemma=lemma,
        language=event.language_hint,
        created_at_utc=utc_now(),
        confidence=CANDIDATE_CONFIDENCE,
        confidence_note=_source_summary(evidence),
        source_evidence=[e.as_dict() for e in evidence],
        meaning_candidate={
            "definitions": definitions,
            "part_of_speech_candidates": sorted({e.part_of_speech for e in evidence if e.part_of_speech}),
            "register_candidates": sorted({e.register for e in evidence if e.register}),
            "review_required": True,
        },
        scalar_context={
            "colour": colour,
            "intensity": round(float(intensity), 9),
            "density_priority_weight": round(float(density), 9),
            "viscosity_solo_subjective": round(float(viscosity_solo), 9),
            "viscosity_group_subjective": round(float(viscosity_group), 9),
            "saturation": round(float(saturation), 9),
        },
        potential={
            "kappa_info_ln2_over_24pi": round(KAPPA_INFO, 12),
            "semantic_rest_mass_seed": semantic_mass_rest,
            "potential_phi": potential_phi,
        },
        relation_energy={
            "model": "semantic_linguistic_nbody_proxy",
            "energy": relation_energy,
            "note": "Candidate relation energy; revalue after repeated use, source agreement and human corrections.",
        },
        lexical_relations={
            "near_synonyms": synonyms,
            "antonyms": antonyms,
        },
        correction_policy="suggest_only_under_human_supervision_no_auto_canon",
        learning_policy="append observations; revalue confidence and scalar field over time; promote only after evidence+review gate",
        noema_payload={**noema_payload, "candidate_digest": sha256_json(noema_payload)},
    )


def candidate_path_for_card(repo_root: str | Path, card: CandidateWordCard, date: str | None = None) -> Path:
    day = date or today_utc()
    return runtime_root(repo_root) / "candidate_cards" / day / f"{safe_slug(card.lemma)}__{card.card_id.split(':')[-1]}.candidate.json"


def record_realtime_unresolved(
    text: str,
    repo_root: str | Path = ".",
    *,
    language_hint: str | None = "pl",
    source_role: str = "runtime_text_sample",
    create_candidates: bool = True,
) -> dict[str, Any]:
    """Append unresolved events and optional 0.5 candidate cards in real time."""
    root = runtime_root(repo_root)
    day = today_utc()
    events = unresolved_events_from_text(text, repo_root, language_hint=language_hint, source_role=source_role)
    event_records = [e.as_dict() for e in events]
    unresolved_path = root / "unresolved.jsonl"
    daily_path = root / "daily" / f"{day}.unresolved.jsonl"
    _append_jsonl(unresolved_path, event_records)
    _append_jsonl(daily_path, event_records)

    candidate_paths: list[str] = []
    candidate_count = 0
    if create_candidates:
        for event in events:
            evidence = source_candidates_for_word(event.normalized, repo_root, language_hint=language_hint)
            card = build_candidate_word_card(event, evidence)
            if card is None:
                continue
            cpath = candidate_path_for_card(repo_root, card, date=day)
            cpath.parent.mkdir(parents=True, exist_ok=True)
            cpath.write_text(json.dumps(card.as_dict(), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
            candidate_paths.append(str(cpath.relative_to(Path(repo_root).resolve())))
            candidate_count += 1

    digest_payload = {
        "input": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "events": [e.event_id for e in events],
        "candidates": candidate_paths,
    }
    report = RealtimeUnresolvedReport(
        schema="cielingo/realtime-unresolved-report/v0.1",
        created_at_utc=utc_now(),
        input_text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        token_count=len(WORD_RE.findall(text)),
        unresolved_count=len(events),
        candidate_count=candidate_count,
        unresolved_event_paths=[str(unresolved_path.relative_to(Path(repo_root).resolve())), str(daily_path.relative_to(Path(repo_root).resolve()))],
        candidate_card_paths=candidate_paths,
        daily_dump_path=str(daily_path.relative_to(Path(repo_root).resolve())),
        report_digest=sha256_json(digest_payload),
        notes=[
            "Realtime unresolved recording is append-only.",
            "Candidate cards start at confidence 0.5 only when local source evidence exists.",
            "No candidate is canonical; promotion requires evidence and human/supervised review.",
        ],
    )
    report_path = root / "reports" / f"realtime_unresolved_{day}.report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report.as_dict(), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return report.as_dict()


def daily_unresolved_rollup(repo_root: str | Path = ".", *, date: str | None = None) -> dict[str, Any]:
    """Produce a deterministic daily rollup without deleting raw events."""
    root = runtime_root(repo_root)
    day = date or today_utc()
    daily_path = root / "daily" / f"{day}.unresolved.jsonl"
    events = list(_jsonl_records([daily_path]))
    by_word: dict[str, list[dict[str, Any]]] = {}
    for ev in events:
        by_word.setdefault(str(ev.get("normalized", "")), []).append(ev)
    words = []
    for word, items in sorted(by_word.items()):
        evidence = source_candidates_for_word(word, repo_root)
        words.append(
            {
                "word": word,
                "count": len(items),
                "first_event_id": items[0].get("event_id"),
                "source_evidence_count": len(evidence),
                "candidate_ready": bool(evidence),
                "latest_status": items[-1].get("status"),
            }
        )
    rollup = {
        "schema": "cielingo/daily-unresolved-rollup/v0.1",
        "date": day,
        "event_count": len(events),
        "unique_unresolved_count": len(words),
        "candidate_ready_count": sum(1 for w in words if w["candidate_ready"]),
        "words": words,
        "append_only": True,
        "daily_dump_path": str(daily_path.relative_to(Path(repo_root).resolve())) if daily_path.exists() else str(daily_path),
    }
    rollup["rollup_digest"] = sha256_json(rollup)
    out = root / "daily" / f"{day}.rollup.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rollup, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return rollup


__all__ = [
    "UNRESOLVED_SCHEMA",
    "CANDIDATE_SCHEMA",
    "CANDIDATE_CONFIDENCE",
    "UnresolvedWordEvent",
    "SourceEvidence",
    "CandidateWordCard",
    "RealtimeUnresolvedReport",
    "normalize_word",
    "load_source_evidence",
    "source_candidates_for_word",
    "unresolved_events_from_text",
    "build_candidate_word_card",
    "record_realtime_unresolved",
    "daily_unresolved_rollup",
]
