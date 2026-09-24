from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping
import json
import re
import time

from .cielingo_bridge import build_lingo_frame
from .discourse_memory import (
    build_discourse_state,
    check_consistency,
    enrich_query_with_discourse,
)
from .surface_realizer import build_surface_plan, realize_surface
from .episodic_memory import episodes_from_rows, select_episodic_memory


@dataclass(frozen=True)
class DialogueAct:
    act: str
    language: str
    concepts: List[str]
    operators: List[str]
    unresolved: List[str]
    confidence: float
    turn_index: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _lang(language: str | None, text: str) -> str:
    polish_chars = set("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ")
    text_is_polish = any(ch in polish_chars for ch in text)
    # Text detection wins if the text is clearly Polish — state language may be stale.
    if text_is_polish:
        return "pl"
    if language:
        key = language.lower()
        if key.startswith("pl"):
            return "pl"
        if key.startswith("en"):
            return "en"
    return "en"


def _is_question(text: str, operators: Iterable[str]) -> bool:
    if "?" in text:
        return True
    q = {
        "czy", "co", "kto", "gdzie", "kiedy", "dlaczego", "jak", "ile",
        "what", "who", "where", "when", "why", "how", "which",
    }
    tokens = {t.lower() for t in re.findall(r"[\wąćęłńóśźż]+", text, flags=re.I)}
    return bool(tokens & q) or bool(set(operators) & q)


def _detect_act(text: str, frame: Mapping[str, Any], turn_index: int, language: str) -> DialogueAct:
    concepts = [str(x) for x in frame.get("concept_tokens", []) if str(x).strip()]
    operators = [str(x) for x in frame.get("operator_tokens", []) if str(x).strip()]
    unresolved = [str(x) for x in frame.get("unresolved", []) if str(x).strip()]
    route = frame.get("noema_route") if isinstance(frame.get("noema_route"), Mapping) else {}
    confidence = float(route.get("confidence", frame.get("projection_confidence", 0.0)) or 0.0)

    low = text.strip().lower()
    greetings = {"cześć", "czesc", "hej", "dzień dobry", "dzien dobry", "hello", "hi", "hey"}
    thanks = {"dzięki", "dzieki", "dziękuję", "dziekuje", "thanks", "thank you"}
    continues = {"kontynuuj", "dalej", "continue", "go on"}
    correction_markers = {
        "to nieprawda", "to błąd", "to blad", "koryguj",
        "chodziło mi o", "chodzilo mi o", "miałem na myśli", "mialem na mysli",
        "that is false", "that's false", "that is wrong", "that's wrong", "i meant",
    }
    provenance_markers = {
        "fakt", "hipoteza", "źródło", "zrodlo", "pochodzenie", "pewność", "pewnosc",
        "fact", "hypothesis", "source", "provenance", "confidence",
    }
    temporal_markers = {"kiedy", "when"}
    capability_markers = {"potrafisz", "możesz", "mozesz", "umiesz", "can", "able"}
    surface_tokens = {t.lower() for t in re.findall(r"[\wąćęłńóśźż]+", text, flags=re.I)}

    normalized_control = re.sub(r"[?!.]+$", "", low).strip()
    normalized_control = re.sub(r"^(a|i|and|then)\s+", "", normalized_control).strip()

    # Check if text STARTS WITH a greeting word (even if followed by name/question)
    _first_token = re.split(r"[\s,!.?]", low)[0] if low else ""
    _starts_with_greeting = _first_token in greetings

    explicit_correction_command = normalized_control in {"popraw", "correct that", "correct it"}
    if any(marker in low for marker in correction_markers) or low.startswith(("nie,", "no,")) or explicit_correction_command:
        act = "correct"
    elif low in greetings or _starts_with_greeting:
        act = "greet"
    elif low in thanks:
        act = "acknowledge_thanks"
    elif low in continues or normalized_control in continues:
        act = "continue"
    elif _is_question(text, operators) and bool(surface_tokens & capability_markers):
        act = "capability_question"
    elif _is_question(text, operators) and bool(surface_tokens & provenance_markers):
        act = "provenance_question"
    elif _is_question(text, operators) and bool(surface_tokens & temporal_markers):
        act = "temporal_question"
    elif _is_question(text, operators):
        act = "answer_question"
    elif unresolved:
        act = "clarify"
    else:
        act = "respond"

    return DialogueAct(
        act=act,
        language=language,
        concepts=concepts,
        operators=operators,
        unresolved=unresolved,
        confidence=confidence,
        turn_index=turn_index,
    )


