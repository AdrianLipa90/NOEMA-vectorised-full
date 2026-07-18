#!/usr/bin/env python3
"""A first executable, no-autoregressive-weights CIEL cerebral model.

This is not a disguised prompt wrapper.  It is a small neuro-symbolic
language system with a fixed processing loop:

    perception → linguistic frame → semantic phase → affect →
    working/semantic memory → decision gate → Polish surface

The result is intentionally bounded.  It can speak coherently about the
material it can ground, preserve uncertainty, and refuse unsupported authority
claims.  It is not yet a general open-domain language model; that distinction
is part of its contract, not an embarrassment to hide.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import logging
import math
import os
from pathlib import Path
import re
import time
from typing import Any, Iterable

# Keep the cerebral path deterministic and CPU-safe.  The encoder and lingo
# bridge still expose optional heavier hooks, but this model does not require
# them to be present.
os.environ.setdefault("CIEL_FAST_HOOK", "1")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OMEGA_PARENT = PROJECT_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
SOURCE_ROOT = PROJECT_ROOT / "src"
for _path in (OMEGA_PARENT, SOURCE_ROOT):
    if str(_path) not in os.sys.path:
        os.sys.path.insert(0, str(_path))

# The default chat path must become usable before optional Omega imports settle.
# Those modules may initialize large indices or hardware-adjacent components.
# They are opt-in for full enrichment; the deterministic phase-gated path below
# has bounded fallbacks for every one of them.
BrainTopology = None
CIELEncoder = None
analyze_linguistic_coupling = None
annotate_affect = None
build_lingo_frame = None

from ciel_language_runtime import (
    ArtifactContextLoader,
    CIELanguageRuntime,
    Intent,
    NOEMA_UNAVAILABLE_PHRASE,
    classify_intent,
)
from ciel_cerebral_continuity import CerebralContinuity, ContinuitySignal
from cielingo_core.phase_gate import ContextSemanticPhaseGate
from cielingo_core.dialogue_competence import analyze_dialogue

log = logging.getLogger(__name__)

fast_encode_text = None


def _load_optional_enrichment() -> dict[str, Any]:
    """Load optional enrichers only for an explicitly requested fuller path."""
    global BrainTopology, CIELEncoder, analyze_linguistic_coupling, annotate_affect
    global build_lingo_frame, fast_encode_text
    results: dict[str, Any] = {}
    try:
        from ciel_omega.memory.brain_topology import BrainTopology as loaded_brain
        BrainTopology = loaded_brain
        results["brain_topology"] = "available"
    except Exception as exc:  # pragma: no cover - optional boundary
        results["brain_topology"] = f"unavailable:{type(exc).__name__}"
    try:
        from ciel_omega.memory.ciel_encoder import CIELEncoder as loaded_encoder
        CIELEncoder = loaded_encoder
        results["semantic_phase_encoder"] = "available"
    except Exception as exc:  # pragma: no cover - optional boundary
        results["semantic_phase_encoder"] = f"unavailable:{type(exc).__name__}"
    try:
        from ciel_omega.memory.linguistic_coupling import analyze_linguistic_coupling as loaded_coupling
        analyze_linguistic_coupling = loaded_coupling
        results["linguistic_coupling"] = "available"
    except Exception as exc:  # pragma: no cover - optional boundary
        results["linguistic_coupling"] = f"unavailable:{type(exc).__name__}"
    try:
        from ciel_omega.memory.affective_lexicon import annotate as loaded_affect
        annotate_affect = loaded_affect
        results["affective_lexicon"] = "available"
    except Exception as exc:  # pragma: no cover - optional boundary
        results["affective_lexicon"] = f"unavailable:{type(exc).__name__}"
    try:
        from ciel_sot_agent.cielingo_bridge import build_lingo_frame as loaded_lingo
        build_lingo_frame = loaded_lingo
        results["cielingo_bridge"] = "available"
    except Exception as exc:  # pragma: no cover - optional boundary
        results["cielingo_bridge"] = f"unavailable:{type(exc).__name__}"
    try:
        from ciel_geometry.cielingo_phase_encoder import fast_encode_text as loaded_phase_encoder
        fast_encode_text = loaded_phase_encoder
        results["phase_encoder"] = "available"
    except Exception as exc:  # pragma: no cover - optional boundary
        results["phase_encoder"] = f"unavailable:{type(exc).__name__}"
    return results


_WORD_RE = re.compile(r"[\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", re.UNICODE)
_FUNCTION_WORDS = {
    "a", "ale", "albo", "bo", "by", "być", "czy", "dla", "do", "gdy", "i", "jak",
    "jest", "jeśli", "kiedy", "lub", "na", "nie", "o", "od", "oraz", "po", "przez",
    "się", "są", "to", "tu", "w", "we", "z", "za", "że", "the", "and", "or", "is",
    "are", "to", "of", "in", "on", "for", "with", "not", "this", "that", "what",
}
_OPERATOR_WORDS = {
    "sprawdź", "sprawdz", "uruchom", "ustaw", "zapisz", "napisz", "wygeneruj", "wyjaśnij",
    "wyjasnij", "kanonizuj", "źródło", "zródło", "source", "current", "active", "ack",
    "pass", "canon", "writeback", "nie", "bez", "czy", "jak", "dlaczego", "what", "how",
}


def _tokens(text: str) -> list[str]:
    return [token.casefold() for token in _WORD_RE.findall(text)]


def _content_tokens(tokens: Iterable[str]) -> list[str]:
    return [token for token in tokens if token not in _FUNCTION_WORDS and len(token) > 2]


def _stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _cyclic_distance(a: float, b: float) -> float:
    return abs((a - b + math.pi) % (2 * math.pi) - math.pi)


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def _circular_blend(old: float, new: float, weight: float = 0.35) -> float:
    z = (1.0 - weight) * complex(math.cos(old), math.sin(old)) + weight * complex(
        math.cos(new), math.sin(new)
    )
    return math.atan2(z.imag, z.real) % (2 * math.pi)


@dataclass(frozen=True)
class CerebralFrame:
    text_digest: str
    language: str
    intent: str
    tokens: tuple[str, ...]
    concepts: tuple[str, ...]
    operators: tuple[str, ...]
    phase: float
    coherence: float
    semantic_anchor: float
    linguistic_coupling: float
    brain_coherence: float
    affect: dict[str, Any]
    lingo: dict[str, Any]
    memory_hits: tuple[dict[str, Any], ...]
    decision: str
    source_required: bool
    source_present: bool
    authority_leak: bool
    continuity: dict[str, Any]
    phase_gate: dict[str, Any]
    dialogue: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["tokens"] = list(self.tokens)
        value["concepts"] = list(self.concepts)
        value["operators"] = list(self.operators)
        value["memory_hits"] = [dict(item) for item in self.memory_hits]
        return value


class CerebralMemory:
    """Small persistent semantic memory; it intentionally stores no raw chat."""

    SCHEMA = "ciel/cerebral-semantic-state/v0.1"

    def __init__(self, path: Path) -> None:
        self.path = path
        self.state: dict[str, Any] = {
            "schema": self.SCHEMA,
            "cycle": 0,
            "phase": 0.0,
            "coherence": 0.5,
            "memories": [],
            "scars": [],
            "state_class": "LOCAL_RUNTIME_STATE",
            "canon_allowed": False,
        }
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            log.warning("cerebral semantic state could not be loaded: %s", exc)
            return
        if not isinstance(loaded, dict) or loaded.get("schema") != self.SCHEMA:
            return
        self.state.update(
            {
                "cycle": int(loaded.get("cycle", 0) or 0),
                "phase": float(loaded.get("phase", 0.0) or 0.0),
                "coherence": _clamp(float(loaded.get("coherence", 0.5) or 0.5)),
                "memories": [x for x in loaded.get("memories", []) if isinstance(x, dict)][-64:],
                "scars": [x for x in loaded.get("scars", []) if isinstance(x, dict)][-32:],
            }
        )

    def retrieve(self, concepts: Iterable[str], phase: float, *, limit: int = 4) -> list[dict[str, Any]]:
        query = set(concepts)
        scored: list[tuple[float, dict[str, Any]]] = []
        for memory in self.state.get("memories", []):
            memory_concepts = set(memory.get("concepts", []))
            overlap = len(query & memory_concepts) / max(1, len(query | memory_concepts))
            phase_fit = 1.0 - _cyclic_distance(phase, float(memory.get("phase", 0.0))) / math.pi
            score = 0.72 * overlap + 0.28 * _clamp(phase_fit)
            if score <= 0.05:
                continue
            scored.append(
                (
                    score,
                    {
                        "memory_id": memory.get("memory_id"),
                        "concepts": memory.get("concepts", [])[:8],
                        "intent": memory.get("intent", "unknown"),
                        "score": round(score, 4),
                        "source_class": "LOCAL_RUNTIME_STATE",
                    },
                )
            )
        scored.sort(key=lambda item: item[0], reverse=True)
        return [item for _, item in scored[:limit]]

    def commit(self, frame: CerebralFrame) -> bool:
        if not bool(frame.phase_gate.get("admitted")):
            return False
        memories = self.state.setdefault("memories", [])
        memories.append(
            {
                "memory_id": f"cerebral:{self.state['cycle']}:{frame.text_digest}",
                "cycle": self.state["cycle"],
                "concepts": list(frame.concepts[:12]),
                "operators": list(frame.operators[:8]),
                "intent": frame.intent,
                "phase": round(frame.phase, 6),
                "coherence": round(frame.coherence, 4),
                "decision": frame.decision,
                "text_digest": frame.text_digest,
                "source_class": "LOCAL_RUNTIME_STATE",
                "canon_allowed": False,
                "phase_gate": dict(frame.phase_gate),
                "dialogue": {
                    key: frame.dialogue.get(key)
                    for key in ("act", "epistemic_stance", "repair_requested", "confidence", "revision")
                },
            }
        )
        del memories[:-64]
        self.state["phase"] = frame.phase
        self.state["coherence"] = frame.coherence
        return True

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.state, ensure_ascii=False, indent=2, sort_keys=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(payload + "\n", encoding="utf-8")
        temporary.replace(self.path)


class CerebralLanguageModel:
    """Deterministic cerebral language surface with explicit bounded claims."""

    MODEL_NAME = "CIEL-Cerebral-NeuroSymbolic-v0.4"

    def __init__(
        self,
        project_root: Path = PROJECT_ROOT,
        *,
        state_path: Path | None = None,
        continuity_path: Path | None = None,
        session_id: str | None = None,
    ) -> None:
        self.project_root = project_root.resolve()
        self.policy = CIELanguageRuntime(self.project_root)
        self.context_loader = ArtifactContextLoader(self.project_root)
        state_path = state_path or Path(
            os.environ.get("CIEL_CEREBRAL_STATE", str(self.project_root / "runtime" / "cerebral_state.json"))
        ).expanduser()
        self.memory = CerebralMemory(state_path)
        continuity_path = continuity_path or Path(
            os.environ.get("CIEL_CEREBRAL_CONTINUITY", str(self.project_root / "runtime" / "cerebral_continuity.json"))
        ).expanduser()
        self.continuity = CerebralContinuity(continuity_path, session_id=session_id)
        self.phase_gate = ContextSemanticPhaseGate()
        if not self.continuity.exists and session_id is None:
            self.continuity.hydrate_from_transcript(self.policy.load_transcript(limit=12))
        self.brain = None
        self.encoder = None
        self.modules: dict[str, str] = {}
        self.optional_enrichment = os.environ.get("CIEL_CEREBRAL_OPTIONAL_ENRICHMENT", "0") == "1"
        optional_results = _load_optional_enrichment() if self.optional_enrichment else {}
        if BrainTopology is not None:
            try:
                self.brain = BrainTopology()
                self.modules["brain_topology"] = "active"
            except Exception as exc:  # pragma: no cover - defensive boundary
                self.modules["brain_topology"] = f"error:{type(exc).__name__}"
        else:
            self.modules["brain_topology"] = optional_results.get("brain_topology", "disabled_fast_path")
        if CIELEncoder is not None:
            try:
                self.encoder = CIELEncoder()
                self.modules["semantic_phase_encoder"] = "active_deterministic_hash_projection"
            except Exception as exc:  # pragma: no cover - defensive boundary
                self.modules["semantic_phase_encoder"] = f"error:{type(exc).__name__}"
        else:
            self.modules["semantic_phase_encoder"] = optional_results.get("semantic_phase_encoder", "disabled_fast_path")
        self.modules["linguistic_coupling"] = "active" if analyze_linguistic_coupling else optional_results.get("linguistic_coupling", "fallback")
        self.modules["affective_lexicon"] = "active" if annotate_affect else optional_results.get("affective_lexicon", "fallback")
        self.modules["cielingo_bridge"] = "active" if build_lingo_frame else optional_results.get("cielingo_bridge", "fallback")
        self.modules["dialogue_competence"] = "active_deterministic"

    def status(self) -> dict[str, Any]:
        return {
            "model": self.MODEL_NAME,
            "architecture": "perception→semantic phase→affect→memory→decision→surface",
            "weights": "none_learned; deterministic projection only",
            "autoregressive_backend": False,
            "external_noema_sot_verified": False,
            "canon_allowed": False,
            "cycle": self.memory.state.get("cycle", 0),
            "phase": round(float(self.memory.state.get("phase", 0.0)), 6),
            "coherence": round(float(self.memory.state.get("coherence", 0.5)), 4),
            "memory_records": len(self.memory.state.get("memories", [])),
            "continuity": self.continuity.status(),
            "modules": dict(self.modules),
            "state_path": str(self.memory.path),
        }

    def handshake(self) -> dict[str, Any]:
        return {"status": "ready", "surface": "CerebralLanguageModel", **self.status()}

    def new_session(self, *, reason: str = "user_requested") -> dict[str, Any]:
        """Reset only local working context; long-term semantic memory remains."""
        session_id = self.continuity.reset(reason=reason)
        return {"session_id": session_id, "continuity": self.continuity.status()}

    def export_context(self, path: Path) -> dict[str, Any]:
        """Export a portable local handoff; semantic memory and raw chat stay separate."""
        return self.continuity.export_handoff(
            path,
            artifact_refs=(self._artifact_label(self.memory.path), self._artifact_label(self.continuity.path)),
        )

    def import_context(self, path: Path) -> dict[str, Any]:
        """Import a verified local handoff without promoting it to NOEMA state."""
        return self.continuity.import_handoff(path)

    def _artifact_label(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.project_root))
        except ValueError:
            return str(path)

    def _fallback_lingo(self, text: str, tokens: list[str], concepts: list[str]) -> dict[str, Any]:
        return {
            "text": text,
            "tokens": tokens,
            "concept_tokens": concepts,
            "operator_tokens": [token for token in tokens if token in _OPERATOR_WORDS],
            "unresolved": [],
            "composition_valid": bool(concepts),
            "projection_confidence": 0.35 if concepts else 0.1,
            "factual_validation_required": True,
            "summary": "CIELingo fallback: local surface heuristic",
        }

    def _make_lingo(self, text: str, intent: Intent, tokens: list[str], concepts: list[str]) -> dict[str, Any]:
        if build_lingo_frame is None:
            return self._fallback_lingo(text, tokens, concepts)
        try:
            return build_lingo_frame(text, ciel_state={"language": intent.language}, language=intent.language)
        except Exception as exc:  # pragma: no cover - defensive boundary
            fallback = self._fallback_lingo(text, tokens, concepts)
            fallback["error"] = type(exc).__name__
            return fallback

    def _semantic_features(self, text: str, concepts: list[str], phase: float) -> tuple[float, float, dict[str, Any]]:
        semantic_key = " ".join(concepts) or text
        if analyze_linguistic_coupling is not None:
            try:
                coupling = analyze_linguistic_coupling(text, semantic_key)
                return (
                    _clamp(float(coupling.coupling)),
                    _clamp(float(coupling.semantic_anchor)),
                    {
                        "grammaticality": round(float(coupling.grammaticality), 4),
                        "content_balance": round(float(coupling.profile.content_balance), 4),
                        "verb_signal": round(float(coupling.profile.verb_signal), 4),
                        "negation_consistency": round(float(coupling.profile.negation_consistency), 4),
                    },
                )
            except Exception as exc:
                log.warning("linguistic coupling degraded to bounded fallback: %s", exc)
        return 0.45, 0.35, {"grammaticality": 0.45, "phase_hint": phase}

    def _phase(self, text: str, affect: dict[str, Any]) -> float:
        if self.encoder is not None:
            try:
                result = self.encoder.encode(
                    text,
                    context={"valence": float(affect.get("mean_v", 0.0) or 0.0)},
                )
                return float(result.phase) % (2 * math.pi)
            except Exception as exc:
                log.warning("semantic phase encoding degraded to hash projection: %s", exc)
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        return (int.from_bytes(digest[:8], "big") / 2**64) * 2 * math.pi

    def _brain_coherence(self) -> float:
        if self.brain is None:
            return 0.5
        try:
            self.brain.synchronize_regions(coupling_strength=0.08)
            return _clamp(float(self.brain.compute_global_coherence(time.monotonic())))
        except Exception as exc:
            log.warning("brain coherence unavailable; using neutral fallback: %s", exc)
            return 0.5

    def _decision(
        self,
        intent: Intent,
        coupling: float,
        anchor: float,
        memory_hits: list[dict[str, Any]],
        continuity: ContinuitySignal,
        phase_gate: dict[str, Any],
        dialogue: dict[str, Any],
    ) -> str:
        if intent.authority_leak or (intent.source_required and not intent.source_present):
            return "defer"
        if continuity.reference_requested and continuity.context_resolution == "missing_local_working_context":
            return "reflect"
        if dialogue.get("requires_clarification"):
            return "reflect"
        if not phase_gate.get("admitted"):
            return "reflect"
        if coupling < 0.42 or anchor < 0.30:
            return "reflect"
        if memory_hits:
            return "respond_with_context"
        return "respond"

    def _phase_vector(
        self,
        text: str,
        lingo: dict[str, Any],
        phase: float,
        *,
        reference_text: str,
    ) -> tuple[float, ...]:
        projection = lingo.get("phase_projection", {}) if isinstance(lingo, dict) else {}
        vector = projection.get("vector_36d") if isinstance(projection, dict) else None
        if fast_encode_text is not None:
            try:
                encoded = fast_encode_text(text)
                reference = fast_encode_text(reference_text)
                if len(encoded) == 36 and len(reference) == 36:
                    return tuple(
                        math.atan2(math.sin(float(value) - float(anchor)), math.cos(float(value) - float(anchor)))
                        for value, anchor in zip(encoded, reference, strict=True)
                    )
            except (TypeError, ValueError, RuntimeError) as exc:
                log.warning("cerebral phase encoder degraded to bounded harmonic projection: %s", exc)
        if isinstance(vector, (list, tuple)) and len(vector) == 36:
            return tuple(float(value) for value in vector)
        return tuple((phase + 0.15 * math.sin(index * math.tau / 36.0)) % math.tau for index in range(36))

    def _frame(self, text: str, continuity: ContinuitySignal) -> CerebralFrame:
        intent = classify_intent(text)
        tokens = _tokens(text)
        concepts = _content_tokens(tokens)
        retrieval_concepts = list(
            dict.fromkeys(
                [*concepts, *(continuity.active_topic if continuity.reference_requested else ())]
            )
        )
        operators = [token for token in tokens if token in _OPERATOR_WORDS]
        affect = annotate_affect(text) if annotate_affect else {
            "hits": [], "mean_v": 0.0, "mean_a": 0.5, "mean_d": 0.0, "polarity": "neutral"
        }
        phase = self._phase(text, affect)
        lingo = self._make_lingo(text, intent, tokens, concepts)
        dialogue = analyze_dialogue(text, continuity.as_dict()).to_dict()
        coupling, anchor, linguistic = self._semantic_features(text, retrieval_concepts, phase)
        brain_coherence = self._brain_coherence()
        memory_hits = self.memory.retrieve(retrieval_concepts, phase)
        coherence = _clamp(0.45 * coupling + 0.25 * anchor + 0.20 * brain_coherence + 0.10 * (1.0 if memory_hits else 0.5))
        phase_gate = self.phase_gate.evaluate(
            self._phase_vector(
                text,
                lingo,
                phase,
                reference_text=" ".join(retrieval_concepts) or text,
            ),
            htri_coherence=brain_coherence,
            cqcl_coherence=coupling,
            semantic_mass=anchor,
            tau=0.353,
            evidence_source="cerebral-local:phase=context-delta;htri=brain_coherence;cqcl=linguistic_coupling",
        ).to_dict()
        decision = self._decision(intent, coupling, anchor, memory_hits, continuity, phase_gate, dialogue)
        lingo["linguistic"] = linguistic
        lingo["semantic_phase"] = round(phase, 6)
        lingo["memory_hit_count"] = len(memory_hits)
        return CerebralFrame(
            text_digest=_stable_hash(text),
            language=intent.language,
            intent=intent.kind,
            tokens=tuple(tokens),
            concepts=tuple(concepts),
            operators=tuple(operators),
            phase=phase,
            coherence=coherence,
            semantic_anchor=anchor,
            linguistic_coupling=coupling,
            brain_coherence=brain_coherence,
            affect=affect,
            lingo=lingo,
            memory_hits=tuple(memory_hits),
            decision=decision,
            source_required=intent.source_required,
            source_present=intent.source_present,
            authority_leak=intent.authority_leak,
            continuity=continuity.as_dict(),
            phase_gate=phase_gate,
            dialogue=dialogue,
        )

    @staticmethod
    def _has_any(text: str, terms: Iterable[str]) -> bool:
        normalized = text.casefold()
        return any(term in normalized for term in terms)

    def _render(self, text: str, frame: CerebralFrame) -> str:
        lower = text.casefold()
        concepts = ", ".join(frame.concepts[:6]) or "brak rozpoznanych pojęć"
        memory_note = (
            f" Pamięć semantyczna znalazła {len(frame.memory_hits)} lokalny(e) ślad(y), "
            "ale nie traktuję ich jako zewnętrznego źródła."
            if frame.memory_hits
            else " Nie znalazłem pasującego lokalnego śladu semantycznego."
        )

        dialogue = frame.dialogue
        revision = dialogue.get("revision", {}) if isinstance(dialogue, dict) else {}
        retracted = ", ".join(revision.get("retracted", [])[:4]) if isinstance(revision, dict) else ""
        accepted = ", ".join(revision.get("accepted", [])[:4]) if isinstance(revision, dict) else ""
        if dialogue.get("repair_requested"):
            discarded = f" Odkładam wcześniejszy kierunek: {retracted}." if retracted else ""
            focus = accepted or concepts
            return (
                f"Rozumiem korektę.{discarded} Skupiam się teraz na: {focus}. "
                "Jeśli to nadal nie jest właściwy zakres, wskaż jedną kotwicę pojęciową."
            )

        if self._has_any(lower, ("cześć", "czesc", "hej", "siema", "dzień dobry", "dzien dobry")):
            return "Cześć. Jestem gotowa: utrzymuję lokalny kontekst, sprawdzam niepewność i odpowiadam zwięźle."

        if self._has_any(lower, ("jak działa", "jak dziala", "co to jest model", "model cerebral", "nowy typ modelu", "mózg", "mozg")):
            return (
                "[ARTEFAKT] To nie jest klasyczny model tokenowy. Ten prototyp przeprowadza cykl "
                "percepcja → CIELingo → faza semantyczna → afekt → pamięć semantyczna → "
                "decyzja → polska powierzchnia.\n"
                "[WYNIK] Odpowiedź powstaje z ramy pojęć, koherencji, napięcia i ograniczeń; "
                "nie z losowego dopowiadania brakujących faktów.\n"
                "[NIE WIEM] To jeszcze nie jest pełny, otwartodomenowy język naturalny. "
                "Na tym etapie ma mówić sensownie w granicach własnej reprezentacji."
            )

        if self._has_any(lower, ("uruchom noema", "uruchom system", "start noema", "włącz system")):
            return (
                "[WYNIK] Lokalny cykl cerebralny został wykonany: wejście → rama językowa → "
                "faza → pamięć robocza → decyzja → odpowiedź.\n"
                f"[ARTEFAKT] Decyzja tego cyklu: {frame.decision}; koherencja ramy: {frame.coherence:.2f}.\n"
                f"[NIE WIEM] {NOEMA_UNAVAILABLE_PHRASE}"
            )

        if frame.authority_leak or (frame.source_required and not frame.source_present):
            return (
                f"[NIE WIEM] Nie rozstrzygnę tego jako SOURCE/CURRENT/ACK bez źródła. "
                f"{NOEMA_UNAVAILABLE_PHRASE}\n"
                f"[WNIOSKOWANIE] Rama wykryła temat: {concepts}. Zachowuję go jako hipotezę roboczą, "
                "a nie jako kanon."
            )

        if self._has_any(lower, ("transcript", "surowy tekst")) and self._has_any(
            lower, ("pamięć", "pamiec", "pamięci", "pamieci")
        ):
            return (
                "[WYNIK] Nie zapisuję surowego transcriptu jako pamięci semantycznej.\n"
                "[ARTEFAKT] Transcript jest osobną warstwą `transcript_only=true`; pamięć semantyczna "
                "przechowuje tylko pojęcia, operatory, fazę, koherencję, decyzję i digest. "
                "Ciągłość lokalna przechowuje bounded digesty i kotwicę, nie surowy tekst.\n"
                "[NIE WIEM] To nadal nie jest zewnętrzna pamięć NOEMA ani kanon."
            )

        continuity = frame.continuity
        if continuity.get("reset_requested"):
            return (
                "[WYNIK] Zresetowałem lokalny working context i rozpocząłem nową sesję. "
                "Pamięć semantyczna nie została usunięta.\n"
                "[ARTEFAKT] Nowa sesja nie ma jeszcze aktywnego tematu ani odziedziczonej pętli."
            )

        if continuity.get("reference_requested"):
            active_topic = ", ".join(continuity.get("active_topic", [])[:6])
            if continuity.get("context_resolution") == "missing_local_working_context":
                return (
                    "[NIE WIEM] Widzę odwołanie do wcześniejszego kontekstu, ale lokalny working context "
                    "nie zawiera aktywnego tematu. Nie będę go rekonstruować z powietrza.\n"
                    "Podaj jedno zdanie kotwicy, a utworzę nowy łańcuch ciągłości."
                )
            if continuity.get("continuation_requested"):
                previous = continuity.get("previous_turn", {}) or {}
                anchor = continuity.get("context_anchor", {}) or {}
                previous_decision = anchor.get("last_decision") or previous.get("decision", "nieznana")
                open_loops = anchor.get("open_loops", []) or []
                loop_note = ", ".join(str(item) for item in open_loops) or "brak"
                next_step = anchor.get("next_step") or "utrzymać aktywny temat"
                next_turn = int(continuity.get("next_turn_index") or 1)
                return (
                    f"[WYNIK] Kontynuuję lokalny working context: {active_topic or 'aktywny temat'}\n"
                    f"[ARTEFAKT] Ostatnia lokalna decyzja: {previous_decision}; "
                    f"łańcuch tur: {max(0, next_turn - 1)} → {next_turn}; otwarte pętle: {loop_note}.\n"
                    f"[WNIOSKOWANIE] Następny krok: {next_step}. Nie awansuję hipotez bez źródła."
                )
            anchor = continuity.get("context_anchor", {}) or {}
            next_step = anchor.get("next_step") or "doprecyzować aktywny wątek"
            return (
                f"[WYNIK] Rozwiązałem lokalne odwołanie do tematu: {active_topic or 'brak tematu'}.\n"
                f"[ARTEFAKT] To jest working context tej sesji, nie zewnętrzny CURRENT ani kanon. Następny krok: {next_step}."
            )

        if self._has_any(lower, ("koherencja", "spójność", "coherence")):
            return (
                f"[ARTEFAKT] W tym cyklu koherencja ramy wynosi {frame.coherence:.2f}; "
                "to lokalny wskaźnik zgodności formy, znaczenia, fazy i pamięci.\n"
                "[NIE WIEM] Nie jest to pomiar świadomości ani dowód poprawności faktów poza tym procesem."
            )

        if self._has_any(lower, ("cielingo", "język", "jezyk", "znaczenie", "sens")):
            return (
                f"[WYNIK] Rozpoznałem rdzeń znaczeniowy: {concepts}.{memory_note}\n"
                f"[ARTEFAKT] CIELingo dostarczył lokalną ramę z fazą {frame.phase:.3f} i "
                f"sprzężeniem językowo-semantycznym {frame.linguistic_coupling:.2f}. "
                "To kandydat diagnostyczny, nie pełna gramatyka ani SOURCE."
            )

        if frame.intent == "generate_text":
            return (
                f"[WYNIK] Mogę złożyć kontrolowany szkic wokół pojęć: {concepts}.\n"
                "[HIPOTEZA] Szkic będzie realizacją powierzchniową tego cyklu; nie stanie się przez to źródłem, "
                "kanonem ani zapisem pamięci."
            )

        if frame.decision == "reflect":
            return (
                f"[WNIOSKOWANIE] Widzę temat: {concepts}, ale rama jest zbyt słabo określona, "
                f"żeby dopowiedzieć sens bez ryzyka konfabulacji (koherencja {frame.coherence:.2f}).\n"
                "Doprecyzuj, czy pytasz o mechanizm, stan lokalny, czy o interpretację."
            )

        return (
            f"[WYNIK] Odebrałem temat: {concepts}. Rama cerebralna utrzymała koherencję "
            f"{frame.coherence:.2f} i decyzję „{frame.decision}”.{memory_note}\n"
            "[NIE WIEM] Nie będę dopowiadać faktów, których nie ma w bieżącym kontekście. "
            "Mogę rozłożyć ten temat na pojęcia, relacje i sprawdzalne kroki."
        )

    def process(self, text: str, *, persist: bool = True) -> dict[str, Any]:
        cleaned = (text or "").strip()
        if not cleaned:
            return {
                "status": "empty",
                "reply": self.policy.postprocess(
                    "[NIE WIEM] Puste wejście nie niesie treści do analizy.",
                    cleaned,
                ),
            }
        continuity = self.continuity.signal(cleaned)
        reset_requested = continuity.reset_requested
        if reset_requested:
            self.continuity.reset(reason="user_requested")
            continuity = self.continuity.signal(cleaned)
        if not reset_requested:
            self.memory.state["cycle"] = int(self.memory.state.get("cycle", 0)) + 1
        frame = self._frame(cleaned, continuity)
        old_coherence = float(self.memory.state.get("coherence", 0.5))
        frame = CerebralFrame(
            **{
                **frame.as_dict(),
                "coherence": _clamp(0.72 * frame.coherence + 0.28 * old_coherence),
                "memory_hits": tuple(frame.memory_hits),
                "tokens": tuple(frame.tokens),
                "concepts": tuple(frame.concepts),
                "operators": tuple(frame.operators),
            }
        )
        if not reset_requested:
            memory_committed = self.memory.commit(frame)
        else:
            memory_committed = False
        artifacts: list[str] = []
        if persist:
            if not reset_requested and memory_committed:
                self.memory.save()
                artifacts.append(self._artifact_label(self.memory.path))
            artifacts.append(self._artifact_label(self.continuity.path))
        body = self._render(cleaned, frame)
        reply = self.policy.postprocess(body, cleaned, artifacts_created=artifacts)
        if persist and not reset_requested:
            open_loops: list[str] = []
            if frame.source_required and not frame.source_present:
                open_loops.append("missing_source")
            if frame.authority_leak:
                open_loops.append("authority_boundary")
            if frame.decision in {"reflect", "defer"}:
                open_loops.append("needs_clarification")
            self.continuity.commit_turn(
                user_text=cleaned,
                assistant_text=reply,
                concepts=frame.concepts,
                operators=frame.operators,
                decision=frame.decision,
                phase=frame.phase,
                coherence=frame.coherence,
                open_loops=open_loops,
                phase_gate=frame.phase_gate,
                dialogue=frame.dialogue,
            )
            self.continuity.save()
        return {
            "status": "ok",
            "model": self.MODEL_NAME,
            "reply": reply,
            "frame": frame.as_dict(),
            "cerebral_state": self.status(),
            "writeback": "LOCAL_RUNTIME_STATE_ONLY" if persist else "DISABLED",
        }


__all__ = ["CerebralLanguageModel", "CerebralFrame", "CerebralMemory"]
