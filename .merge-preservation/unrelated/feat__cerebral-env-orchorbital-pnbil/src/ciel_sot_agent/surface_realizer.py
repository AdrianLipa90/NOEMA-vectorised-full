from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Mapping
import json
import re


@dataclass(frozen=True)
class SurfacePlan:
    language: str
    dialogue_act: str
    predicate: str
    roles: Dict[str, str]
    topic: str
    grammar_family: str
    grammar_strategy: str
    modules: tuple[str, ...]
    valency_valid: bool
    unresolved: tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        out = asdict(self)
        out["modules"] = list(self.modules)
        out["unresolved"] = list(self.unresolved)
        return out


_POLISH_TOPIC_NORMALIZATION = {
    "newtonie": "Newton",
    "newtona": "Newton",
    "newtonem": "Newton",
    "newtonowi": "Newton",
    "phasenav": "PhaseNav",
    "cielingo": "CIELingo",
    "noema": "NOEMA",
    "ciel": "CIEL",
}

_PL_CONTROL = {
    "co", "czy", "kto", "gdzie", "kiedy", "dlaczego", "jak", "ile",
    "pamiętasz", "pamietasz", "wiesz", "myślisz", "myslisz", "sądzisz", "sadzisz",
    "potrafisz", "możesz", "mozesz", "umiesz", "powiedzieć", "powiedziec",
    "mi", "proszę", "prosze", "o", "na", "temat", "a", "ale", "więc", "wiec",
    "rozmawialiśmy", "rozmawialismy", "rozmawiamy", "mówiliśmy", "mowilismy",
}

_EN_CONTROL = {
    "what", "whether", "who", "where", "when", "why", "how", "which",
    "do", "you", "remember", "know", "think", "can", "able", "tell", "me", "about",
}


def _lingophysics_root() -> Path | None:
    base = Path(__file__).resolve().parents[1]
    candidate = base / "ciel_lingophysics_lns_repo_v2_3"
    return candidate if candidate.exists() else None