def _memory_lines(ciel_state: Mapping[str, Any], max_items: int = 12) -> List[str]:
    out: List[str] = []
    sector = ciel_state.get("sector_memory") if isinstance(ciel_state.get("sector_memory"), Mapping) else {}
    governed = sector.get("governed_retrieval") if isinstance(sector.get("governed_retrieval"), Mapping) else {}
    ranked = governed.get("coherence_surface") if isinstance(governed.get("coherence_surface"), list) else governed.get("ranked", [])
    if not isinstance(ranked, list):
        return out
    for row in ranked[:max_items]:
        if not isinstance(row, Mapping):
            continue
        text = str(row.get("text") or row.get("summary") or row.get("content") or "").strip()
        if text:
            out.append(text)
    return out


def _topic(act: DialogueAct, history: List[Mapping[str, str]]) -> str:
    # Continuation acts should recover the preceding user topic, not treat the control word itself as content.
    if act.act != "continue" and act.concepts:
        return ", ".join(act.concepts[:3])
    for msg in reversed(history):
        if str(msg.get("role", "")).lower() == "user":
            text = str(msg.get("content", "")).strip()
            if text:
                return text[:80]
    return "ten temat" if act.language == "pl" else "this topic"


_PL_CONNECTORS = [
    "",
    "Ponadto, warto wiedzieć, że ",
    "Warto dodać, że ",
    "Jednocześnie należy pamiętać, że ",
    "Z perspektywy systemu, widać, że ",
    "Co więcej, okazuje się, że ",
    "Należy też zauważyć, że ",
    "W tym kontekście istotne jest, że ",
    "Równocześnie wiadomo, że ",
    "Istotne jest też, że ",
    "Poza tym należy wskazać, że ",
    "Można też wskazać, że ",
    "Na poziomie architektury, kluczowe jest, że ",
    "W ramach tej analizy wynika, że ",
    "Dopełniając obraz, trzeba zaznaczyć, że ",
]
_EN_CONNECTORS = [
    "",
    "Furthermore, ",
    "It is worth adding that ",
    "At the same time, ",
    "From the system perspective, ",
    "Moreover, ",
    "It should also be noted that ",
    "In this context, ",
    "Concurrently, ",
    "It is also significant that ",
    "Beyond that, ",
    "One can also point out that ",
    "At the architectural level, ",
    "Within this analysis, ",
    "To complete the picture, ",
]


def _token_stems(text: str) -> set[str]:
    toks = re.findall(r"[\wąćęłńóśźż]+", text.lower(), flags=re.I)
    return {tok[:5] for tok in toks if len(tok) >= 4}


def _select_memory(text: str, memories: List[str]) -> str | None:
    query = _token_stems(text)
    best: tuple[int, str] | None = None
    for mem in memories:
        score = len(query & _token_stems(mem))
        if score <= 0:
            continue
        if best is None or score > best[0]:
            best = (score, mem)
    return best[1] if best else None


def _is_nl_memory(t: str) -> bool:
    """Odrzuca REPO karty, JSON, metadane — akceptuje naturalny język."""
    t = t.strip()
    if len(t) < 20:
        return False
    if t.startswith(("#", "{", "[", "```", "- **")):
        return False
    if "**id_karty:**" in t or '"method":' in t or '"samples":' in t:
        return False
    if "## Tożsamość" in t or "poziom_orbitalny" in t:
        return False
    _REPO_MARKERS = ("**Purpose**:", "**Imports**:", "**Exports**:",
                     "**Active**:", "**Uses**:", "**Status**:",
                     "**Entry points**:", "**Optional deps**:",
                     "**Dependencies**:", "**Description**:")
    if any(m in t for m in _REPO_MARKERS):
        return False
    non_ascii = sum(1 for c in t if ord(c) > 127 and not c.isalpha())
    if non_ascii > len(t) * 0.25:
        return False
    return True


def _compose_memory_lines(memories: List[str], language: str, max_items: int = 15) -> str | None:
    """Komponuje wiele wpisów pamięci w wielozdaniowy akapit."""
    clean: List[str] = []
    seen: set[str] = set()
    for m in memories[:max_items * 2]:  # skanuj więcej, bo część odpada przez filtr
        m = m.strip().rstrip(" .")
        if not m or m in seen or not _is_nl_memory(m):
            continue
        seen.add(m)
        clean.append(m)
        if len(clean) >= max_items:
            break
    if not clean:
        return None
    if len(clean) == 1:
        return clean[0]
    connectors = _PL_CONNECTORS if language == "pl" else _EN_CONNECTORS
    sentences: List[str] = []
    for i, mem in enumerate(clean):
        conn = connectors[i] if i < len(connectors) else ("Dodatkowo, " if language == "pl" else "Additionally, ")
        if conn:
            body = mem[0].lower() + mem[1:] if len(mem) > 1 else mem.lower()
        else:
            body = mem
        sentences.append(f"{conn}{body}.")
    return " ".join(sentences)


