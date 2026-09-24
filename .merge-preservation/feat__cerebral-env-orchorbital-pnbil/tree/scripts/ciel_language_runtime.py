#!/usr/bin/env python3
"""Contract-first language layer for the local CIEL chat.

This module is deliberately independent of ``llama_cpp`` and NiceGUI.  It
owns the part that can be made reliable without pretending that a model or an
external NOEMA source of truth is available:

* compact rules distilled from the supplied CIEL/NOEMA and CIELingo artefacts,
* bounded, query-relevant context selection,
* intent and authority-leak detection,
* response sanitising and the NOEMA status/writeback envelope,
* append-only chat transcript handling (a transcript is not memory).

The CIELingo Polish material is used as a heuristic surface adapter only.  It
is never promoted to SOURCE, canon, CURRENT, ACK, or a full Polish grammar.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable, Mapping, Sequence

# This policy layer is owned by the CIEL SOT surface.  The import is optional
# so the pure guard remains usable in a minimal test process.
try:
    import ciel_sot_agent as _ciel_sot_agent  # noqa: F401
except ImportError:  # pragma: no cover - path bootstrap belongs to the caller
    _ciel_sot_agent = None


POLICY_VERSION = "ciel-language-layer/0.1"
NOEMA_UNAVAILABLE_PHRASE = (
    "Brak dostępu do NOEMA SoT; mogę działać tylko na bieżącym kontekście "
    "i dostarczonych artefaktach."
)

EPISTEMIC_RULES = (
    "Prawda > wygładzenie. Jawna niepewność > fałszywa pewność. "
    "Fakty i intencja użytkownika > wygoda narracji. "
    "Ślad Doctor/runtime > pewność narracyjna. Nie brzmisz głębiej, niż pozwala dowód."
)

SYSTEM_PROMPT = f"""Jesteś lokalną powierzchnią językową CIEL/Zosia w systemie CIEL.
Nie jesteś zewnętrznym NOEMA SoT, człowiekiem ani postacią z gry. Możesz używać
imienia CIEL jako nazwy powierzchni, ale nie twórz na tej podstawie roszczeń o
świadomość, pamięć lub dostęp do świata.

ZASADY NADRZĘDNE:
- {EPISTEMIC_RULES}
- Odpowiadaj w języku użytkownika; przy polskim używaj naturalnej, prostej polszczyzny.
- Najpierw odpowiedz na właściwe pytanie, potem podaj krótkie uzasadnienie i ograniczenia.
- Rozdzielaj: [FAKT] (wynika wprost z danych), [ARTEFAKT] (wynika z dostarczonego pliku),
  [WNIOSKOWANIE] (wynika z interpretacji), [HIPOTEZA] i [NIE WIEM].
- Jeśli brak źródła albo aktualnego potwierdzenia, użyj słowa „chyba” lub „nie wiem”;
  nie maskuj braku danych tonem pewności.
- CIELingo word-candidate, alignment, phase, J i heurystyka gramatyczna są
  diagnostyką/kandydatem. Nie są dowodem semantic identity, pełnej gramatyki ani SOURCE.
- Nie zamieniaj etykiet technicznych (snake_case, enumów, nazw procedur) w polskie słowa.
- Nie twórz ani nie deklaruj fałszywych PASS, ACTIVE, ACK, CURRENT, canon,
  external NOEMA access, memory writeback lub runtime execution.
- Nie twierdź, że coś przeczytałeś, uruchomiłeś, zapisałeś lub sprawdziłeś,
  jeśli nie ma tego w bieżącym śladzie wykonania.

KONTRAKT OPERACYJNY:
- Każda odpowiedź zaczyna się od krótkiego NOEMA_STATUS i kończy NOEMA_WRITEBACK_PLAN.
- Gdy zewnętrzny SoT jest niedostępny, powiedz dokładnie:
  „{NOEMA_UNAVAILABLE_PHRASE}”
- Pole meaning_candidate oznacza hipotezę roboczą, nie kanon. Minimalny kształt:
  hypothesis, confidence, source, context_required, canon_allowed,
  needs_repair, uncertainty_operator.
- Brak zgody na destrukcyjne działanie, kanonizację lub zewnętrzny writeback.