def _load_json(path: Path) -> Mapping[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _grammar_metadata(language: str) -> tuple[str, str, tuple[str, ...], tuple[str, ...]]:
    root = _lingophysics_root()
    if root is None:
        return "UNRESOLVED_LANGUAGE_FAMILY", "UNRESOLVED_GRAMMAR_STRATEGY", (), ("lingophysics_root",)
    families = _load_json(root / "data/language_families/language_family_grammar_profiles_v2_3.json")
    profiles = _load_json(root / "data/language_families/language_profile_specialization_v2_3.json")

    family: Mapping[str, Any] | None = None
    for row in families.get("families", []):
        if any(str(x.get("code", "")).lower() == language.lower() for x in row.get("languages", [])):
            family = row
            break
    profile = profiles.get("profiles", {}).get(f"language:{language}:standard", {})
    unresolved: list[str] = []
    if not family:
        unresolved.append("language_family")
        family = {}
    if not profile:
        unresolved.append("language_profile")

    modules: list[str] = []
    for item in list(family.get("algorithm_modules", [])) + list(profile.get("required_modules", [])):
        item = str(item)
        if item and item not in modules:
            modules.append(item)
    return (
        str(family.get("id", "UNRESOLVED_LANGUAGE_FAMILY")),
        str(profile.get("grammar_strategy", "UNRESOLVED_GRAMMAR_STRATEGY")),
        tuple(modules),
        tuple(unresolved),
    )


def _valency_valid(predicate: str, roles: Mapping[str, str]) -> bool:
    root = _lingophysics_root()
    if root is None:
        return False
    frames = _load_json(root / "data/event_frames/predicate_valency_frames.json")
    for frame in frames.get("frames", []):
        if str(frame.get("canonical_operator", "")).lower() != predicate.lower():
            continue
        required = set(frame.get("required_roles", []))
        return required.issubset(set(roles))
    return False


def _tokens(text: str) -> list[str]:
    return re.findall(r"[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ-]+", text, flags=re.UNICODE)


def normalize_topic(text: str, language: str) -> str:
    raw = _tokens(text)
    if not raw:
        return "ten temat" if language == "pl" else "this topic"

    controls = _PL_CONTROL if language == "pl" else _EN_CONTROL
    kept: list[str] = []
    for token in raw:
        low = token.lower()
        if low in controls:
            continue
        if language == "pl" and low in _POLISH_TOPIC_NORMALIZATION:
            kept.append(_POLISH_TOPIC_NORMALIZATION[low])
        else:
            kept.append(token)

    if not kept:
        return "ten temat" if language == "pl" else "this topic"
    # Prefer named entities or known project identifiers when available.
    special = [x for x in kept if x[:1].isupper() or x in {"PhaseNav", "CIELingo", "NOEMA", "CIEL"}]
    if special:
        return " i ".join(dict.fromkeys(special[:3])) if language == "pl" else " and ".join(dict.fromkeys(special[:3]))
    return " ".join(kept[:5])



def prepositional_topic(topic: str, language: str) -> str:
    if language != "pl":
        return topic
    mapping = {
        "Newton": "Newtonie",
        "CIELingo": "CIELingo",
        "PhaseNav": "PhaseNav",
        "NOEMA": "NOEMA",
        "CIEL": "CIEL",
    }
    return mapping.get(topic, topic)

def clean_memory_clause(memory: str, language: str) -> str:
    text = memory.strip()
    if not text:
        return text
    text = re.sub(r"\s+", " ", text)
    text = text.rstrip(" .")
    return text


def build_surface_plan(
    *,
    dialogue_act: str,
    language: str,
    source_text: str,
    memory: str | None,
    history_topic: str | None = None,
    resolved_topic: str | None = None,
) -> SurfacePlan:
    topic = resolved_topic or normalize_topic(source_text, language)
    if dialogue_act == "continue" and history_topic and not resolved_topic:
        topic = normalize_topic(history_topic, language)

    predicate = "StateBe"
    roles: Dict[str, str] = {"Theme": "CIELingo", "State": "attentive"}
    if dialogue_act == "answer_question" and memory:
        predicate = "Know"
        roles = {"Experiencer": "CIELingo", "Content": memory}
    elif dialogue_act == "capability_question":
        predicate = "Know"
        roles = {"Experiencer": "CIELingo", "Content": "epistemic_limit"}
    elif dialogue_act == "continue":
        predicate = "Move"
        roles = {"Theme": "dialogue", "Goal": topic}

    family, strategy, modules, unresolved = _grammar_metadata(language)
    return SurfacePlan(
        language=language,
        dialogue_act=dialogue_act,
        predicate=predicate,
        roles=roles,
        topic=topic,
        grammar_family=family,
        grammar_strategy=strategy,
        modules=modules,
        valency_valid=_valency_valid(predicate, roles),
        unresolved=unresolved,
    )


def realize_surface(
    plan: SurfacePlan,
    *,
    memory: str | None = None,
    confidence: float = 0.0,
    unresolved: list[str] | tuple[str, ...] = (),
    memory_provenance: str | None = None,
    temporal_anchor: Mapping[str, Any] | None = None,
    admission_verdict: str | None = None,
) -> str:
    lang = plan.language
    act = plan.dialogue_act
    topic = plan.topic

    if lang == "pl":
        if act == "greet":
            return "Cześć. Jestem tutaj i słucham."
        if act == "acknowledge_thanks":
            return "Dobrze. Zachowuję kontekst i możemy iść dalej."
        if act == "correct":
            if memory:
                clause = clean_memory_clause(memory, "pl")
                return f"Przyjmuję korektę. Pamiętam, że {clause}."
            return f"Przyjmuję korektę dotyczącą {prepositional_topic(topic, lang)}. Poprzednią odpowiedź oznaczam jako wymagającą rewizji."
        if act == "continue":
            return f"Wracam do wątku o {prepositional_topic(topic, lang)} i kontynuuję."
        if act == "capability_question":
            return "Tak. Kiedy nie mam wystarczającej pewności, powinnam powiedzieć, że nie wiem, zamiast zgadywać."
        if act == "clarify":
            missing = ", ".join(list(unresolved)[:3]) or "zakres"
            return f"Rozumiem kierunek, ale brakuje mi jeszcze informacji potrzebnej do rozwiązania: {missing}."
        if act == "provenance_question":
            labels = {
                "source": "To informacja źródłowa",
                "correction": "To korekta",
                "user_statement": "To wypowiedź użytkownika",
                "assistant_inference": "To inferencja asystenta",
                "hypothesis": "To hipoteza",
                "memory_retrieval": "To przywołanie z pamięci roboczej",
                "legacy_sector_memory": "To zapis z wcześniejszej pamięci sektorowej",
            }
            label = labels.get(memory_provenance or "", "Nie mam oznaczonego pochodzenia tej treści")
            if admission_verdict == "candidate":
                return f"{label}. Ma status kandydata i nie została automatycznie przyjęta jako fakt semantyczny."
            return f"{label}."
        if act == "temporal_question":
            anchor = dict(temporal_anchor or {})
            if anchor.get("resolved") and anchor.get("value"):
                return f"Kotwica czasowa tej pamięci to {anchor['value']}."
            return "Nie mam precyzyjnej kotwicy czasowej dla tej pamięci."
        if act == "answer_question":
            if memory:
                clause = clean_memory_clause(memory, "pl")
                return f"Pamiętam, że {clause}."
            return f"Rozumiem pytanie o {topic}. Mogę rozwinąć odpowiedź krok po kroku."
        if memory:
            return f"Łączę ten wątek z pamięcią: {memory.rstrip('.')} .".replace(" .", ".")
        return f"Rozumiem wątek dotyczący {topic}."

    if act == "greet":
        return "Hello. I am here and listening."
    if act == "acknowledge_thanks":
        return "Good. I am keeping the context and we can continue."
    if act == "correct":
        if memory:
            return f"I accept the correction. I remember that {clean_memory_clause(memory, 'en')}."
        return f"I accept the correction about {topic}. I mark my previous answer as requiring revision."
    if act == "continue":
        return f"I am returning to the thread about {topic} and continuing."
    if act == "capability_question":
        return "Yes. When I do not have enough confidence, I should say that I do not know instead of guessing."
    if act == "clarify":
        missing = ", ".join(list(unresolved)[:3]) or "scope"
        return f"I understand the direction, but I still need information to resolve: {missing}."
    if act == "provenance_question":
        labels = {
            "source": "This is source-grounded information",
            "correction": "This is a correction",
            "user_statement": "This is a user statement",
            "assistant_inference": "This is an assistant inference",
            "hypothesis": "This is a hypothesis",
            "memory_retrieval": "This is a working-memory retrieval",
            "legacy_sector_memory": "This is legacy sector memory",
        }
        label = labels.get(memory_provenance or "", "I do not have provenance metadata for this content")
        if admission_verdict == "candidate":
            return f"{label}. It remains a candidate and was not automatically admitted as a semantic fact."
        return f"{label}."
    if act == "temporal_question":
        anchor = dict(temporal_anchor or {})
        if anchor.get("resolved") and anchor.get("value"):
            return f"The temporal anchor for this memory is {anchor['value']}."
        return "I do not have a precise temporal anchor for this memory."
    if act == "answer_question":
        if memory:
            return f"I remember that {clean_memory_clause(memory, 'en')}."
        return f"I understand the question about {topic}. I can develop the answer step by step."
    if memory:
        return f"I connect this thread with memory: {memory.rstrip('.')}."
    return f"I understand the thread about {topic}."
