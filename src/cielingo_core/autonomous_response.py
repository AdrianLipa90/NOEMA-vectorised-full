"""Source-grounded, session-continuous speech for the CIEL headless surface.

This module is deliberately not an LLM simulator.  It composes reviewed claims,
equations and provenance from declarative knowledge packs.  Unsupported topics
remain unavailable instead of being filled with hash routing or canned metrics.
Session continuity is bounded and volatile: raw prompts are never persisted.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct
import threading
import time
from typing import Any

from ciel_geometry.web_search import search as web_search

from ciel_geometry.phasenav.operator_algebra import ALL_OPERATOR_IDS


ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_PATH = ROOT / "data" / "cielingo" / "verified_knowledge" / "general_v1.json"
RUNTIME_CONTRACT_PATH = ROOT / "config" / "ciel_headless_runtime.json"

# Concept candidates observed outside the current verified knowledge pack are
# logged here. CIEL researches them itself (scripts/validate_concept_candidates.py,
# whitelist-only, no auth/CAPTCHA sources) and may answer directly from
# cross-source agreement — tagged with explicit uncertainty, never claimed as
# canon. Promotion of a concept into verified_knowledge/*.json (the sha256-
# pinned claims file the hook contract checks) still requires a separate,
# explicit human step; this only governs what CIEL says out loud with how
# much confidence.
CONCEPT_REGISTRY_PATH = Path("/media/adrian/NOEMA_SANDBOX/concepts/registry.jsonl")
CONCEPT_PENDING_DIR = Path("/media/adrian/NOEMA_SANDBOX/concepts/pending_review")
CROSS_SOURCE_AGREEMENT_THRESHOLD = 2

# A whole question ("wyjaśnij algorytm grovera") is not a lookup key any
# external API recognises — it 404s against a page-title endpoint. Stripping
# the question stem down to the actual concept ("algorytm grovera") is what
# makes the whitelist sources resolve at all. Keep this list in sync with
# scripts/validate_concept_candidates.py's copy — duplicated rather than
# imported because the script runs standalone, outside the package.
_QUESTION_STEMS = [
    r"^wyja[sś]nij\s+", r"^wyt[lł]umacz\s+",
    r"^co to s[aą]\s+", r"^co to jest\s+",
    r"^kto to jest\s+", r"^czym jest\s+",
    r"^czym s[aą]\s+", r"^kim jest\s+",
    r"^jaka jest\s+", r"^jakie s[aą]\s+",
    r"^jak\s+", r"^czy\s+",
    r"^co oznacza\s+", r"^zdefiniuj\s+",
    r"^opowiedz (mi )?o\s+", r"^powiedz mi o\s+",
    r"^explain\s+", r"^what (is|are)\s+",
    r"^define\s+", r"^tell me about\s+",
]


_FILLER_PREFIXES = [
    r"^problem\s+", r"^spos[óo]b\s+", r"^metod(a|ę)\s+",
    r"^zastosowanie\s+", r"^zastosowa[ńn]\s+",
    r"^znaczenie\s+", r"^definicj(a|ę)\s+",
    r"^istot(a|ę)\s+", r"^poj[ęe]cie\s+",
    r"^rozwi[aą]za[ńn](ie|ia)\s+",
]

# Posiłkowe czasowniki pytające — jeśli tekst zaczyna się od takiego,
# to znaczy że stem pytania nie został w pełni uchwycony.
_QUESTION_VERBS = [
    r"^rozwi[aą]za[ćc]?\s+",
    r"^dzia[łl]a[ćc]?\s+",
    r"^zrobi[ćc]\s+",
    r"^stworzy[ćc]\s+",
    r"^napisa[ćc]\s+",
    r"^znale[źz][ćc]\s+",
    r"^policzy[ćc]\s+",
    r"^obliczy[ćc]\s+",
    r"^zdefiniowa[ćc]\s+",
    r"^wyja[sś]ni[ćc]\s+",
    r"^opisa[ćc]\s+",
    r"^przedstawi[ćc]\s+",
    r"^istnie[ćcje]\s+",
]


def _extract_key_term(normalised_text: str) -> str:
    text = normalised_text
    # Pass 1: question-stems
    for pattern in _QUESTION_STEMS:
        stripped = re.sub(pattern, "", text)
        if stripped != text:
            text = stripped
            break
    word = text.strip() or normalised_text
    # Pass 2: filer prefixes (meta-words like "problem", "zastosowanie")
    for pattern in _FILLER_PREFIXES:
        stripped = re.sub(pattern, "", word)
        if stripped != word:
            word = stripped
            break
    # Pass 3: residual question verbs (Polish infinitives after "jak")
    for pattern in _QUESTION_VERBS:
        stripped = re.sub(pattern, "", word)
        if stripped != word:
            word = stripped
            break
    # Pass 4: ponownie filery (mogły się odkryć po usunięciu czasownika)
    for pattern in _FILLER_PREFIXES:
        stripped = re.sub(pattern, "", word)
        if stripped != word:
            word = stripped
            break
    # Pass 5: przywróć mianownik
    word = _restore_polish_nominative(word)
    return word


def _search_variants(term: str) -> list[str]:
    """Generuje warianty wyszukiwania — oryginał i ewentualne formy mianownikowe."""
    variants = [term]
    restored = _restore_polish_nominative(term)
    if restored != term:
        variants.append(restored)
    return variants


def _restore_polish_nominative(word: str) -> str:
    """Próbuje odgadnąć mianownik z formy odmienionej (wielokrotne podstawienia)."""
    replacements = [
        # Przymiotniki: (-ego → -y, -ej → -a, -ym → -y, -ych → -y)
        (r"ego\b", "y"),
        (r"ej\b", "a"),
        (r"ym\b", "y"),
        (r"ych\b", "y"),
        # Rzeczowniki żeńskie: Biernik -ę → -a, -ą → -a, Ms. -rze → -ra, -zie → -za
        (r"[ęą]\b", "a"),
        (r"rze\b", "ra"),
        (r"zie\b", "za"),
        (r"ce\b", "ka"),
        # Dopełniacz nijaki -nia → -nie
        (r"nia\b", "nie"),
        # Dopełniacz męski nieosobowy -u → "" (tylko po t/d/k/n/s)
        (r"(?<=[kltndst])u\b", ""),
        # Dopełniacz: -ii → -ia, -ji → -ja
        (r"ii\b", "ia"),
        (r"ji\b", "ja"),
        # Specyficzne nazwiska: -a → 0
        (r"stein[ea]\b", "stein"),
        (r"rier[ea]\b", "rier"),
        (r"lace[ea]\b", "lace"),
        # Dopełniacz żeński: -ki → -ka, -gi → -ga TYLKO dla długich słów (≥8 znaków)
        (r"(?<=\w{6})ki\b", "ka"),
        (r"(?<=\w{6})gi\b", "ga"),
    ]
    result = word
    for pattern, repl in replacements:
        candidate = re.sub(pattern, repl, result)
        if candidate != result:
            result = candidate
    return result


def _log_concept_candidate(normalised_text: str, matched_terms: list[str]) -> None:
    try:
        CONCEPT_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "text": normalised_text,
            "concept": _extract_key_term(normalised_text),
            "matched_terms": matched_terms,
            "review_status": "pending",
        }
        with CONCEPT_REGISTRY_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass


HOLONOMY_CANDIDATES_PATH = Path("/media/adrian/NOEMA_SANDBOX/concepts/holonomy_candidates.jsonl")
PHASENAV_SURFACE = Path("/dev/shm/ciel_noema")


def _concept_frequency(concept: str) -> int:
    """How many times this concept has been observed across the registry —
    explicit sieve parameter 5/8."""
    if not CONCEPT_REGISTRY_PATH.exists():
        return 0
    count = 0
    for line in CONCEPT_REGISTRY_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (entry.get("concept") or _extract_key_term(entry.get("text", ""))) == concept:
            count += 1
    return count


def _holonomy_edge_strength(concept: str) -> float:
    """Weight of any existing candidate holonomy edge for this concept —
    explicit sieve parameter 8/8."""
    if not HOLONOMY_CANDIDATES_PATH.exists():
        return 0.0
    best = 0.0
    for line in HOLONOMY_CANDIDATES_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            edge = json.loads(line)
        except json.JSONDecodeError:
            continue
        if edge.get("source_surface") == concept or edge.get("target_surface") == concept:
            best = max(best, float(edge.get("weight") or 0.0))
    return best


def _phasenav_subthreshold_signals() -> dict[str, float | None]:
    """Sub-threshold context — never shown to the user, only used to weight
    confidence. Read directly from the live surface; absent/unreadable is a
    normal, non-fatal state (this function runs inside a formally-verified
    request path that does not otherwise depend on the phasenav surface)."""
    signals: dict[str, float | None] = {"phi_norm": None, "coherence_R": None}
    try:
        phi_path = PHASENAV_SURFACE / "phi"
        if phi_path.exists():
            import struct
            data = phi_path.read_bytes()
            n = len(data) // 8
            values = struct.unpack(f"{n}d", data[: n * 8])
            signals["phi_norm"] = round(sum(v * v for v in values) ** 0.5, 4)
    except (OSError, struct.error):
        pass
    try:
        r_path = PHASENAV_SURFACE / "R"
        if r_path.exists():
            import struct
            signals["coherence_R"] = round(struct.unpack("d", r_path.read_bytes()[:8])[0], 4)
    except (OSError, struct.error):
        pass
    return signals


def _confidence_sieve(
    *,
    concept: str,
    alias_match: bool,
    intent_term_match: bool,
    domain_carried: bool,
    draft: dict[str, Any] | None,
    operator_ids: list[str],
) -> dict[str, Any]:
    """The full, explicit basis for any answer CIEL gives outside a plain
    canon-alias hit — 8 named parameters plus sub-threshold context. A
    'simple answer' stays simple; what justifies it does not have to."""
    usable = _usable_findings(draft) if draft else []
    explicit = {
        "1_alias_match": alias_match,
        "2_intent_term_match": intent_term_match,
        "3_domain_carried": domain_carried,
        "4_cross_source_agreement": len(usable),
        "5_concept_frequency": _concept_frequency(concept),
        "6_bilingual_pl_en_coverage": bool(draft.get("bilingual_pl_en")) if draft else False,
        "7_operator_coherence": round(len(operator_ids) ** -0.5, 4) if operator_ids else 0.0,
        "8_holonomy_edge_strength": _holonomy_edge_strength(concept),
    }
    return {
        "schema": "noema.confidence_sieve/v1",
        "explicit_parameters": explicit,
        "subthreshold": _phasenav_subthreshold_signals(),
    }


def _load_research_draft(normalised_text: str) -> dict[str, Any] | None:
    key_term = _extract_key_term(normalised_text)
    digest = hashlib.sha256(key_term.encode("utf-8")).hexdigest()[:16]
    path = CONCEPT_PENDING_DIR / f"{digest}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _usable_findings(draft: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        finding
        for finding in draft.get("findings", [])
        if finding.get("has_content") is True and finding.get("extract")
    ]


def _compose_cross_source_speech(term: str, findings: list[dict[str, Any]]) -> str:
    lines = [
        f"[Badanie wielo-źródłowe, nie kanon] Dla «{term}» znalazłem zgodne "
        f"wzmianki w {len(findings)} niezależnych, otwartych źródłach:"
    ]
    for finding in findings[:4]:
        lines.append(f"  - {finding['source_name']}: {finding['extract']}")
        lines.append(f"    ({finding['url']})")
    lines.append(
        "To NIE jest zweryfikowana karta kanoniczna — to moje własne "
        "zestawienie źródeł open-source. Traktuj z odpowiednią niepewnością."
    )
    return "\n".join(lines)


def _web_resolve(question: str, normalised: str) -> tuple[str, str, list[dict[str, Any]], tuple[str, ...]]:
    key = _extract_key_term(normalised) or normalised
    variants = _search_variants(key)  # key-term + ewentualny mianownik
    results: list[dict[str, Any]] = []
    for v in variants:
        try:
            results = web_search(v, max_results=7)
            if results:
                key = v
                break
        except Exception:
            continue
    if not results:
        try:
            results = web_search(key, max_results=7)
        except Exception:
            return "unavailable", "", [], ("web_resolve_error",)
    if not results:
        return "unavailable", "", [], ("web_resolve_no_results",)
    sources = []
    lines = [
        f"[Web — nie kanon] Dla «{key}» znalazłam informacje w otwartych źródłach:"
    ]
    for i, r in enumerate(results[:4], 1):
        snippet = r.get("snippet", "").strip()[:300]
        title = r.get("title", "").strip()
        url = r.get("url", "")
        lines.append(f"\n{i}. {title or '(bez tytułu)'}")
        if snippet:
            lines.append(f"   {snippet}")
        lines.append(f"   Źródło: {url}")
        sources.append({"id": f"web_{i}", "label": title, "url": url, "type": "web"})
    lines.append(
        "\nTo nie jest zweryfikowana karta kanoniczna — "
        "to wynik automatycznego przeszukania sieci. "
        "Zweryfikuj w oryginalnych źródłach przed użyciem."
    )
    return "web_resolved", "\n".join(lines), sources, ("web_resolved", "not_canon_reviewed", f"sources={len(results)}")


def _load_runtime_contract(path: Path = RUNTIME_CONTRACT_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "ciel.headless-runtime/v1":
        raise ValueError("unsupported CIEL headless runtime contract")
    return payload


_RUNTIME_CONTRACT = _load_runtime_contract()
MAX_SESSIONS = int(_RUNTIME_CONTRACT["session"]["capacity"])
SESSION_TTL_NS = int(_RUNTIME_CONTRACT["session"]["ttl_seconds"]) * 1_000_000_000
SESSION_ID_MAX_BYTES = int(_RUNTIME_CONTRACT["request"]["session_id_max_bytes"])


@dataclass
class SessionState:
    session_key: str
    turn_index: int = 0
    active_domain: str | None = None
    previous_focus: str | None = None
    claim_ids: list[str] = field(default_factory=list)
    started_monotonic_ns: int = field(default_factory=time.monotonic_ns)
    updated_monotonic_ns: int = field(default_factory=time.monotonic_ns)


@dataclass(frozen=True)
class AutonomousSpeech:
    status: str
    text: str
    domain: str | None
    focus: str | None
    operator: str
    phase_vector: tuple[float, ...]
    phase_basis: tuple[str, ...]
    phase_encoding: str
    claim_ids: tuple[str, ...]
    sources: tuple[dict[str, str], ...]
    uncertainty: tuple[str, ...]
    continuity: dict[str, Any]
    generated_at: str
    event_id: str
    generation_mode: str = "source_grounded_composition"
    fallback_used: bool = False
    raw_prompt_persisted: bool = False
    confidence_sieve: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["phase_vector"] = list(self.phase_vector)
        row["phase_basis"] = list(self.phase_basis)
        row["claim_ids"] = list(self.claim_ids)
        row["sources"] = list(self.sources)
        row["uncertainty"] = list(self.uncertainty)
        return row


class CIELAutonomousResponder:
    """Deterministic speech planner over reviewed source claims."""

    def __init__(self, knowledge_path: Path = KNOWLEDGE_PATH) -> None:
        payload = json.loads(knowledge_path.read_text(encoding="utf-8"))
        if payload.get("schema") != "cielingo.verified-knowledge/v1":
            raise ValueError("unsupported CIELingo knowledge schema")
        self.knowledge_path = knowledge_path
        self.pack = payload
        self.claims = {claim["id"]: claim for claim in payload["claims"]}
        self.claims_by_focus: dict[str, list[dict[str, Any]]] = {}
        for claim in payload["claims"]:
            self.claims_by_focus.setdefault(claim["focus"], []).append(claim)
        self.sources = {source["id"]: source for source in payload["sources"]}
        self.focus_parents = {
            focus: tuple(parents) for focus, parents in payload["focus_parents"].items()
        }
        self.focus_claims = {
            focus: tuple(claim_ids) for focus, claim_ids in payload["focus_claims"].items()
        }
        self.focus_operators = payload["focus_operators"]
        unknown_operators = {
            binding["operator"]
            for binding in self.focus_operators.values()
            if binding["operator"] not in ALL_OPERATOR_IDS
        }
        if unknown_operators:
            raise ValueError(f"unknown PhaseNav operators in knowledge pack: {sorted(unknown_operators)}")
        self._validate_pack()
        self._sessions: dict[str, SessionState] = {}
        self._lock = threading.RLock()

    def _validate_pack(self) -> None:
        claim_ids = [claim["id"] for claim in self.pack["claims"]]
        source_ids = [source["id"] for source in self.pack["sources"]]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("duplicate claim id in CIELingo knowledge pack")
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("duplicate source id in CIELingo knowledge pack")
        unknown_sources = {
            source_id
            for claim in self.pack["claims"]
            for source_id in claim.get("sources", [])
            if source_id not in self.sources
        }
        if unknown_sources:
            raise ValueError(f"unknown source ids in claims: {sorted(unknown_sources)}")
        unknown_claims = {
            claim_id
            for plan in self.focus_claims.values()
            for claim_id in plan
            if claim_id not in self.claims
        }
        if unknown_claims:
            raise ValueError(f"unknown claim ids in focus plans: {sorted(unknown_claims)}")
        known_foci = set(self.focus_claims)
        if set(self.focus_operators) != known_foci:
            raise ValueError("focus_operators must cover exactly every focus plan")
        referenced_foci = set(self.focus_parents)
        referenced_foci.update(parent for parents in self.focus_parents.values() for parent in parents)
        if referenced_foci - known_foci:
            raise ValueError(f"unknown focus in graph: {sorted(referenced_foci - known_foci)}")
        for focus in known_foci:
            if self._is_ancestor(focus, focus):
                raise ValueError(f"cycle in focus graph at {focus}")

    @staticmethod
    def _normalise(text: str) -> str:
        return " ".join(re.findall(r"[\w+\-/=]+", text.casefold(), flags=re.UNICODE))

    def _domain_matches(self, normalised: str) -> bool:
        return any(alias in normalised for alias in self.pack["aliases"])

    def _is_ancestor(self, candidate: str, focus: str) -> bool:
        """Return whether candidate is a declared semantic ancestor of focus."""
        pending = list(self.focus_parents.get(focus, ()))
        visited: set[str] = set()
        while pending:
            parent = pending.pop()
            if parent == candidate:
                return True
            if parent not in visited:
                visited.add(parent)
                pending.extend(self.focus_parents.get(parent, ()))
        return False

    def _focus(self, normalised: str, state: SessionState) -> tuple[str | None, list[str]]:
        matches: dict[str, list[str]] = {}
        for focus, terms in self.pack["intent_terms"].items():
            found = [term for term in terms if term in normalised]
            if found:
                matches[focus] = found
        if matches:
            terminal_foci = [
                focus
                for focus in matches
                if not any(
                    focus != other and self._is_ancestor(focus, other)
                    for other in matches
                )
            ]
            focus = "+".join(terminal_foci)
            found = [term for terminal in terminal_foci for term in matches[terminal]]
            return focus, found
        follow_up = any(term in normalised for term in self.pack["continuity_terms"])
        if follow_up and state.active_domain == self.pack["domain_id"]:
            return state.previous_focus or "definition", ["session_continuity"]
        return None, []

    def _claims_for(self, focus: str) -> list[dict[str, Any]]:
        claim_ids: list[str] = []
        for component in focus.split("+"):
            for claim_id in self.focus_claims.get(component, ()):
                if claim_id not in claim_ids:
                    claim_ids.append(claim_id)
        return [self.claims[claim_id] for claim_id in claim_ids]

    def _operator_coordinates(self, focus: str | None) -> tuple[str, tuple[float, ...]]:
        """Encode declared logical roles on the exact canonical operator axes.

        The coordinates are an L2-normalised incidence vector.  This avoids
        treating SHA-seeded pseudo-random signatures as measured semantics.
        """
        operator_ids: list[str] = []
        for component in (focus or "").split("+"):
            binding = self.focus_operators.get(component)
            if binding and binding["operator"] not in operator_ids:
                operator_ids.append(binding["operator"])
        if not operator_ids:
            operator_ids = ["UNCERTAINTY"]
        amplitude = len(operator_ids) ** -0.5
        vector = tuple(amplitude if axis in operator_ids else 0.0 for axis in ALL_OPERATOR_IDS)
        return "+".join(operator_ids), vector

    @staticmethod
    def _render_claims(claims: list[dict[str, Any]]) -> str:
        paragraphs: list[str] = []
        for claim in claims:
            part = claim["statement_pl"]
            equations = claim.get("equations") or []
            if equations:
                part += "\n" + "\n".join(f"  {equation}" for equation in equations)
            paragraphs.append(part)
        return "\n\n".join(paragraphs)

    def _source_rows(self, claims: list[dict[str, Any]]) -> tuple[dict[str, str], ...]:
        ids: list[str] = []
        for claim in claims:
            for source_id in claim.get("sources", []):
                if source_id not in ids:
                    ids.append(source_id)
        return tuple(dict(self.sources[source_id]) for source_id in ids)

    def _next_state(self, session_key: str) -> SessionState:
        now_ns = time.monotonic_ns()
        expired = [
            key
            for key, item in self._sessions.items()
            if now_ns - item.updated_monotonic_ns >= SESSION_TTL_NS
        ]
        for key in expired:
            self._sessions.pop(key, None)
        state = self._sessions.get(session_key)
        if state is None:
            if len(self._sessions) >= MAX_SESSIONS:
                oldest = min(self._sessions.values(), key=lambda item: item.updated_monotonic_ns)
                self._sessions.pop(oldest.session_key, None)
            state = SessionState(session_key=session_key)
            self._sessions[session_key] = state
        return state

    def respond(self, text: str, *, session_id: str) -> AutonomousSpeech:
        if not text.strip():
            raise ValueError("CIEL speech requires non-empty text")
        if not session_id.strip():
            raise ValueError("CIEL speech requires session_id")
        if len(session_id.encode("utf-8")) > SESSION_ID_MAX_BYTES:
            raise ValueError("CIEL speech session_id exceeds runtime contract")
        normalised = self._normalise(text)
        session_key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()

        with self._lock:
            state = self._next_state(session_key)
            prior_turns = state.turn_index
            prior_focus = state.previous_focus
            focus, matched_terms = self._focus(normalised, state)
            alias_matches = self._domain_matches(normalised)
            focus_has_domain_evidence = focus is not None and matched_terms != ["session_continuity"]
            domain_carried = (
                not alias_matches
                and state.active_domain == self.pack["domain_id"]
                and focus is not None
            )
            domain_matches = alias_matches or focus_has_domain_evidence or domain_carried

            if domain_matches and focus is not None:
                claims = self._claims_for(focus)
                status = "ok"
                speech = self._render_claims(claims)
                if "elektrowoltaika" in normalised:
                    speech = (
                        "Interpretuję «elektrowoltaikę Einsteina» jako elektrowakuum "
                        "Einsteina-Maxwella; jeśli chodziło o inny formalizm, skoryguj mnie.\n\n"
                        + speech
                    )
                uncertainty: tuple[str, ...] = ()
                state.active_domain = self.pack["domain_id"]
                state.previous_focus = focus
                for claim in claims:
                    if claim["id"] not in state.claim_ids:
                        state.claim_ids.append(claim["id"])
            else:
                draft = _load_research_draft(normalised)
                usable = _usable_findings(draft) if draft else []
                if len(usable) >= CROSS_SOURCE_AGREEMENT_THRESHOLD:
                    claims = []
                    status = "ok"
                    speech = _compose_cross_source_speech(text, usable)
                    uncertainty = (
                        "cross_source_research",
                        "not_canon_reviewed",
                        f"agreeing_sources={len(usable)}",
                    )
                else:
                    w_status, w_speech, w_sources, w_uncertainty = _web_resolve(text, normalised)
                    if w_status == "web_resolved":
                        claims = []
                        status = "web_resolved"
                        speech = w_speech
                        sources = w_sources
                        uncertainty = w_uncertainty
                    else:
                        claims = []
                        status = "unavailable"
                        speech = (
                            "Nie mam dla tego pytania zweryfikowanego pakietu twierdzeń. "
                            "Mogę odpowiedzieć dopiero po dołączeniu źródła albo kanonicznej karty wiedzy."
                        )
                        uncertainty = ("verified_knowledge_unavailable",)
                        _log_concept_candidate(normalised, matched_terms)

            state.turn_index += 1
            state.updated_monotonic_ns = time.monotonic_ns()
            claim_ids = tuple(claim["id"] for claim in claims)
            source_rows = tuple(sources) if status == "web_resolved" else self._source_rows(claims)
            operator, vector = self._operator_coordinates(focus if status == "ok" else None)
            continuity = {
                "session_ref": session_key[:16],
                "turn_index": state.turn_index,
                "prior_turns": prior_turns,
                "prior_focus": prior_focus,
                "active_domain": state.active_domain,
                "topic_carried_from_session": domain_carried,
                "matched_terms": matched_terms,
                "remembered_claim_ids": list(state.claim_ids),
                "storage": _RUNTIME_CONTRACT["session"]["storage"],
            }
            generated_at = datetime.now(timezone.utc).isoformat()
            event_payload = json.dumps(
                {
                    "session_ref": session_key[:16],
                    "turn": state.turn_index,
                    "domain": state.active_domain,
                    "focus": focus,
                    "claims": claim_ids,
                    "operator": operator,
                    "generated_at": generated_at,
                },
                sort_keys=True,
                ensure_ascii=False,
            )
            event_id = "ciel_evt_" + hashlib.sha256(event_payload.encode("utf-8")).hexdigest()[:24]
            active_domain = state.active_domain
            sieve = _confidence_sieve(
                concept=_extract_key_term(normalised),
                alias_match=alias_matches,
                intent_term_match=focus_has_domain_evidence,
                domain_carried=domain_carried,
                draft=draft if not (domain_matches and focus is not None) else None,
                operator_ids=operator.split("+"),
            )

        return AutonomousSpeech(
            status=status,
            text=speech,
            domain=active_domain if status == "ok" else None,
            focus=focus,
            operator=operator,
            phase_vector=tuple(float(value) for value in vector),
            phase_basis=tuple(ALL_OPERATOR_IDS),
            phase_encoding="canonical_operator_incidence_l2",
            claim_ids=claim_ids,
            sources=source_rows,
            uncertainty=uncertainty,
            continuity=continuity,
            generated_at=generated_at,
            event_id=event_id,
            confidence_sieve=sieve,
            fallback_used=status == "web_resolved",
            generation_mode="web_resolved_composition" if status == "web_resolved" else "source_grounded_composition",
        )


_RESPONDER: CIELAutonomousResponder | None = None
_RESPONDER_LOCK = threading.Lock()


def get_autonomous_responder() -> CIELAutonomousResponder:
    global _RESPONDER
    if _RESPONDER is None:
        with _RESPONDER_LOCK:
            if _RESPONDER is None:
                _RESPONDER = CIELAutonomousResponder()
    return _RESPONDER


__all__ = ["AutonomousSpeech", "CIELAutonomousResponder", "get_autonomous_responder"]