def realize_native_reply(
    text: str,
    *,
    ciel_state: Mapping[str, Any] | None = None,
    history: List[Mapping[str, str]] | None = None,
    language: str | None = None,
) -> Dict[str, Any]:
    """Produce a deterministic, auditable CIELingo dialogue reply without an LLM.

    This is deliberately a small fallback surface realizer. It does not claim broad
    language competence. It turns CIELingo semantic frames, route confidence and
    retrieved memory into a conversational response that can later be replaced or
    refined by a primary language backend.
    """
    state = dict(ciel_state or {})
    hist = list(history or [])
    lang = _lang(language or str(state.get("language", "") or ""), text)
    frame = build_lingo_frame(text, ciel_state=state, language=lang)
    act = _detect_act(text, frame, len(hist), lang)
    discourse = build_discourse_state(text, history=hist, language=lang)
    retrieval_query = enrich_query_with_discourse(text, discourse)
    memories = _memory_lines(state, max_items=15)
    topic = discourse.active_topic or _topic(act, hist)
    episodic_rows = state.get("episodic_memory") if isinstance(state.get("episodic_memory"), list) else []
    episodes = episodes_from_rows(episodic_rows)
    selected_episode = select_episodic_memory(retrieval_query, episodes, topic=discourse.active_topic) if episodes else None
    # Dla answer_question: komponuj wielozdaniową odpowiedź z WSZYSTKICH pamięci.
    # Dla innych aktów: wybierz jedną najlepiej dopasowaną (nie zaburzaj powitań, korekt, itp.)
    if act.act == "answer_question" and not selected_episode:
        selected_memory = _compose_memory_lines(memories, lang, max_items=15)
    else:
        selected_memory = selected_episode.content if selected_episode else _select_memory(retrieval_query, memories)

    history_topic = None
    if act.act == "continue":
        for msg in reversed(hist):
            if str(msg.get("role", "")).lower() == "user":
                candidate = str(msg.get("content", "")).strip()
                if candidate:
                    history_topic = candidate
                    break

    surface_plan = build_surface_plan(
        dialogue_act=act.act,
        language=lang,
        source_text=text,
        memory=selected_memory,
        history_topic=history_topic,
        resolved_topic=topic,
    )
    consistency = check_consistency(
        history=hist,
        new_claim=selected_memory,
        topic=surface_plan.topic,
    )
    reply = realize_surface(
        surface_plan,
        memory=selected_memory,
        confidence=act.confidence,
        unresolved=[*act.unresolved, *discourse.unresolved_references],
        memory_provenance=selected_episode.provenance_class if selected_episode else "legacy_sector_memory",
        temporal_anchor=selected_episode.temporal_anchor.to_dict() if selected_episode else None,
        admission_verdict=selected_episode.admission_verdict if selected_episode else None,
    )
    if consistency.contradiction_detected and selected_memory:
        clause = selected_memory.strip().rstrip(" .")
        reply = (
            f"Koryguję wcześniejszą odpowiedź. {clause}."
            if lang == "pl"
            else f"I am correcting my earlier answer. {clause}."
        )

    return {
        "reply": reply,
        "dialogue_act": act.to_dict(),
        "frame": frame,
        "memory_used": [selected_memory] if selected_memory else [],
        "memory_provenance": selected_episode.provenance_class if selected_episode else "legacy_sector_memory",
        "memory_temporal_anchor": selected_episode.temporal_anchor.to_dict() if selected_episode else None,
        "memory_admission_verdict": selected_episode.admission_verdict if selected_episode else None,
        "surface_plan": surface_plan.to_dict(),
        "discourse_state": discourse.to_dict(),
        "consistency_check": consistency.to_dict(),
        "mode": "native_cielingo_lingophysics_discourse_episodic_surface",
    }


def append_dialogue_turn(
    journal_path: str | Path,
    *,
    user_text: str,
    result: Mapping[str, Any],
    feedback: str | None = None,
) -> None:
    """Append one auditable dialogue turn to a JSONL learning journal."""
    path = Path(journal_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts_unix": time.time(),
        "user_text": user_text,
        "reply": str(result.get("reply", "")),
        "dialogue_act": result.get("dialogue_act", {}),
        "mode": result.get("mode", ""),
        "feedback": feedback,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
