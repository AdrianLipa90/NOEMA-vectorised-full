"""Bounded dialogue-competence signals for CIELingo.

This module does not claim to determine whether a speaker is human.  It turns
observable conversational obligations--turn taking, clarification, correction,
reference, and epistemic stance--into small, inspectable signals that a
response policy can use.  It is deliberately deterministic and retains no raw
dialogue.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Iterable, Mapping


_WORD_RE = re.compile(r"[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", re.UNICODE)
_QUESTION_WORDS = {
    "co", "czy", "dlaczego", "gdzie", "jak", "jaki", "jakie", "kiedy", "kto", "po co",
    "which", "why", "how", "what", "when", "where", "who", "can",
}
_GREETING_WORDS = {"cześć", "czesc", "hej", "siema", "witaj", "dzień", "dzien", "hello", "hi"}
_ACK_WORDS = {"ok", "okej", "dobrze", "jasne", "super", "dzięki", "dzieki", "thanks", "thanks"}
_CORRECTION_MARKERS = ("nie chodzi o", "nie o", "tylko o", "raczej", "poprawka", "korekta")
_CONTENT_NOISE = {
    "chodzi", "nie", "o", "tylko", "raczej", "to", "ten", "ta", "te", "jest", "było", "bylo",
    "proszę", "prosze", "mi", "się", "sie", "the", "and", "that", "this",
}


def _tokens(text: str) -> list[str]:
    return [token.casefold() for token in _WORD_RE.findall(text)]


def _content(values: Iterable[str], *, limit: int = 6) -> tuple[str, ...]:
    return tuple(dict.fromkeys(token for token in values if len(token) > 2 and token not in _CONTENT_NOISE))[:limit]


def _revision(text: str) -> dict[str, tuple[str, ...]]:
    """Extract a bounded semantic correction without preserving the sentence."""
    normalized = " ".join(text.casefold().split())
    match = re.search(r"nie\s+(?:chodzi\s+)?o\s+(.+?),?\s+(?:ale\s+)?tylko\s+o\s+(.+)", normalized)
    if not match:
        return {"retracted": (), "accepted": ()}
    return {
        "retracted": _content(_tokens(match.group(1))),
        "accepted": _content(_tokens(match.group(2))),
    }


@dataclass(frozen=True)
class DialogueSignal:
    act: str
    epistemic_stance: str
    social_tone: str
    requires_clarification: bool
    repair_requested: bool
    revision: dict[str, tuple[str, ...]]
    confidence: float
    quality: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["revision"] = {key: list(items) for key, items in self.revision.items()}
        return value


def analyze_dialogue(text: str, continuity: Mapping[str, Any] | None = None) -> DialogueSignal:
    """Return an explainable dialogue policy signal from one local turn.

    ``continuity`` may contain bounded context metadata only.  No text from a
    previous turn is accepted or emitted by this function.
    """
    cleaned = " ".join(str(text or "").split())
    tokens = _tokens(cleaned)
    token_set = set(tokens)
    has_question = "?" in cleaned or bool(token_set & _QUESTION_WORDS)
    revision = _revision(cleaned)
    repair_requested = bool(revision["retracted"] or revision["accepted"]) or any(
        marker in cleaned.casefold() for marker in _CORRECTION_MARKERS
    )
    greeting = bool(token_set & _GREETING_WORDS)
    acknowledgement = len(tokens) <= 5 and bool(token_set & _ACK_WORDS)
    reference_requested = bool((continuity or {}).get("reference_requested"))
    has_topic = bool((continuity or {}).get("active_topic"))

    if repair_requested:
        act = "correction"
    elif greeting and len(tokens) <= 6:
        act = "greeting"
    elif acknowledgement:
        act = "acknowledgement"
    elif has_question:
        act = "question"
    elif tokens and tokens[0] in {"zrób", "zrob", "wyjaśnij", "wyjasnij", "napisz", "sprawdź", "sprawdz"}:
        act = "request"
    else:
        act = "statement"

    requires_clarification = not tokens or (has_question and len(_content(tokens)) == 0)
    stance = "inquiry" if has_question else "revision" if repair_requested else "directive" if act == "request" else "social" if act in {"greeting", "acknowledgement"} else "assertion"
    social_tone = "warm" if greeting or acknowledgement else "repair" if repair_requested else "neutral"
    reference_score = 1.0 if not reference_requested else (1.0 if has_topic else 0.0)
    repair_score = 1.0 if repair_requested else 0.8
    clarity_score = 0.35 if requires_clarification else min(1.0, 0.55 + 0.08 * len(_content(tokens)))
    confidence = round(max(0.0, min(1.0, 0.45 * clarity_score + 0.35 * reference_score + 0.20 * repair_score)), 4)
    return DialogueSignal(
        act=act,
        epistemic_stance=stance,
        social_tone=social_tone,
        requires_clarification=requires_clarification,
        repair_requested=repair_requested,
        revision=revision,
        confidence=confidence,
        quality={
            "turn_taking": 1.0 if tokens else 0.0,
            "reference_resolution": reference_score,
            "repair_handling": repair_score,
            "clarity": round(clarity_score, 4),
        },
    )


__all__ = ["DialogueSignal", "analyze_dialogue"]
