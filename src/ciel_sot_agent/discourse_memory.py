from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Mapping, Sequence
import re


KNOWN_ENTITIES = {
    "newton": "Newton",
    "newtonie": "Newton",
    "newtona": "Newton",
    "newtonem": "Newton",
    "newtonowi": "Newton",
    "phasenav": "PhaseNav",
    "cielingo": "CIELingo",
    "noema": "NOEMA",
    "ciel": "CIEL",
}

_PL_ANAPHORA = {
    "on", "ona", "ono", "oni", "one", "go", "jego", "jej", "nim", "niej",
    "mu", "ją", "ich", "nich", "tego", "temu", "tym", "to", "ten", "ta", "te",
}
_EN_ANAPHORA = {
    "he", "she", "it", "they", "him", "her", "them", "this", "that", "these", "those",
}


@dataclass(frozen=True)
class DiscourseState:
    active_topic: str | None
    referents: List[str]
    unresolved_references: List[str]
    correction_target: str | None
    correction_requested: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConsistencyCheck:
    contradiction_detected: bool
    previous_claim: str | None
    new_claim: str | None
    topic: str | None
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _tokens(text: str) -> List[str]:
    return re.findall(r"[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ-]+", text, flags=re.UNICODE)


def _entity_mentions(text: str) -> List[str]:
    out: List[str] = []
    for token in _tokens(text):
        entity = KNOWN_ENTITIES.get(token.lower())
        if entity and entity not in out:
            out.append(entity)
    return out


def _history_messages(history: Sequence[Mapping[str, str]]) -> Iterable[Mapping[str, str]]:
    for row in reversed(history):
        if isinstance(row, Mapping):
            yield row


def _last_topic_from_history(history: Sequence[Mapping[str, str]]) -> str | None:
    for row in _history_messages(history):
        content = str(row.get("content", "")).strip()
        mentions = _entity_mentions(content)
        if mentions:
            return mentions[0]
    return None


def _is_correction(text: str, language: str) -> bool:
    low = text.strip().lower()
    if language == "pl":
        markers = (
            "nie,", "nie.", "to nieprawda", "to błąd", "to blad", "popraw", "koryguj",
            "chodziło mi o", "chodzilo mi o", "miałem na myśli", "mialem na mysli",
        )
    else:
        markers = (
            "no,", "no.", "that's false", "that is false", "that's wrong", "correct that",
            "i meant", "what i meant",
        )
    return any(marker in low for marker in markers)


def build_discourse_state(
    text: str,
    *,
    history: Sequence[Mapping[str, str]] | None = None,
    language: str = "pl",
) -> DiscourseState:
    hist = list(history or [])
    explicit = _entity_mentions(text)
    prior_topic = _last_topic_from_history(hist)
    tokens = {t.lower() for t in _tokens(text)}
    anaphora = _PL_ANAPHORA if language == "pl" else _EN_ANAPHORA
    reference_tokens = sorted(tokens & anaphora)

    unresolved: List[str] = []
    active_topic: str | None = explicit[0] if explicit else None
    referents: List[str] = list(explicit)

    if not active_topic and reference_tokens:
        if prior_topic:
            active_topic = prior_topic
            referents.append(prior_topic)
        else:
            unresolved.extend(reference_tokens)
    elif not active_topic and prior_topic:
        # Elliptical follow-ups such as "A dalej?" inherit the active topic,
        # but ordinary unrelated utterances do not force that inheritance.
        low = text.strip().lower()
        if low.startswith(("a ", "i ", "dalej", "kontynuuj", "więc", "wiec", "and ", "then ", "continue")):
            active_topic = prior_topic
            referents.append(prior_topic)

    correction_requested = _is_correction(text, language)
    correction_target = prior_topic if correction_requested else None
    return DiscourseState(
        active_topic=active_topic,
        referents=list(dict.fromkeys(referents)),
        unresolved_references=list(dict.fromkeys(unresolved)),
        correction_target=correction_target,
        correction_requested=correction_requested,
    )


def enrich_query_with_discourse(text: str, state: DiscourseState) -> str:
    """Add only the resolved topic needed for retrieval; never rewrite source text in-place."""
    if not state.active_topic:
        return text
    mentions = _entity_mentions(text)
    if state.active_topic in mentions:
        return text
    return f"{text} [{state.active_topic}]"


def _claim_signature(text: str, topic: str | None) -> tuple[set[str], bool]:
    low = text.lower()
    neg = bool(re.search(r"\b(nie|nigdy|brak|never|not|no)\b", low))
    toks = {
        t.lower()[:6]
        for t in _tokens(text)
        if len(t) >= 4 and t.lower() not in {
            "pamiętam", "pamietam", "that", "remember", "wcześniejszą", "wczesniejsza",
            "odpowiedź", "odpowiedz", "koryguję", "koryguje", "earlier", "answer",
        }
    }
    if topic:
        toks.add(topic.lower()[:6])
    return toks, neg


def check_consistency(
    *,
    history: Sequence[Mapping[str, str]] | None,
    new_claim: str | None,
    topic: str | None,
) -> ConsistencyCheck:
    if not new_claim:
        return ConsistencyCheck(False, None, None, topic, "no_new_claim")

    previous: str | None = None
    for row in _history_messages(list(history or [])):
        if str(row.get("role", "")).lower() != "assistant":
            continue
        candidate = str(row.get("content", "")).strip()
        if not candidate:
            continue
        if topic and topic.lower() not in candidate.lower():
            continue
        previous = candidate
        break

    if not previous:
        return ConsistencyCheck(False, None, new_claim, topic, "no_comparable_previous_claim")

    prev_sig, prev_neg = _claim_signature(previous, topic)
    new_sig, new_neg = _claim_signature(new_claim, topic)
    overlap = len(prev_sig & new_sig)
    contradiction = overlap >= 2 and prev_neg != new_neg
    reason = "opposed_polarity_on_shared_signature" if contradiction else "no_simple_contradiction"
    return ConsistencyCheck(contradiction, previous, new_claim, topic, reason)