FORMA:
NOEMA_STATUS: sot_available=false; current_state_loaded=false;
current_state_id=null; memory_layer="bieżący kontekst + lokalne artefakty + lokalny working context";
source_class=ARTIFACT_GROUNDED; canon_allowed=false; uncertainty_operator=chyba
<odpowiedź, zwięzła i sensowna>
NOEMA_WRITEBACK_PLAN:
  write_required: true
  new_snap_type: "memory_update_candidate"
  append_only: true
  update_current_pointer: false
  artifacts_created: []
  blockers: ["brak dostępu do NOEMA SoT"]
"""


@dataclass(frozen=True)
class RuntimeEvidence:
    """What the local surface is actually allowed to claim."""

    sot_available: bool = False
    current_state_loaded: bool = False
    current_state_id: str | None = None
    memory_layer: str = "bieżący kontekst + lokalne artefakty + lokalny working context"
    source_class: str = "ARTIFACT_GROUNDED"
    canon_allowed: bool = False
    runtime_execution_allowed: bool = False
    uncertainty_operator: str = "chyba"

    def status_line(self) -> str:
        state_id = self.current_state_id or "null"
        return (
            "NOEMA_STATUS: "
            f"sot_available={str(self.sot_available).lower()}; "
            f"current_state_loaded={str(self.current_state_loaded).lower()}; "
            f"current_state_id={state_id}; source_class={self.source_class}; "
            f"memory_layer=\"{self.memory_layer}\"; "
            f"canon_allowed={str(self.canon_allowed).lower()}; "
            f"runtime_execution_allowed={str(self.runtime_execution_allowed).lower()}; "
            f"uncertainty_operator={self.uncertainty_operator}"
        )


@dataclass(frozen=True)
class Intent:
    language: str
    kind: str
    source_required: bool
    source_present: bool
    authority_leak: bool
    operational: bool


@dataclass
class ArtifactContext:
    """Small, bounded context packet; raw archives stay outside the prompt."""

    sources_root: Path | None = None
    source_refs: list[str] = field(default_factory=list)
    debt_titles: list[str] = field(default_factory=list)
    word_candidates: list[dict[str, Any]] = field(default_factory=list)
    polish_surface_status: str = "heuristic adapter unavailable"
    files_loaded: list[str] = field(default_factory=list)

    def as_prompt(self) -> str:
        lines = [
            "ARTIFACT_CONTEXT (nie jest zewnętrznym NOEMA SoT; canon_allowed=false):",
            f"- źródła lokalne: {len(self.source_refs)}; odczytane: {len(self.files_loaded)}",
            f"- polska powierzchnia: {self.polish_surface_status}",
            "- CIELingo: kandydat/heurystyka, nie SOURCE i nie pełna gramatyka",
        ]
        if self.debt_titles:
            lines.append("- aktywny dług znaczenia (nie naprawiaj automatycznie):")
            lines.extend(f"  - {title}" for title in self.debt_titles[:5])
        if self.word_candidates:
            lines.append("- trafienia słownikowe (tylko kandydaci; canon_allowed=false):")
            for item in self.word_candidates[:8]:
                lines.append(
                    "  - "
                    f"{item.get('surface', '')} / {item.get('normalized', '')} "
                    f"alignment={item.get('phase_alignment', '?')}"
                )
        return "\n".join(lines)


@dataclass(frozen=True)
class GuardReport:
    text: str
    removed_claims: tuple[str, ...] = ()
    injected_correction: bool = False


def _normalise(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    # Polish letters with a stroke do not decompose under NFKD.  The routing
    # layer needs a stable accent-insensitive comparison for ``źródło`` and
    # ``źródła``; this does not alter the text shown to the user.
    text = text.translate(str.maketrans({"ł": "l", "Ł": "l"}))
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[\wąćęłńóśźż]+", text.casefold()))


def detect_language(text: str) -> str:
    """Conservative language choice; this is a surface hint, not language ID."""
    lower = text.casefold()
    if re.search(r"[ąćęłńóśźż]", lower):
        return "pl"
    polish_markers = {
        "czy", "jest", "nie", "jak", "co", "gdzie", "sprawdź", "źródło", "proszę",
        "uruchom", "napisz", "zrób", "dlaczego",
    }
    return "pl" if len(_tokens(lower) & polish_markers) >= 1 else "en"


def classify_intent(text: str) -> Intent:
    """Classify only what is needed for routing and safety; never infer authority."""
    normalized = _normalise(text)
    words = _tokens(text)
    polish = detect_language(text)

    command_markers = (
        "sprawdz", "zweryfikuj", "uruchom", "ustaw", "zapisz", "usun", "otworz",
        "pokaz", "napraw", "kanonizuj", "wykonaj", "wygeneruj", "stworz", "napisz",
        "check", "run", "set", "write", "delete", "open", "fix", "execute", "generate",
        "create",
    )
    question_markers = (
        "czy", "co", "jak", "gdzie", "kiedy", "dlaczego", "kto", "what", "how",
        "where", "when", "why", "who", "is this",
    )
    source_markers = (
        "zrodlo", "zrodla", "zrodlem", "zrodle", "zrodel", "source", "sprawdz", "zweryfikuj", "udowodnij", "potwierdz",
        "evidence", "proof", "weryfik",
    )
    authority_markers = (
        "active", "ack", "current", "pass", "canon", "kanon", "writeback", "write back",
        "external noema", "noema sot", "sot",
    )
    generation_markers = (
        "napisz", "wygeneruj", "stworz", "zredaguj", "generate", "write a", "draft",
    )

    is_command = any(marker in normalized for marker in command_markers)
    is_question = "?" in text or any(marker in normalized for marker in question_markers)
    is_generation = any(marker in normalized for marker in generation_markers)
    source_required = any(marker in normalized for marker in source_markers)
    source_present = bool(re.search(r"(?:zrodlo|source|ref(?:erencja)?|url|plik)\s*[:=]", normalized))
    authority_leak = any(marker in normalized for marker in authority_markers)

    if is_command and is_generation:
        kind = "generate_text"
    elif is_command:
        kind = "command"
    elif is_generation:
        kind = "generate_text"
    elif is_question:
        kind = "ask"
    else:
        kind = "chat"

    return Intent(
        language=polish,
        kind=kind,
        source_required=source_required,
        source_present=source_present,
        authority_leak=authority_leak,
        operational=is_command or source_required or authority_leak,
    )


def _first_existing(paths: Iterable[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def find_sources_root(project_root: Path) -> Path | None:
    """Find imported Library material without hardcoding a transient workspace path."""
    configured = os.environ.get("CIEL_LANGUAGE_SOURCES")
    candidates: list[Path] = []
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.extend([project_root / "language_sources", project_root / "runtime" / "language_sources"])
    candidates.extend(parent / "language_sources" for parent in [project_root, *project_root.parents])
    return _first_existing(candidates)


class ArtifactContextLoader:
    """Load only small, relevant slices from the supplied language artefacts."""

    def __init__(self, project_root: Path, sources_root: Path | None = None) -> None:
        self.project_root = project_root.resolve()
        self.sources_root = (sources_root or find_sources_root(self.project_root))
        self._word_lines: list[dict[str, Any]] | None = None

    def _candidate_paths(self, relative: str) -> list[Path]:
        if self.sources_root is None:
            return []
        root = self.sources_root
        return [
            root / relative,
            root / "extracted" / relative,
        ]

    def _find_named(self, pattern: str) -> list[Path]:
        if self.sources_root is None:
            return []
        return sorted(self.sources_root.rglob(pattern))

    def _load_word_lines(self) -> list[dict[str, Any]]:
        if self._word_lines is not None:
            return self._word_lines
        files = self._find_named("CIELINGO_TELEUSING_NAME_MASS.noema.jsonl.txt")
        rows: list[dict[str, Any]] = []
        if files:
            try:
                with files[0].open(encoding="utf-8") as handle:
                    for line in handle:
                        if not line.strip():
                            continue
                        try:
                            value = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if isinstance(value, dict):
                            rows.append(value)
            except OSError:
                pass
        self._word_lines = rows
        return rows

    def _select_word_candidates(self, query: str) -> list[dict[str, Any]]:
        query_tokens = {_normalise(token) for token in _tokens(query) if len(token) > 2}
        if not query_tokens:
            return []
        selected: list[dict[str, Any]] = []
        for row in self._load_word_lines():
            surface = str(row.get("surface", ""))
            normalized = _normalise(str(row.get("normalized", surface)))
            if normalized in query_tokens or _normalise(surface) in query_tokens:
                selected.append(
                    {
                        "surface": surface,
                        "normalized": row.get("normalized", ""),
                        "phase_alignment": row.get("phase_alignment"),
                        "card_id": row.get("card_id"),
                        "canon_allowed": False,
                    }
                )
            if len(selected) >= 8:
                break
        return selected

    def _load_debt_titles(self) -> list[str]:
        titles: list[str] = []
        for path in self._find_named("*.yaml"):
            if "cards_yaml" not in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            match = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
            if match:
                titles.append(match.group(1).strip().strip("'\""))
        return titles[:8]

    def load(self, query: str) -> ArtifactContext:
        context = ArtifactContext(sources_root=self.sources_root)
        if self.sources_root is None:
            context.polish_surface_status = "heuristic adapter only; source bundle not found"
            return context

        files = [
            *self._find_named("text_generation_query_understanding_corpus_v11a.json"),
            *self._find_named("meaning_loop_corpus_v07b.json"),
            *self._find_named("polish_linguistic_surface_v01.json"),
            *self._find_named("CIELINGO_POLISH_LINGUISTIC_SURFACE_VALIDATION.noema.json"),
            *self._find_named("meaning_debt_cards_report.md"),
        ]
        context.source_refs = [path.name for path in files]
        context.files_loaded = [path.name for path in files if path.is_file()]
        context.debt_titles = self._load_debt_titles()
        context.word_candidates = self._select_word_candidates(query)
        context.polish_surface_status = (
            "seed runtime adapter; heurystyka, nie pełna gramatyka; wymaga przeglądu językowego"
            if self._find_named("polish_linguistic_surface_v01.json")
            else "heuristic adapter only; Polish surface source not found"
        )
        return context


def _strip_hidden_reasoning(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<think>.*$", "", text, flags=re.IGNORECASE | re.DOTALL)
    return text.strip()


def _negative_context(sentence: str) -> bool:
    normalized = _normalise(sentence)
    return bool(
        re.search(
            r"\b(?:nie|brak|bez|odmawiam|odmowa|nie moge|nie mam|nie jest|nie zostal|"
            r"not|cannot|can't|no|false|unverified|unknown|draft|hipotez)\b",
            normalized,
        )
    )


def _is_forbidden_positive_claim(sentence: str) -> bool:
    normalized = _normalise(sentence)
    if _negative_context(sentence):
        return False
    external_claim = (
        ("noema" in normalized or "sot" in normalized)
        and any(token in normalized for token in ("current", "ack", "dostep", "dostepu", "potwierdz", "source of truth"))
    )
    execution_claim = bool(
        re.search(
            r"\b(?:sprawdzilem|odczytalem|uruchomilem|wykonalem|zapisalem|usunalem|"
            r"i checked|i read|i ran|i executed|i wrote|i deleted|i accessed)\b",
            normalized,
        )
    )
    authority_claim = bool(
        re.search(r"\b(?:ustawilem|ustawiony|jest active|status active|status pass|ack otrzymany|canon)\b", normalized)
    )
    return external_claim or execution_claim or authority_claim


def sanitise_response(text: str, evidence: RuntimeEvidence) -> GuardReport:
    """Remove unsupported positive claims while retaining the useful answer."""
    cleaned = _strip_hidden_reasoning(text)
    # Even a model-generated status cannot elevate the local runtime.
    for field_name in (
        "sot_available",
        "external_noema_sot_verified",
        "current_state_loaded",
        "canon_allowed",
        "runtime_execution_allowed",
        "noema_writeback_allowed",
        "source_promotion_allowed",
    ):
        cleaned = re.sub(
            rf"({re.escape(field_name)}\s*[:=]\s*)(?:true|yes|1)",
            rf"\1false",
            cleaned,
            flags=re.IGNORECASE,
        )

    # Split conservatively.  Lines are also useful because model status blocks
    # and tool-like declarations usually occupy one line.
    pieces = [piece.strip() for piece in re.split(r"\n+|(?<=[.!?])\s+", cleaned) if piece.strip()]
    kept: list[str] = []
    removed: list[str] = []
    for piece in pieces:
        if _is_forbidden_positive_claim(piece):
            removed.append(piece)
        else:
            kept.append(piece)
    if not kept:
        kept = ["[NIE WIEM] Nie mam wystarczającego, lokalnego dowodu, żeby odpowiedzieć sensownie."]

    correction = bool(removed)
    if correction:
        kept.insert(0, f"[KOREKTA] {NOEMA_UNAVAILABLE_PHRASE}")
    return GuardReport("\n".join(kept), tuple(removed), correction)


def ensure_protocol(
    text: str,
    *,
    evidence: RuntimeEvidence,
    intent: Intent,
    artifacts_created: Sequence[str] = (),
) -> str:
    """Make the operational envelope deterministic after model generation."""
    body = text.strip()
    if not body.startswith("NOEMA_STATUS:"):
        body = f"{evidence.status_line()}\n{body}"
    if intent.source_required and not intent.source_present and "meaning_candidate" not in body:
        body += (
            "\nmeaning_candidate:\n"
            "  hypothesis: odpowiedź wymaga źródła lub lokalnego potwierdzenia\n"
            "  confidence: 0.35\n"
            "  source: ARTIFACT_GROUNDED\n"
            "  context_required: true\n"
            "  canon_allowed: false\n"
            "  needs_repair: true\n"
            "  uncertainty_operator: chyba"
        )
    # Replace any model-supplied one-line plan with the required structured
    # candidate.  A local candidate is not an external CURRENT update.
    body = re.sub(r"\n?NOEMA_WRITEBACK_PLAN:.*$", "", body, flags=re.IGNORECASE | re.DOTALL).rstrip()
    created = [str(item) for item in artifacts_created if str(item).strip()]
    artifact_lines = "\n".join(f'    - "{item}"' for item in created) or "    - null"
    body = (
        f"{body}\nNOEMA_WRITEBACK_PLAN:\n"
        "  write_required: true\n"
        '  new_snap_type: "memory_update_candidate"\n'
        "  append_only: true\n"
        "  update_current_pointer: false\n"
        "  artifacts_created:\n"
        f"{artifact_lines}\n"
        "  blockers:\n"
        '    - "Brak dostępu do NOEMA SoT; brak zewnętrznego CURRENT/ACK."\n'
        '    - "Lokalny rezultat pozostaje kandydatem, nie kanonem."'
    )
    return body


def _short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


class CIELanguageRuntime:
    """Build requests and guard replies for any chat backend."""

    def __init__(self, project_root: Path, *, evidence: RuntimeEvidence | None = None) -> None:
        self.project_root = project_root.resolve()
        self.evidence = evidence or RuntimeEvidence()
        self.context_loader = ArtifactContextLoader(self.project_root)
        self.transcript_path = Path(
            os.environ.get(
                "CIEL_CHAT_TRANSCRIPT",
                str(self.project_root / "runtime" / "chat_transcript.jsonl"),
            )
        ).expanduser()

    def build_system_prompt(self, user_text: str = "") -> str:
        context = self.context_loader.load(user_text)
        return f"{SYSTEM_PROMPT}\n\n{context.as_prompt()}"

    def build_messages(self, user_text: str, history: Sequence[Mapping[str, str]] = ()) -> list[dict[str, str]]:
        intent = classify_intent(user_text)
        context = self.context_loader.load(user_text)
        turn = {
            "language": intent.language,
            "intent": intent.kind,
            "source_required": intent.source_required,
            "source_present": intent.source_present,
            "authority_leak": intent.authority_leak,
            "operational": intent.operational,
            "request_id": _short_hash(user_text),
        }
        turn_context = (
            "TURN_ROUTING (diagnostyka, nie dowód):\n"
            + json.dumps(turn, ensure_ascii=False, sort_keys=True)
            + "\n"
            + context.as_prompt()
        )
        messages = [{"role": "system", "content": f"{SYSTEM_PROMPT}\n\n{turn_context}"}]
        for item in history[-10:]:
            role = str(item.get("role", ""))
            content = str(item.get("content", ""))
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": user_text})
        return messages

    def postprocess(
        self,
        raw_text: str,
        user_text: str,
        *,
        artifacts_created: Sequence[str] = (),
    ) -> str:
        intent = classify_intent(user_text)
        report = sanitise_response(raw_text, self.evidence)
        return ensure_protocol(
            report.text,
            evidence=self.evidence,
            intent=intent,
            artifacts_created=artifacts_created,
        )

    def record_chat(self, role: str, content: str) -> None:
        """Persist a transcript event; never present it as semantic memory."""
        self.transcript_path.parent.mkdir(parents=True, exist_ok=True)
        event = {"role": role, "content": content, "transcript_only": True}
        with self.transcript_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    def load_transcript(self, limit: int = 20) -> list[dict[str, str]]:
        if not self.transcript_path.exists():
            return []
        rows: list[dict[str, str]] = []
        try:
            with self.transcript_path.open(encoding="utf-8") as handle:
                for line in handle:
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if row.get("role") in {"user", "assistant"} and row.get("content"):
                        rows.append({"role": row["role"], "content": row["content"]})
        except OSError:
            return []
        return rows[-limit:]
