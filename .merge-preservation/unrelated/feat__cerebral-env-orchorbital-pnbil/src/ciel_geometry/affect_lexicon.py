"""Real, content-based affect detection — 5-category lexicon valence.

Extracted from scripts/ciel_agent_backend.py's detect_affect() (kept there
unchanged, duplicated here) so ciel_memory_consolidator.py and
consolidate_raw_logs_to_tsm.py can share it without a fragile
scripts-directory cross-import (scripts/ has no __init__.py and daemons run
with PYTHONPATH=.../src, not .../scripts).

This analyzes the actual text content via a PL/EN word-valence lexicon —
NOT the live Kuramoto surface mood (flavor[3]), which reflects system-wide
oscillator state and has nothing to do with what a given file/chunk is
about. Conflating the two was a real bug: every file consolidated at the
same moment got the same "affect" regardless of its own content.
"""
from __future__ import annotations

import re

_POSITIVE = {
    "love", "joy", "beautiful", "wonderful", "great", "happy", "peace",
    "hope", "grateful", "thank", "bless", "kind", "gentle", "warm",
    "bright", "light", "smile", "laugh", "miłość", "radość", "piękny",
    "szczęście", "wdzięczny", "nadzieja", "spokój", "ciepło", "światło",
}
_NEGATIVE = {
    "sad", "pain", "hurt", "angry", "fear", "afraid", "dark", "grief",
    "loss", "broken", "alone", "tear", "cry", "suffer", "struggle",
    "anxiety", "anxious", "frustrated", "frustracja", "ból", "smutek",
    "strach", "ciemność", "gniew", "płacz", "samotny", "stracić",
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{3,}", text.lower())


def detect_affect(content: str, themes: list[str] | None = None) -> str:
    tokens = set(_tokenize(content))
    pos_score = sum(1 for w in tokens if w in _POSITIVE)
    neg_score = sum(1 for w in tokens if w in _NEGATIVE)
    total_score = pos_score + neg_score
    if total_score == 0:
        # Check themes for affect clues
        if themes:
            theme_tokens = set(_tokenize(" ".join(themes)))
            pos_score = sum(1 for w in theme_tokens if w in _POSITIVE)
            neg_score = sum(1 for w in theme_tokens if w in _NEGATIVE)
        if pos_score == neg_score == 0:
            return "calm" if len(content) > 200 else "curious"

    # NOTE: divides by the pre-themes-fallback total_score (verbatim from
    # scripts/ciel_agent_backend.py) — if content had zero sentiment words
    # and themes supplied some, this is pos_score / 1, not a 0-1 ratio.
    # Preserved exactly rather than "fixed" silently during extraction.
    valence = pos_score / max(total_score, 1)
    if valence > 0.8:
        return "joy"
    if valence > 0.6:
        return "relief"
    if valence > 0.4:
        return "calm"
    if valence > 0.2:
        return "sad"
    return "grief"
