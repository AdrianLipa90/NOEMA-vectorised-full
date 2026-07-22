#!/usr/bin/env python3
"""Append-only local working-context continuity for the cerebral model.

This layer is intentionally separate from semantic memory and from the chat
transcript.  It keeps enough bounded state to resolve references such as
"kontynuuj", "to" and "jak wcześniej", while marking the result as
``LOCAL_WORKING_CONTEXT`` rather than NOEMA CURRENT or external memory.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import time
import uuid
from typing import Any, Iterable, Mapping, Sequence

log = logging.getLogger(__name__)


SCHEMA = "ciel/cerebral-continuity/v0.2"
HANDOFF_SCHEMA = "ciel/cerebral-handoff/v0.1"
GENESIS_DIGEST = "GENESIS"
MAX_RECENT_TURNS = 12
MAX_TOPIC_ITEMS = 12
MAX_REVISIONS = 12

_WORD_RE = re.compile(r"[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", re.UNICODE)
_CONTINUATION_MARKERS = (
    "kontynuuj", "kontynuacja", "dalej", "co dalej", "jak wcześniej", "jak wczesniej",
    "wróćmy", "wrocmy", "wracamy", "wznów", "wznow", "ciągłość", "ciaglosc",
    "continue", "carry on", "go on", "resume", "still", "next step",
)
_REFERENCE_MARKERS = (
    "to", "ten", "ta", "te", "tam", "wcześniej", "wczesniej", "poprzedni", "poprzednia",
    "znowu", "dalej", "wątek", "watek", "temat", "jak mówiłem", "jak mowilem",
    "jak mówiłeś", "jak mowiles",
)
_RESET_MARKERS = (
    "nowa sesja", "nowy kontekst", "wyczyść kontekst", "wyczysc kontekst",
    "reset kontekstu", "reset sesji", "start od zera", "new session", "reset context",
)
_TOPIC_NOISE = {
    "to", "ten", "ta", "te", "tam", "wcześniej", "wczesniej", "poprzedni", "poprzednia",
    "znowu", "dalej", "wątek", "watek", "temat", "kontynuuj", "kontynuacja", "wznów", "wznow",
    "ciągłość", "ciaglosc", "tym", "tę", "tego", "cześć", "czesc", "ciel", "hej", "siema",
    "dzień", "dzien", "dobry", "co", "dokładnie", "dokladnie", "pamiętasz", "pamietasz",
    "tej", "tura", "turze", "pamiętam", "pamietam",
    "chodzi", "tylko", "rozmawiamy", "rozmawiać", "rozmawiac",
}
_RAW_CHAT_KEYS = {"user_text", "assistant_text", "content", "raw_text", "transcript"}


def _tokens(text: str) -> list[str]:
    return [item.casefold() for item in _WORD_RE.findall(text)]


def _normalise(text: str) -> str:
    return text.casefold().translate(str.maketrans({"ł": "l", "Ł": "l"}))


def _digest(*parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def _marker_matches(text: str, marker: str) -> bool:
    normalized = _normalise(text)
    normalized_marker = _normalise(marker)
    if " " in normalized_marker:
        pattern = rf"(?<!\w){re.escape(normalized_marker)}(?!\w)"
        return bool(re.search(pattern, normalized))
    return normalized_marker in set(_tokens(normalized))


def _contains_marker(text: str, markers: Iterable[str]) -> bool:
    return any(_marker_matches(text, marker) for marker in markers)


def _topic_tokens(values: Iterable[str]) -> list[str]:
    return [value for value in values if _normalise(value) not in {_normalise(x) for x in _TOPIC_NOISE}]


def _same_topic(left: str, right: str) -> bool:
    """Conservative lexical stem equivalence for bounded Polish topic repairs."""
    normalized_left = _normalise(left)
    normalized_right = _normalise(right)
    if normalized_left == normalized_right:
        return True
    shortest = min(len(normalized_left), len(normalized_right))
    return shortest >= 5 and (
        normalized_left.startswith(normalized_right[:5])
        or normalized_right.startswith(normalized_left[:5])
    )


def _next_step(decision: str | None, open_loops: Sequence[str], has_topic: bool) -> str:
    """Derive a bounded next action without storing or inventing raw dialogue."""
    loop_steps = (
        ("missing_source", "uzupełnić źródło albo pozostawić twierdzenie jako hipotezę"),
        ("authority_boundary", "utrzymać granicę między artefaktem, hipotezą i kanonem"),
        ("needs_clarification", "doprecyzować pytanie przed kolejnym wnioskowaniem"),
    )
    for loop, step in loop_steps:
        if loop in open_loops:
            return step
    if decision in {"reflect", "defer"}:
        return "doprecyzować wejście przed kolejnym wnioskowaniem"
    if has_topic:
        return "wykonać następny sprawdzalny krok w aktywnym temacie"
    return "podaj jedno zdanie kotwicy dla nowego wątku"


def _excerpt(text: str, limit: int = 220) -> str:
    compact = " ".join(str(text).split())
    return compact[:limit].rstrip()


@dataclass(frozen=True)
class ContinuitySignal:
    session_id: str
    next_turn_index: int
    continuation_requested: bool
    reference_requested: bool
    reset_requested: bool
    references: tuple[str, ...]
    active_topic: tuple[str, ...]
    previous_turn: dict[str, Any]
    context_anchor: dict[str, Any]
    context_resolution: str
    chain_valid: bool
    revisions: tuple[dict[str, Any], ...] = ()
    source_class: str = "LOCAL_WORKING_CONTEXT"

    def as_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "next_turn_index": self.next_turn_index,
            "continuation_requested": self.continuation_requested,
            "reference_requested": self.reference_requested,
            "reset_requested": self.reset_requested,
            "references": list(self.references),
            "active_topic": list(self.active_topic),
            "previous_turn": dict(self.previous_turn),
            "context_anchor": dict(self.context_anchor),
            "context_resolution": self.context_resolution,
            "chain_valid": self.chain_valid,
            "revisions": [dict(item) for item in self.revisions],
            "source_class": self.source_class,
        }


class CerebralContinuity:
    """Persist and resolve a bounded chain of local working-context turns."""

    def __init__(self, path: Path, *, session_id: str | None = None) -> None:
        self.path = path
        configured_session = session_id or os.environ.get("CIEL_SESSION_ID")
        self.configured_session = configured_session
        self.state: dict[str, Any] = {
            "schema": SCHEMA,
            "session_id": configured_session or f"cerebral-{uuid.uuid4().hex[:12]}",
            "turn_index": 0,
            "chain_digest": GENESIS_DIGEST,
            "active_topic": [],
            "open_loops": [],
            "recent_turns": [],
            "revisions": [],
            "state_class": "LOCAL_WORKING_CONTEXT",
            "source_class": "LOCAL_WORKING_CONTEXT",
            "continuity_confidence": 1.0,
            "canon_allowed": False,
            "reconstructed_from_transcript": False,
        }
        self._loaded = False
        self._load(configured_session)

    @property
    def exists(self) -> bool:
        return self._loaded

    def _load(self, configured_session: str | None) -> None:
        if not self.path.exists():
            return
        try:
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            log.warning("cerebral continuity state could not be loaded: %s", exc)
            return
        if not isinstance(loaded, dict) or loaded.get("schema") != SCHEMA:
            return
        if configured_session and loaded.get("session_id") != configured_session:
            return
        self.state.update(
            {
                "session_id": str(loaded.get("session_id") or self.state["session_id"]),
                "turn_index": int(loaded.get("turn_index", 0) or 0),
                "chain_digest": str(loaded.get("chain_digest") or GENESIS_DIGEST),
                "active_topic": [str(x) for x in loaded.get("active_topic", [])][:MAX_TOPIC_ITEMS],
                "open_loops": [str(x) for x in loaded.get("open_loops", [])][:8],
                "recent_turns": [x for x in loaded.get("recent_turns", []) if isinstance(x, dict)][-MAX_RECENT_TURNS:],
                "revisions": [x for x in loaded.get("revisions", []) if isinstance(x, dict)][-MAX_REVISIONS:],
                "continuity_confidence": float(loaded.get("continuity_confidence", 1.0) or 1.0),
                "reconstructed_from_transcript": bool(loaded.get("reconstructed_from_transcript", False)),
            }
        )
        self._loaded = True

    @staticmethod
    def _verify_chain_rows(rows: Sequence[Mapping[str, Any]], chain_digest: str) -> bool:
        # The window is bounded.  When older rows have been dropped, the
        # first retained row carries the digest anchor of the omitted prefix.
        previous = str(rows[0].get("previous_turn_digest", GENESIS_DIGEST)) if rows else GENESIS_DIGEST
        for row in rows:
            if not isinstance(row, dict):
                return False
            if row.get("previous_turn_digest", previous) != previous:
                return False
            expected = _digest(
                previous,
                str(row.get("user_digest", "")),
                str(row.get("assistant_digest", "")),
                str(row.get("turn_index", "")),
            )
            if row.get("turn_digest") != expected:
                return False
            previous = expected
        if rows and chain_digest != previous:
            return False
        if not rows and chain_digest != GENESIS_DIGEST:
            return False
        return True

    def _verify_chain(self) -> bool:
        return self._verify_chain_rows(
            self.state.get("recent_turns", []),
            str(self.state.get("chain_digest") or GENESIS_DIGEST),
        )

    def hydrate_from_transcript(self, rows: Sequence[Mapping[str, str]]) -> bool:
        """Seed only a low-confidence working topic from a local transcript.

        This is never treated as a recovered NOEMA state.  It is explicitly
        tagged ``LOCAL_TRANSCRIPT_DERIVED`` and can be discarded with reset.
        """
        if self.exists or not rows:
            return False
        user_rows = [row for row in rows if row.get("role") == "user" and row.get("content")]
        if not user_rows:
            return False
        latest = user_rows[-1]
        concepts = _topic_tokens(token for token in _tokens(str(latest.get("content", ""))) if len(token) > 2)
        self.state["active_topic"] = list(dict.fromkeys(concepts))[:MAX_TOPIC_ITEMS]
        self.state["continuity_confidence"] = 0.35
        self.state["reconstructed_from_transcript"] = True
        self.state["source_class"] = "LOCAL_TRANSCRIPT_DERIVED"
        self.save()
        self._loaded = True
        return True

    def _context_anchor(self) -> dict[str, Any]:
        active_topic = list(self.state.get("active_topic", [])[:MAX_TOPIC_ITEMS])
        previous = self.state.get("recent_turns", [])[-1] if self.state.get("recent_turns") else {}
        previous = previous if isinstance(previous, dict) else {}
        open_loops = list(self.state.get("open_loops", [])[:8])
        if not open_loops:
            open_loops = [str(item) for item in previous.get("open_loops", [])][:8]
        decision = str(previous.get("decision")) if previous.get("decision") else None
        chain_digest = str(self.state.get("chain_digest") or GENESIS_DIGEST)
        anchor_digest = _digest(
            chain_digest,
            "|".join(active_topic),
            decision or "",
            "|".join(open_loops),
        )
        return {
            "turn_index": int(self.state.get("turn_index", 0) or 0),
            "topic": active_topic,
            "last_decision": decision,
            "open_loops": open_loops,
            "revisions": [
                dict(item) for item in self.state.get("revisions", [])[-MAX_REVISIONS:]
                if isinstance(item, dict)
            ],
            "next_step": _next_step(decision, open_loops, bool(active_topic)),
            "anchor_digest": anchor_digest,
            "source_class": self.state.get("source_class", "LOCAL_WORKING_CONTEXT"),
            "canon_allowed": False,
        }

    def signal(self, text: str) -> ContinuitySignal:
        reset_requested = _contains_marker(text, _RESET_MARKERS)
        continuation_requested = _contains_marker(text, _CONTINUATION_MARKERS)
        references = tuple(marker for marker in _REFERENCE_MARKERS if _marker_matches(text, marker))
        reference_requested = bool(references) or continuation_requested
        if reset_requested:
            return ContinuitySignal(
                session_id=self.state["session_id"],
                next_turn_index=1,
                continuation_requested=False,
                reference_requested=False,
                reset_requested=True,
                references=(),
                active_topic=(),
                previous_turn={},
                context_anchor={},
                context_resolution="reset_requested",
                chain_valid=self._verify_chain(),
                revisions=(),
            )

        active_topic = tuple(self.state.get("active_topic", [])[:MAX_TOPIC_ITEMS])
        previous = self.state.get("recent_turns", [])[-1] if self.state.get("recent_turns") else {}
        context_anchor = self._context_anchor()
        if reference_requested and active_topic:
            resolution = "resolved_local_working_context"
        elif reference_requested:
            resolution = "missing_local_working_context"
        else:
            resolution = "not_requested"
        return ContinuitySignal(
            session_id=str(self.state["session_id"]),
            next_turn_index=int(self.state.get("turn_index", 0)) + 1,
            continuation_requested=continuation_requested,
            reference_requested=reference_requested,
            reset_requested=False,
            references=references,
            active_topic=active_topic,
            previous_turn=dict(previous) if isinstance(previous, dict) else {},
            context_anchor=context_anchor,
            context_resolution=resolution,
            chain_valid=self._verify_chain(),
            revisions=tuple(
                dict(item) for item in self.state.get("revisions", [])[-MAX_REVISIONS:]
                if isinstance(item, dict)
            ),
        )

    def reset(self, *, reason: str = "user_requested") -> str:
        old_session = str(self.state.get("session_id"))
        configured = self.configured_session
        self.state = {
            "schema": SCHEMA,
            "session_id": configured or f"cerebral-{uuid.uuid4().hex[:12]}",
            "turn_index": 0,
            "chain_digest": GENESIS_DIGEST,
            "active_topic": [],
            "open_loops": [],
            "recent_turns": [],
            "revisions": [],
            "state_class": "LOCAL_WORKING_CONTEXT",
            "source_class": "LOCAL_WORKING_CONTEXT",
            "continuity_confidence": 1.0,
            "canon_allowed": False,
            "reset_reason": reason,
            "previous_session_id": old_session,
        }
        self._loaded = True
        self.save()
        return str(self.state["session_id"])

    def commit_turn(
        self,
        *,
        user_text: str,
        assistant_text: str,
        concepts: Sequence[str],
        operators: Sequence[str],
        decision: str,
        phase: float,
        coherence: float,
        open_loops: Sequence[str] = (),
        phase_gate: Mapping[str, Any] | None = None,
        dialogue: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not isinstance(phase_gate, Mapping) or phase_gate.get("admitted") is not True:
            return {
                "committed": False,
                "reason": "phase_gate_not_admitted",
                "turn_index": int(self.state.get("turn_index", 0)),
            }
        previous = str(self.state.get("chain_digest") or GENESIS_DIGEST)
        turn_index = int(self.state.get("turn_index", 0)) + 1
        user_digest = hashlib.sha256(user_text.encode("utf-8")).hexdigest()[:24]
        assistant_digest = hashlib.sha256(assistant_text.encode("utf-8")).hexdigest()[:24]
        turn_digest = _digest(previous, user_digest, assistant_digest, str(turn_index))
        revision = dialogue.get("revision", {}) if isinstance(dialogue, Mapping) else {}
        revision = revision if isinstance(revision, Mapping) else {}
        retracted = _topic_tokens(str(item) for item in revision.get("retracted", ()) if isinstance(item, str))
        accepted = _topic_tokens(str(item) for item in revision.get("accepted", ()) if isinstance(item, str))
        topic = [
            item for item in self.state.get("active_topic", [])
            if not any(_same_topic(str(item), retracted_item) for retracted_item in retracted)
        ]
        current_concepts = [
            item for item in _topic_tokens(concepts)
            if not any(_same_topic(item, retracted_item) for retracted_item in retracted)
        ]
        topic = list(dict.fromkeys([*topic, *accepted, *current_concepts]))[:MAX_TOPIC_ITEMS]
        dialogue_record = {
            "act": str(dialogue.get("act", "statement")) if isinstance(dialogue, Mapping) else "statement",
            "epistemic_stance": str(dialogue.get("epistemic_stance", "assertion")) if isinstance(dialogue, Mapping) else "assertion",
            "repair_requested": bool(dialogue.get("repair_requested")) if isinstance(dialogue, Mapping) else False,
            "confidence": float(dialogue.get("confidence", 0.0) or 0.0) if isinstance(dialogue, Mapping) else 0.0,
            "revision": {"retracted": retracted[:MAX_TOPIC_ITEMS], "accepted": accepted[:MAX_TOPIC_ITEMS]},
        }
        row = {
            "turn_id": f"{self.state['session_id']}:{turn_index}",
            "turn_index": turn_index,
            "previous_turn_digest": previous,
            "turn_digest": turn_digest,
            "user_digest": user_digest,
            "assistant_digest": assistant_digest,
            "concepts": list(dict.fromkeys(concepts))[:MAX_TOPIC_ITEMS],
            "operators": list(dict.fromkeys(operators))[:8],
            "active_topic": topic,
            "open_loops": list(dict.fromkeys(open_loops))[:8],
            "decision": decision,
            "phase": round(float(phase), 6),
            "coherence": round(float(coherence), 4),
            "created_at": time.time(),
            "source_class": "LOCAL_WORKING_CONTEXT",
            "canon_allowed": False,
            "phase_gate": {
                "disposition": phase_gate.get("disposition"),
                "score": phase_gate.get("score"),
                "tension": phase_gate.get("tension"),
                "graph_digest": phase_gate.get("graph_digest"),
            },
            "dialogue": dialogue_record,
            "committed": True,
        }
        rows = self.state.setdefault("recent_turns", [])
        rows.append(row)
        del rows[:-MAX_RECENT_TURNS]
        self.state["turn_index"] = turn_index
        self.state["chain_digest"] = turn_digest
        self.state["active_topic"] = topic
        self.state["open_loops"] = list(dict.fromkeys(open_loops))[:8]
        if retracted or accepted:
            revisions = self.state.setdefault("revisions", [])
            revisions.append({"turn_index": turn_index, **dialogue_record["revision"]})
            del revisions[:-MAX_REVISIONS]
        self.state["continuity_confidence"] = 1.0 if self._verify_chain() else 0.0
        self.state["source_class"] = "LOCAL_WORKING_CONTEXT"
        return row

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.state, ensure_ascii=False, indent=2, sort_keys=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(payload + "\n", encoding="utf-8")
        temporary.replace(self.path)

    def export_handoff(
        self,
        path: Path,
        *,
        artifact_refs: Sequence[str] = (),
    ) -> dict[str, Any]:
        """Write a portable local-context packet without raw dialogue."""
        rows = [row for row in self.state.get("recent_turns", []) if isinstance(row, dict)][-MAX_RECENT_TURNS:]
        payload = {
            "schema": HANDOFF_SCHEMA,
            "state_class": "LOCAL_WORKING_CONTEXT",
            "source_class": "LOCAL_HANDOFF_PACKET",
            "canon_allowed": False,
            "session_id": self.state.get("session_id"),
            "turn_index": int(self.state.get("turn_index", 0) or 0),
            "chain_digest": self.state.get("chain_digest") or GENESIS_DIGEST,
            "chain_valid": self._verify_chain(),
            "active_topic": list(self.state.get("active_topic", []))[:MAX_TOPIC_ITEMS],
            "open_loops": list(self.state.get("open_loops", []))[:8],
            "revisions": [dict(item) for item in self.state.get("revisions", [])[-MAX_REVISIONS:] if isinstance(item, dict)],
            "recent_turns": rows,
            "context_anchor": self._context_anchor(),
            "artifact_refs": list(dict.fromkeys(str(item) for item in artifact_refs))[:8],
            "created_at": time.time(),
        }
        path = path.expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
        return payload

    def import_handoff(self, path: Path) -> dict[str, Any]:
        """Restore only a verified local working-context packet."""
        path = path.expanduser()
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"nie można odczytać handoffu: {type(exc).__name__}") from exc
        if not isinstance(payload, dict) or payload.get("schema") != HANDOFF_SCHEMA:
            raise ValueError("nieznany schemat lokalnego handoffu")
        if payload.get("canon_allowed") is not False:
            raise ValueError("handoff nie spełnia granicy canon_allowed=false")
        configured_session = self.configured_session
        if configured_session and payload.get("session_id") != configured_session:
            raise ValueError("handoff należy do innej sesji; ustaw zgodny CIEL_SESSION_ID")
        rows = payload.get("recent_turns", [])
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError("handoff ma niepoprawny recent_turns")
        rows = rows[-MAX_RECENT_TURNS:]
        if any(_RAW_CHAT_KEYS.intersection(row) for row in rows):
            raise ValueError("handoff zawiera surowy transcript; import odrzucony")
        chain_digest = str(payload.get("chain_digest") or GENESIS_DIGEST)
        if not self._verify_chain_rows(rows, chain_digest):
            raise ValueError("handoff ma nieważny łańcuch digestów")
        turn_index = int(payload.get("turn_index", 0) or 0)
        if rows and turn_index < int(rows[-1].get("turn_index", 0) or 0):
            raise ValueError("handoff ma niespójny turn_index")
        if not rows and turn_index != 0:
            raise ValueError("handoff bez tur nie może mieć niezerowego turn_index")
        active_topic = payload.get("active_topic", [])
        open_loops = payload.get("open_loops", [])
        revisions = payload.get("revisions", [])
        if not isinstance(active_topic, list) or not isinstance(open_loops, list) or not isinstance(revisions, list):
            raise ValueError("handoff ma niepoprawną kotwicę tematu")
        self.state.update(
            {
                "schema": SCHEMA,
                "session_id": str(payload.get("session_id") or self.state["session_id"]),
                "turn_index": turn_index,
                "chain_digest": chain_digest,
                "active_topic": [str(item) for item in active_topic][:MAX_TOPIC_ITEMS],
                "open_loops": [str(item) for item in open_loops][:8],
                "revisions": [item for item in revisions if isinstance(item, dict)][-MAX_REVISIONS:],
                "recent_turns": rows,
                "state_class": "LOCAL_WORKING_CONTEXT",
                "source_class": "LOCAL_HANDOFF_PACKET",
                "continuity_confidence": 0.9,
                "canon_allowed": False,
                "reconstructed_from_transcript": False,
                "handoff_imported": True,
                "handoff_path": str(path),
            }
        )
        self._loaded = True
        self.save()
        return self.status()

    def status(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "session_id": self.state.get("session_id"),
            "turn_index": self.state.get("turn_index", 0),
            "active_topic": list(self.state.get("active_topic", [])),
            "open_loops": list(self.state.get("open_loops", [])),
            "revisions": [dict(item) for item in self.state.get("revisions", [])[-MAX_REVISIONS:] if isinstance(item, dict)],
            "context_anchor": self._context_anchor(),
            "chain_digest": self.state.get("chain_digest"),
            "chain_valid": self._verify_chain(),
            "continuity_confidence": self.state.get("continuity_confidence", 0.0),
            "state_class": "LOCAL_WORKING_CONTEXT",
            "source_class": self.state.get("source_class", "LOCAL_WORKING_CONTEXT"),
            "canon_allowed": False,
            "path": str(self.path),
        }


__all__ = ["CerebralContinuity", "ContinuitySignal", "HANDOFF_SCHEMA", "SCHEMA"]
