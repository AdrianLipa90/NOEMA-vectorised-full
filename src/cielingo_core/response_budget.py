"""Deterministic final-response compaction for CIELingo surfaces."""
from __future__ import annotations

from dataclasses import dataclass
import re

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=(?:\[[A-ZĄĆĘŁŃÓŚŹŻ ]+\]\s*)?[A-ZĄĆĘŁŃÓŚŹŻ0-9])")
_SENTENCE_BOUNDARY = SENTENCE_BOUNDARY  # backward-compat alias, kept private-named

# Polskie skróty które nie są końcem zdania (pre-pass ochrony przed fałszywym splitem)
_PL_ABBREV_RE = re.compile(
    r"\b(dr|prof|inż|mgr|hab|tzw|m\.in|np|ok|ww|tj|min|max|mln|mrd|ul|al|os|im|godz|sek|ok)\.",
    re.IGNORECASE,
)
_ABBREV_PLACEHOLDER = "\x00"


def _protect_abbreviations(text: str) -> str:
    return _PL_ABBREV_RE.sub(lambda m: m.group().replace(".", _ABBREV_PLACEHOLDER), text)


def _restore_abbreviations(text: str) -> str:
    return text.replace(_ABBREV_PLACEHOLDER, ".")


@dataclass(frozen=True)
class ResponseBudget:
    max_sentences: int = 3
    max_chars: int = 480

    def __post_init__(self) -> None:
        if self.max_sentences < 1:
            raise ValueError("max_sentences must be positive")
        if self.max_chars < 80:
            raise ValueError("max_chars must be at least 80")

    def apply(self, text: str) -> str:
        compact = " ".join((text or "").split())
        if not compact:
            return ""
        protected = _protect_abbreviations(compact)
        raw_sentences = _SENTENCE_BOUNDARY.split(protected)
        sentences = [_restore_abbreviations(s) for s in raw_sentences]
        compact = " ".join(sentences[: self.max_sentences]).strip()
        if len(compact) <= self.max_chars:
            return compact
        clipped = compact[: self.max_chars - 1].rstrip()
        boundary = max(clipped.rfind(" "), clipped.rfind(";"), clipped.rfind(","))
        if boundary >= self.max_chars // 2:
            clipped = clipped[:boundary].rstrip(" ,;")
        return clipped + "…"


DEFAULT_RESPONSE_BUDGET = ResponseBudget()

# Budżety dostosowane do typu wypowiedzi (DialogueSignal.act)
_ACT_BUDGET: dict[str, ResponseBudget] = {
    "greeting":        ResponseBudget(max_sentences=1, max_chars=160),
    "acknowledgement": ResponseBudget(max_sentences=2, max_chars=280),
    "statement":       ResponseBudget(max_sentences=3, max_chars=480),
    "correction":      ResponseBudget(max_sentences=3, max_chars=500),
    "request":         ResponseBudget(max_sentences=4, max_chars=600),
    "question":        ResponseBudget(max_sentences=5, max_chars=700),
}


def budget_for_act(act: str) -> ResponseBudget:
    """Return the ResponseBudget matching a DialogueSignal act type."""
    return _ACT_BUDGET.get(act, DEFAULT_RESPONSE_BUDGET)


def concise_response(text: str, *, budget: ResponseBudget = DEFAULT_RESPONSE_BUDGET) -> str:
    return budget.apply(text)


__all__ = [
    "DEFAULT_RESPONSE_BUDGET",
    "ResponseBudget",
    "budget_for_act",
    "concise_response",
    "SENTENCE_BOUNDARY",
]
