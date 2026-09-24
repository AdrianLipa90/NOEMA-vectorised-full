"""Concept windows — split text into sentence-grouped windows centered on
concept anchors, instead of encoding a whole document as one 36D vector.

Origin (2026-07-10, live conversation): CIEL's answer synthesis
(cielingo_inference.py's _synthesize_answer()) was appending unrelated
documents to answers — e.g. "Czy 2+2 to 4?" retrieved a cosmology paper
excerpt at similarity 0.78. Root-caused to fast_encode_text()
(cielingo_phase_encoder.py) starting every text from an IDENTICAL baseline
phase vector (np.linspace(0, 2π, 36)) and only touching a handful of
dimensions per document — the untouched majority is shared by every text
and dominates mean(cos(Δφ)) regardless of actual content.

Adrian's diagnosis, directly: a whole document is not one concept — meaning
is local, closed around the content surrounding each concept, not smeared
across an entire text. This module implements that: split text into
sentences, and for each concept-bearing sentence, build a WINDOW of that
sentence plus its immediate neighbors (a single sentence is often
insufficient context on its own — meaning is frequently built across
sentence boundaries, confirmed directly with Adrian before this design).

This does NOT fix the encoder itself (a separate, deferred, deeper
decision) — but denser, shorter windows have proportionally less "wasted"
untouched-dimension space relative to real content than whole documents,
which measurably improves discrimination (see phasenav_learning_gate.py's
own _vector_phase_coupling fix earlier the same session for the analogous
problem in a different consumer).
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import re
from dataclasses import dataclass

# Reused verbatim from src/cielingo/web_digest.py:32 — simple, punctuation-only,
# PL+EN agnostic, already proven in production (web_digest summarization).
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")

# Reused from src/cielingo_core/bridge/auto_verify.py:133-159 — the most
# complete PL+EN stopword/tokenizer pair found in the repo (handles
# hyphenated/apostrophe'd words). Extended here with a digit-token
# alternation (auto_verify.py's WORD_PATTERN excludes digits entirely,
# which would make "2+2" anchor on nothing at all — concept windows still
# need numeric content to count as an anchor).
_POLISH_STOPWORDS = {
    "i", "w", "na", "z", "do", "się", "nie", "to", "że", "a",
    "o", "ma", "jak", "po", "co", "za", "tak", "ale", "u", "czy",
    "od", "oraz", "przez", "dla", "bez", "nad", "pod", "przed",
    "między", "albo", "lub", "ani", "gdy", "jeżeli", "więc",
    "zatem", "bo", "ponieważ", "też", "no", "tylko", "już",
    "nawet", "właśnie", "być", "był", "była", "będzie", "jest",
    "są", "mają", "może", "mogą", "trzeba", "należy",
    "można", "bardzo", "bardziej", "coraz", "tu", "tam", "tutaj",
}
_ENGLISH_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "can", "shall",
    "it", "its", "this", "that", "these", "those", "i", "you", "he",
    "she", "we", "they", "me", "him", "her", "us", "them", "my",
    "your", "his", "our", "their", "not", "no", "nor", "so",
    "if", "then", "than", "too", "very", "just", "about", "also",
    "up", "down", "out", "off", "over", "under", "again", "further",
    "once", "here", "there", "all", "each", "every", "both", "few",
    "more", "most", "other", "some", "such", "only", "own", "same",
    "into", "upon", "after", "before", "between", "through", "during",
}
_STOPWORDS = _POLISH_STOPWORDS | _ENGLISH_STOPWORDS
_WORD_PATTERN = re.compile(
    r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:[-'][A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+)*|[0-9]+"
)


@dataclass
class ConceptWindow:
    """One sentence-grouped window centered on a concept-bearing sentence."""
    anchor_sentence_idx: int
    window_text: str
    sentence_range: tuple[int, int]  # inclusive [start, end] into the sentence list


def split_sentences(text: str) -> list[str]:
    """Split text into sentences on terminal punctuation. Same regex already
    proven in production by web_digest.py's summarizer."""
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []
    return [s.strip() for s in _SENTENCE_RE.split(normalized) if s.strip()]


def _has_concept_token(sentence: str) -> bool:
    """A sentence is concept-bearing if it has at least one non-stopword
    token — word or number (numbers matter: 'Czy 2+2 to 4?' must anchor on
    something, not fall through to zero tokens the way the underlying
    encoder's own >2-char-length filter drops '2'/'4' entirely)."""
    for tok in _WORD_PATTERN.findall(sentence.lower()):
        if tok not in _STOPWORDS:
            return True
    return False


def extract_concept_anchors(sentences: list[str]) -> list[int]:
    """Indices of sentences that carry at least one real concept token."""
    return [i for i, s in enumerate(sentences) if _has_concept_token(s)]


def build_concept_windows(text: str, radius: int = 1) -> list[ConceptWindow]:
    """Split text into concept windows: for each concept-bearing sentence,
    a window of [anchor-radius, anchor+radius] sentences joined together —
    per Adrian's direct correction (2026-07-10): a single sentence is often
    NOT enough context on its own, meaning is frequently built across
    sentence boundaries, so the window unit is a small group of sentences,
    not a fixed word count and not a lone sentence.

    Adjacent/overlapping windows (concept anchors close enough that their
    ±radius ranges overlap) collapse to identical window_text and are
    deduplicated — a dense paragraph with many content words shouldn't
    produce dozens of near-duplicate windows, one per word.
    """
    sentences = split_sentences(text)
    if not sentences:
        return []

    anchors = extract_concept_anchors(sentences)
    windows: list[ConceptWindow] = []
    seen_text: set[str] = set()

    for anchor in anchors:
        start = max(0, anchor - radius)
        end = min(len(sentences) - 1, anchor + radius)
        window_text = " ".join(sentences[start:end + 1])
        if window_text in seen_text:
            continue
        seen_text.add(window_text)
        windows.append(ConceptWindow(
            anchor_sentence_idx=anchor,
            window_text=window_text,
            sentence_range=(start, end),
        ))

    return windows


if __name__ == "__main__":
    import sys
    import json

    sample = sys.argv[1] if len(sys.argv) > 1 else (
        "Czy 2+2 to 4? To pytanie testowe. "
        "PhaseMemory przechowuje wektory 36D. Każdy wektor reprezentuje tekst. "
        "Dzisiaj naprawiłem kilka bugów w systemd. Bo chmod nie działał na NTFS."
    )
    windows = build_concept_windows(sample)
    for w in windows:
        print(json.dumps({
            "anchor": w.anchor_sentence_idx,
            "range": w.sentence_range,
            "text": w.window_text,
        }, ensure_ascii=False))
