"""Deterministic final-response compaction for CIELingo surfaces."""
from __future__ import annotations

from dataclasses import dataclass
import re

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=(?:\[[A-ZĄĆĘŁŃÓŚŹŻ ]+\]\s*)?[A-ZĄĆĘŁŃÓŚŹŻ0-9])")
_SENTENCE_BOUNDARY = SENTENCE_BOUNDARY  # backward-compat alias, kept private-named


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
        sentences = _SENTENCE_BOUNDARY.split(compact)
        compact = " ".join(sentences[: self.max_sentences]).strip()
        if len(compact) <= self.max_chars:
            return compact
        clipped = compact[: self.max_chars - 1].rstrip()
        boundary = max(clipped.rfind(" "), clipped.rfind(";"), clipped.rfind(","))
        if boundary >= self.max_chars // 2:
            clipped = clipped[:boundary].rstrip(" ,;")
        return clipped + "…"


DEFAULT_RESPONSE_BUDGET = ResponseBudget()


def concise_response(text: str, *, budget: ResponseBudget = DEFAULT_RESPONSE_BUDGET) -> str:
    return budget.apply(text)


__all__ = ["DEFAULT_RESPONSE_BUDGET", "ResponseBudget", "concise_response", "SENTENCE_BOUNDARY"]
