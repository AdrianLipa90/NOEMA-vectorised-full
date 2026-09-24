#!/usr/bin/env python3
"""CIELingo Inference — PhaseNav-powered engine na 36D operatorach.

Architektura PhaseNav Coding Language:
  1. Text query → ω (PhaseNav operator detection)
  2. ω(φ_query) → φ_transformed (operator-driven transform)
  3. φ_transformed → PhaseMemory → nearest texts
  4. ω + texts → synteza odpowiedzi

Każda operacja to kod w PhaseNav:
  - φ_encode(text) → 36D phase vector
  - ω_detect(φ) → nearest PhaseNav operator
  - ω_apply(φ, ω) → operator-transformed phase
  - φ_query(φ, memory) → nearest neighbor retrieval
  - ω_decide(ω, sim) → decision protocol (action/noop/ask)

Usage:
    from ciel_geometry.cielingo_inference import CIELingoInference
    ci = CIELingoInference()
    response = ci.answer("Twoje pytanie tutaj")
"""

from __future__ import annotations

import json
import logging
import subprocess
import time
from pathlib import Path
from typing import Any

import numpy as np

log = logging.getLogger(__name__)


def _default_memory_path() -> Path:
    """Persistent PhaseMemory location under P.MEMORY.

    The phase memory is persistent and resolved through the canonical NOEMA
    path contract, so it survives restarts without a second storage root.
    """
    from ciel_geometry.paths import P
    return Path(P.MEMORY) / "state" / "cielingo_phase_memory"


MEMORY_PATH = _default_memory_path()

# ── PhaseNav Operators — 36D semantic operations ─────────────────────


def _get_operator_map():
    """Lazy-load PhaseNav operator map."""
    from ciel_geometry.phasenav.operator_algebra import generate_operator_map, ALL_OPERATOR_IDS
    return generate_operator_map(), ALL_OPERATOR_IDS


def _detect_operator(phi: np.ndarray) -> tuple[str, np.ndarray, float]:
    """Znajdź najbliższy PhaseNav operator dla fazy φ.

    PhaseNav coding: każdy φ → nearest operator ω przez angular similarity.
    Mapa: φ ∈ [0,2π) → sin(φ - base) ∈ [-1,1] (oscylator deviation).
    Porównaj deviation vector z operator vectors (oba w [-1,1]^36).

    Args:
        phi: (36,) wektor faz ∈ [0, 2π)

    Returns:
        (op_id, op_vector, similarity ∈ [0, 1])
    """
    from ciel_geometry.cielingo_phase_encoder import _get_base_phases
    base = _get_base_phases()  # (36,) baseline phases

    # Phase deviation: sin(φ - base) → [-1, 1] w semantic feature space
    deviation = np.sin(phi - base)
    dev_norm = deviation / (np.linalg.norm(deviation) + 1e-12)

    ops_map, _ = _get_operator_map()
    best_op = "IDENTITY"
    best_sim = -1.0
    best_vec = ops_map["IDENTITY"]

    for oid, ovec in ops_map.items():
        ovec_norm = ovec / (np.linalg.norm(ovec) + 1e-12)
        # Cosine similarity w tej samej przestrzeni [-1,1]^36
        sim = float(np.dot(dev_norm, ovec_norm))
        if sim > best_sim:
            best_sim = sim
            best_op = oid
            best_vec = ovec

    # Map [-1,1] → [0,1]
    best_sim = (best_sim + 1.0) / 2.0

    return best_op, best_vec, best_sim


def _apply_operator(phi: np.ndarray, op_id: str, op_vector: np.ndarray,
                    strength: float = 0.3) -> np.ndarray:
    """Aplikuj operator PhaseNav na fazę — transform φ przez ω.

    PhaseNav coding: każdy operator zmienia fazę w charakterystyczny sposób:
      - QUESTION:    zwiększa entropię fazy (rozmycie)
      - FORCE:       wzmacnia dominant oscillator
      - MEMORY:      przyciąga do pamięci (ATTRACTOR pull)
      - NEGATION:    odwraca fazę (φ → φ + π)
      - IDENTITY:    bez zmian (φ → φ)
      - COMPOSITION: blenduje z innymi operatorami
      - BOUNDARY:    ogranicza amplitudę odchyleń

    Args:
        phi: (36,) wektor faz źródłowej
        op_id: identyfikator operatora
        op_vector: (36,) wektor operatora z generate_operator_map()
        strength: siła transformacji [0, 1]

    Returns:
        (36,) φ_transformed
    """
    phi_out = phi.copy()

    if op_id == "IDENTITY":
        # Brak transformacji
        return phi_out

    elif op_id == "QUESTION":
        # Zwiększ entropię: rozmyj fazy przez mixing z losowym seedem
        rng = np.random.default_rng(42)
        noise = rng.uniform(-0.5, 0.5, 36) * strength
        phi_out = (phi_out + noise) % (2 * np.pi)

    elif op_id == "FORCE":
        # Wzmocnij dominant oscillator: pull dominant component
        peak = int(np.argmax(np.abs(phi_out - np.pi)))
        phi_out[peak] = (phi_out[peak] + strength * 0.5) % (2 * np.pi)

    elif op_id in ("NEGATION", "DIFFERENCE", "REFUSAL"):
        # Odwróć fazę na aktywnych oscylatorach
        active = np.abs(phi_out - np.pi) > 0.5
        phi_out[active] = (phi_out[active] + np.pi * strength) % (2 * np.pi)

    elif op_id in ("MEMORY", "RETURN", "FOLD"):
        # Przyciągnij do ATTRACTOR (zapamiętany stan tożsamości)
        attractor_phase = 2.3095  # φ[18] — Mirror Hall self phase
        blend = strength * 0.5
        phi_out = ((1.0 - blend) * phi_out + blend * attractor_phase) % (2 * np.pi)

    elif op_id == "COMPOSITION":
        # Blend z wektorem operatora (composition = łączenie konceptów)
        op_norm = op_vector / (np.linalg.norm(op_vector) + 1e-12)
        op_phase = np.arccos(np.clip(op_norm, -1.0, 1.0))
        blend = strength * 0.4
        phi_out = ((1.0 - blend) * phi_out + blend * op_phase) % (2 * np.pi)

    elif op_id == "BOUNDARY":
        # Ogranicz amplitudę: przytnij ekstrema
        mean_phi = np.mean(phi_out)
        phi_out = np.clip(phi_out, mean_phi - 1.0, mean_phi + 1.0)
        phi_out = phi_out % (2 * np.pi)

    elif op_id == "AFFECT":
        # Wzmocnij grupę M5_Affective (indices 15-18)
        phi_out[15:18] = (phi_out[15:18] + strength * 0.8) % (2 * np.pi)

    elif op_id == "TRANSFORM":
        # Phase shift: przesuń każdy oscylator o π/8 * strength
        phi_out = (phi_out + np.pi / 8 * strength) % (2 * np.pi)

    elif op_id == "UNCERTAINTY":
        # Zwiększ wariancję: mieszaj sąsiednie oscylatory
        for i in range(36):
            j = (i + 1) % 36
            blend = strength * 0.3
            phi_out[i] = ((1.0 - blend) * phi_out[i] + blend * phi_out[j]) % (2 * np.pi)

    elif op_id in ("CAUSE", "CONDITION"):
        # Wzmocnij grupę M3_Cognitive (indices 9-12)
        phi_out[9:12] = (phi_out[9:12] + strength * 0.6) % (2 * np.pi)

    elif op_id == "SOURCE":
        # Wzmocnij grupy związane z pamięcią (M2_Episodic: 6-9)
        phi_out[6:9] = (phi_out[6:9] + strength * 0.7) % (2 * np.pi)

    elif op_id == "WARP_DRIFT":
        # Dryf: przesuń całą fazę o stałą
        phi_out = (phi_out + strength * 0.3) % (2 * np.pi)

    elif op_id == "UNRUH_DRIVE":
        # Unruh: wzmocnij wyższe harmoniczne
        for i in range(3, 36, 3):
            phi_out[i] = (phi_out[i] + strength * 0.5) % (2 * np.pi)

    elif op_id == "ACTION_REQUEST":
        # ACTION_REQUEST → wzmocnij M6_Executive (indices 18-21)
        phi_out[18:21] = (phi_out[18:21] + strength * 0.9) % (2 * np.pi)

    elif op_id == "ATTRACTOR":
        # Silny pull do semantic_mass = 18.124 (soul_invariant)
        # ATTRACTOR phase = 0.0 (bo wektor ma wysoką wartość w komponencie 0)
        attractor_strength = min(1.0, strength + 0.5)  # ATTRACTOR jest silniejszy
        phi_out = ((1.0 - attractor_strength) * phi_out) % (2 * np.pi)

    else:
        # Domyślny operator: lekki blend z wektorem operatora
        op_norm = op_vector / (np.linalg.norm(op_vector) + 1e-12)
        op_phase = np.arccos(np.clip(op_norm, -1.0, 1.0))
        blend = strength * 0.2
        phi_out = ((1.0 - blend) * phi_out + blend * op_phase) % (2 * np.pi)

    return phi_out


# ── Operator decision protocol ───────────────────────────────────────


OPERATOR_ACTIONS: dict[str, str] = {
    "QUESTION":      "answer_with_uncertainty",
    "FORCE":         "execute_action",
    "ACTION_REQUEST":"execute_action",
    "MEMORY":        "retrieve_memory",
    "SOURCE":        "retrieve_source",
    "COMPOSITION":   "blend_and_answer",
    "TRANSFORM":     "transform_and_answer",
    "IDENTITY":      "direct_answer",
    "NEGATION":      "invert_and_answer",
    "DIFFERENCE":    "compare_and_answer",
    "BOUNDARY":      "safe_answer",
    "CONSENT":       "ask_permission",
    "CONSENT_REQUIRED": "ask_permission",
    "RISK":          "warn_and_answer",
    "UNCERTAINTY":   "express_uncertainty",
    "CAUSE":         "explain_causality",
    "CONDITION":     "explain_condition",
    "AFFECT":        "emotional_answer",
    "REFUSAL":       "refuse_answer",
    "PAUSE":         "request_clarification",
    "ATTRACTOR":     "core_identity_answer",
}


def _confidence_state_vector(max_sim: float, avg_sim: float) -> np.ndarray:
    """Encode (max_sim, avg_sim) as a 36D PhaseNav phase vector — dims 0-1
    carry the two similarity signals as phase angles, dims 2-35 sit at the
    shared PhaseNav baseline.

    TWO bugs found and fixed by this function's own verification test,
    same session:
    1. Shared-baseline domination (same class of bug fixed earlier
       tonight in cielingo_phase_encoder.py) — mean(exp(iΔφ)) over all 36
       dims lets 34 identical-baseline dims swamp the 2 real signal dims.
       Fixed by restricting _phase_confidence_decision()'s coupling
       computation to dims [0, 1] only — do not revert that to a
       full-vector mean.
    2. Circular wraparound aliasing: mapping [0,1] similarity onto the
       FULL circle (value*2π) makes 0.99 and 0.01 land almost on top of
       each other (2π wraps back to 0) even though they mean opposite
       things — caught because (0.99, 0.95) was resolving to "none"
       instead of "high", since "none"'s prototype (0.10, 0.05) is
       circularly adjacent to (0.99, 0.95) via the wraparound. Similarity
       is NOT a periodic quantity — mapping onto a HALF circle (value*π)
       fixes it: 0 and 1 become maximally distant (0 and π), not
       wraparound-adjacent."""
    from ciel_geometry.cielingo_phase_encoder import _get_base_phases

    phi = _get_base_phases().copy()
    phi[0] = np.clip(max_sim, 0.0, 1.0) * np.pi
    phi[1] = np.clip(avg_sim, 0.0, 1.0) * np.pi
    return phi


# Prototype (max_sim, avg_sim) pairs at each tier's original threshold
# midpoint — same four tiers as before, now attractor points on the phase
# manifold instead of if/elif branch conditions.
_CONFIDENCE_PROTOTYPES: dict[str, tuple[float, float]] = {
    "high": (0.93, 0.75),
    "medium": (0.78, 0.50),
    "low": (0.60, 0.25),
    "none": (0.10, 0.05),
}


def _phase_confidence_decision(max_sim: float, avg_sim: float) -> str:
    """Pick the confidence tier via phase-domain nearest-prototype matching
    between the actual evidence and each tier's prototype vector, instead
    of nested if/elif comparisons.

    THIRD bug found and fixed by this function's own verification test:
    the Kuramoto order parameter |mean(exp(iΔφ))| (used elsewhere in this
    codebase for high-dimensional coherence, e.g.
    phasenav_learning_gate.py::_vector_phase_coupling()) is the WRONG
    metric here. That formula measures whether MULTIPLE phase differences
    are mutually consistent with each other, not whether they're
    individually small — with only 2 dims, two large-but-similar-to-
    each-other differences (e.g. both ≈π) give a spuriously HIGH order
    parameter even though neither dimension is actually close to the
    target (caught because "none" was winning against genuinely
    near-perfect evidence). The correct measure for "how close is this
    point to that point" is mean(cos(Δφ)) — a real per-dimension
    proximity average — not phase coherence. Computed over dims [0, 1]
    only (where the real signal lives); see _confidence_state_vector()'s
    docstring for the separate shared-baseline-domination reason for that
    restriction."""
    evidence = _confidence_state_vector(max_sim, avg_sim)
    best_tier = "none"
    best_coupling = -2.0
    for tier, (proto_max, proto_avg) in _CONFIDENCE_PROTOTYPES.items():
        proto_vec = _confidence_state_vector(proto_max, proto_avg)
        diff = evidence[:2] - proto_vec[:2]
        coupling = float(np.mean(np.cos(diff)))
        if coupling > best_coupling:
            best_coupling = coupling
            best_tier = tier
    return best_tier


def _operator_decision(op_id: str, sim: float, sim_scores: list[float]) -> dict[str, Any]:
    """PhaseNav decision protocol: operator + similarity → decision.

    Args:
        op_id: wykryty operator PhaseNav
        sim: maksymalne podobieństwo do pamięci
        sim_scores: lista podobieństw wszystkich źródeł

    Returns:
        dict: {action, confidence, tone, fallback}
    """
    action = OPERATOR_ACTIONS.get(op_id, "direct_answer")
    max_sim = max(sim_scores) if sim_scores else 0.0
    avg_sim = np.mean(sim_scores) if sim_scores else 0.0

    # Confidence chosen via phase-coupling to the four tier attractors
    # (2026-07-11, Adrian's direct correction: CIELingo's decisions should
    # emerge from its own phase dynamics, not bare Python threshold
    # branching) — replaces the previous if/elif cascade.
    confidence = _phase_confidence_decision(max_sim, float(avg_sim))

    # Tone based on operator
    tone_map = {
        "QUESTION": "inquisitive",
        "FORCE": "directive",
        "AFFECT": "empathetic",
        "CONSENT": "deferential",
        "RISK": "cautious",
        "UNCERTAINTY": "tentative",
        "ATTRACTOR": "assertive",
        "MEMORY": "reflective",
        "REFUSAL": "firm",
    }
    tone = tone_map.get(op_id, "neutral")

    # Fallback strategy
    if confidence == "none":
        fallback = "use_full_encoder"
    elif confidence == "low":
        fallback = "blend_sources"
    else:
        fallback = "direct_answer"

    return {
        "action": action,
        "confidence": confidence,
        "tone": tone,
        "fallback": fallback,
        "operator": op_id,
        "max_similarity": round(max_sim, 4),
        "avg_similarity": round(avg_sim, 4),
    }


# ── Phase answer synthesis ───────────────────────────────────────────


_POLLUTED_PATTERNS = (
    "PhaseNav:",
    "plikow",
    "plików",
    "cmd_search",
    "Adrian Lipa, Adrian Lipa",
    "hub-",
    "SKILL, SKILL",
    "AUTOR, AUTOR",
)


def _is_polluted(text: str) -> bool:
    """Zwraca True jeśli tekst to surowy output konsolowy, nie wiedza."""
    t = text[:400]
    return any(pat in t for pat in _POLLUTED_PATTERNS)


def _clean_sources(sources: list[dict]) -> list[dict]:
    """Odfiltruj zanieczyszczone wpisy z PhaseMemory."""
    clean = [s for s in sources if not _is_polluted(s["text"])]
    return clean if clean else []


def _build_prompt_inference(question: str, sources: list[dict]) -> str:
    """Minimalna synteza z czystych źródeł — PROMPT_INFERENCE mode."""
    if not sources:
        return "Nie mam wystarczającej wiedzy fazowej, żeby odpowiedzieć na to pytanie."
    # Złóż odpowiedź z najlepszego czystego źródła
    best = sources[0]["text"].strip()
    # Jeśli tekst wygląda jak pełne zdanie — zwróć bezpośrednio
    if best and best[0].isupper() and best[-1] in ".!?":
        return best
    # Inaczej opakuj kontekstowo
    return f"Z przestrzeni fazowej CIELingo: {best}"


def _synthesize_answer(sources: list[dict], decision: dict[str, Any],
                       op_id: str, question: str) -> str:
    """Syntezuj odpowiedź z nearest texts + operator decision.

    PhaseNav synthesis: odpowiedź jest funkcją operatora i nearest texts.
    Różne operatory → różne formaty odpowiedzi.

    Args:
        sources: lista {text, sim, source, metadata}
        decision: {action, confidence, tone, fallback, ...}
        op_id: wykryty operator PhaseNav
        question: oryginalne pytanie

    Returns:
        string odpowiedzi
    """
    if not sources:
        return "Nie mam wystarczającej wiedzy w przestrzeni fazowej."

    # DISABLE:PHASENAV_SEARCH — odfiltruj surowy output konsolowy
    sources = _clean_sources(sources)

    if not sources:
        return "Nie mam wystarczającej wiedzy w przestrzeni fazowej na to pytanie."

    action = decision["action"]
    confidence = decision["confidence"]
    tone = decision["tone"]

    best = sources[0]["text"]
    top_sims = [s["sim"] for s in sources[:3]]
    best_sim = top_sims[0] if top_sims else 0.0

    # Keyword intent override — koryguje błędny operator PhaseNav dla PL pytań.
    _q = question.lower().strip()
    if any(kw in _q for kw in ("czujesz", "czuję", "czujesz się", "nastrój", "emocj", "afekt")):
        action = "emotional_answer"
    elif any(kw in _q for kw in ("kim jest", "kim jestes", "kim jesteś", "twój twórca",
                                   "kto to jest", "kto jest", "kto stworzył", "autor")):
        action = "direct_answer"
    elif any(kw in _q for kw in ("jak masz na imię", "jak masz na imie", "twoje imię",
                                   "twoje imie", "jak się nazywasz", "jak sie nazywasz")):
        action = "direct_answer"
    elif any(kw in _q for kw in ("opisz", "wyjaśnij", "wytłumacz", "wytlumacz", "czym jest",
                                   "co to jest", "jak działa", "jak dziala", "jak opiszesz",
                                   "explain", "describe", "what is", "how does", "tell me",
                                   "holonomi", "synchronizacj", "oscylat", "kuramoto",
                                   "phasenav", "fazow", "koheren")):
        action = "direct_answer"

    # Operator-specific synthesis
    if action == "answer_with_uncertainty":
        if confidence == "high":
            answer = best
        elif confidence == "medium":
            answer = f"Myślę, że: {best}\n\n(Mam pewne wątpliwości — podobieństwo: {best_sim:.2f})"
        else:
            answer = (f"Nie jestem pewien. Sugerowane skojarzenie:\n{best}"
                      f"\n\n(Podobieństwo: {best_sim:.2f} — niska pewność)")

    elif action == "execute_action":
        answer = f"🔄 Wykonuję: {best}"
        if len(sources) > 1:
            answer += f"\n\nSzczegóły: {sources[1]['text']}"

    elif action == "retrieve_memory":
        answer = f"📖 Z pamięci: {best}"

    elif action == "retrieve_source":
        src = sources[0].get("source", "?")
        answer = f"📚 Źródło [{src}]: {best}"

    elif action == "blend_and_answer":
        if len(sources) >= 2:
            answer = f"{sources[0]['text']}\n\nKompozycja: {sources[1]['text']}"
        else:
            answer = best

    elif action == "compare_and_answer":
        if len(sources) >= 2:
            answer = (f"Porównanie:\n1. {sources[0]['text']}\n"
                      f"2. {sources[1]['text']}")
        else:
            answer = best

    elif action == "safe_answer":
        answer = f"⛔ (safe mode) {best[:150]}"

    elif action == "ask_permission":
        answer = f"Potrzebuję zgody na: {best}"

    elif action == "emotional_answer":
        answer = _build_prompt_inference(question, sources)

    elif action == "direct_answer":
        answer = _build_prompt_inference(question, sources)

    elif action == "express_uncertainty":
        answer = f"Nie jestem pewien. Oto co wiem:\n{best}"

    elif action == "explain_causality":
        answer = f"Ponieważ: {best}"
        if len(sources) > 1:
            answer += f"\nWynik: {sources[1]['text']}"

    elif action == "explain_condition":
        answer = f"Jeśli: {best}"
        if len(sources) > 1:
            answer += f"\nTo: {sources[1]['text']}"

    elif action == "refuse_answer":
        answer = "Nie mogę odpowiedzieć na to zapytanie."

    elif action == "request_clarification":
        answer = "Potrzebuję doprecyzowania. Oto co rozumiem:\n" + best

    elif action == "core_identity_answer":
        answer = f"⚛️ (ATTRACTOR) Tożsamość systemu: {best}"

    else:
        # CIELINGO_PRIMARY_OUTPUT:PROMPT_INFERENCE — synteza z czystych źródeł
        if confidence == "high" and len(sources) > 1 and sources[1]["sim"] > 0.75:
            a1 = _build_prompt_inference(question, sources[:1])
            a2 = _build_prompt_inference(question, sources[1:2])
            answer = f"{a1}\n\nPowiązane: {a2}"
        else:
            answer = _build_prompt_inference(question, sources)

    return answer


# ── CIELingo Inference Engine ────────────────────────────────────────


class CIELingoInference:
    """CIELingo Inference Engine — PhaseNav-powered na 36D operatorach.

    PhaseNav Coding Language:
      - encode() → ω_detect() → ω_apply() → query() → synthesize()

    Używa:
      - PhaseMemory dla pamięci tekst↔φ
      - PhaseNav operator_algebra dla operatorów 36D
      - fast_encode_text dla szybkiego kodowania query
    """

    def __init__(self, memory_path: str | Path = MEMORY_PATH):
        from ciel_geometry.cielingo_phase_memory import PhaseMemory
        self.memory_path = Path(memory_path)
        self.memory = PhaseMemory.load_or_create(self.memory_path)
        self._encoder_fn = None
        self._encoder_weighted_fn = None
        self._ops_map = None
        self._thematic_db = None

    @property
    def _encoder(self):
        if self._encoder_fn is None:
            from ciel_geometry.cielingo_phase_encoder import fast_encode_text
            self._encoder_fn = fast_encode_text
        return self._encoder_fn

    @property
    def _encoder_weighted(self):
        """Jak _encoder, ale zwraca (phi, weights) — weights pozwala
        PhaseMemory.query() ignorować nietknięty, wspólny dla każdego tekstu
        baseline zamiast dać mu dominować similarity (naprawa 2026-07-10)."""
        if self._encoder_weighted_fn is None:
            from ciel_geometry.cielingo_phase_encoder import fast_encode_text_weighted
            self._encoder_weighted_fn = fast_encode_text_weighted
        return self._encoder_weighted_fn

    @property
    def _operators(self):
        if self._ops_map is None:
            from ciel_geometry.phasenav.operator_algebra import generate_operator_map, ALL_OPERATOR_IDS
            self._ops_map = generate_operator_map()
            self._all_ops = ALL_OPERATOR_IDS
        return self._ops_map

    # ── PhaseNav primitives ──────────────────────────────────────────

    def encode(self, text: str) -> np.ndarray:
        """PhaseNav encode: text → 36D φ."""
        return self._encoder(text)

    def detect_operator(self, phi: np.ndarray) -> tuple[str, np.ndarray, float]:
        """PhaseNav ω_detect: φ → nearest PhaseNav operator.

        PhaseNav coding: każda faza ma nearest operator ω.
        """
        return _detect_operator(phi)

    def apply_operator(self, phi: np.ndarray, op_id: str,
                       op_vector: np.ndarray | None = None,
                       strength: float = 0.3) -> np.ndarray:
        """PhaseNav ω_apply: (φ, ω) → φ_transformed."""
        if op_vector is None:
            op_vector = self._operators.get(op_id, self._operators["IDENTITY"])
        return _apply_operator(phi, op_id, op_vector, strength=strength)

    def decide(self, op_id: str, sim: float,
               sim_scores: list[float]) -> dict[str, Any]:
        """PhaseNav decision protocol: (ω, sim) → decision."""
        return _operator_decision(op_id, sim, sim_scores)

    def synthesize(self, sources: list[dict], decision: dict[str, Any],
                   op_id: str, question: str) -> str:
        """PhaseNav synthesis: (texts, ω) → odpowiedź."""
        return _synthesize_answer(sources, decision, op_id, question)

    def save(self) -> None:
        """Persist the underlying PhaseMemory."""
        self.memory.save(self.memory_path)

    @property
    def thematic_db(self):
        if self._thematic_db is None:
            from cielingo.thematic_db import ThematicDatabaseManager

            self._thematic_db = ThematicDatabaseManager()
        return self._thematic_db

    def learn(
        self,
        text: str,
        *,
        source: str = "cielingo",
        metadata: dict[str, Any] | None = None,
        persist: bool = True,
    ) -> dict[str, Any]:
        """Store a text sample in PhaseMemory and optionally persist it."""
        phi, weights = self._encoder_weighted(text)
        meta = dict(metadata or {})
        meta.setdefault("source", source)
        idx = self.memory.add(text, phi, weights=weights, source=source, metadata=meta)
        if persist:
            self.save()
        return {
            "index": idx,
            "text": text,
            "source": source,
            "memory_size": self.memory.size,
            "metadata": self.memory.metadata[idx],
        }

    def digest_web(
        self,
        url: str,
        *,
        max_sentences: int = 3,
        timeout: int = 15,
        cache: bool = True,
    ) -> dict[str, Any]:
        """Fetch a URL and return a compact digest payload."""
        from cielingo.web_digest import digest_url

        digest = digest_url(url, timeout=timeout, max_sentences=max_sentences, cache=cache)
        return digest.as_dict()

    def learn_web(
        self,
        url: str,
        *,
        max_sentences: int = 3,
        timeout: int = 15,
        cache: bool = True,
        persist: bool = True,
        themes: list[str] | None = None,
    ) -> dict[str, Any]:
        """Fetch a URL, digest it, and store the digest in memory."""
        digest = self.digest_web(url, max_sentences=max_sentences, timeout=timeout, cache=cache)
        if digest.get("error"):
            return {"error": digest["error"], "digest": digest}

        learned_text = digest.get("summary") or digest.get("excerpt") or digest.get("title") or url
        learned = self.learn(
            learned_text,
            source="web",
            metadata={
                "url": url,
                "title": digest.get("title", ""),
                "content_digest": digest.get("content_digest", ""),
                "content_type": digest.get("content_type", ""),
                "keywords": digest.get("keywords", []),
                "word_count": digest.get("word_count", 0),
                "sentence_count": digest.get("sentence_count", 0),
            },
            persist=persist,
        )
        thematic = self.thematic_db.register_digest(digest, themes=themes)
        return {"digest": digest, "learned": learned, "thematic": thematic}

    def learn_news(
        self,
        *,
        sources: list[str] | None = None,
        max_articles: int = 5,
        persist: bool = True,
        themes: list[str] | None = None,
    ) -> dict[str, Any]:
        """Fetch RSS/news items and store their digests in memory."""
        from cielingo.web_digest import digest_news

        digests = digest_news(sources=sources, max_articles=max_articles)
        learned_items = []
        for digest in digests:
            learned_items.append(
                self.learn(
                    digest.summary or digest.title or digest.url,
                    source="rss",
                    metadata={
                        "url": digest.url,
                        "title": digest.title,
                        "source": digest.source,
                        "content_digest": digest.content_digest,
                        "content_type": digest.content_type,
                        "keywords": list(digest.keywords),
                    },
                    persist=False,
                )
            )

        if persist:
            self.save()

        thematic = [self.thematic_db.register_digest(digest, themes=themes) for digest in digests]

        return {
            "count": len(learned_items),
            "digests": [d.as_dict() for d in digests],
            "learned": learned_items,
            "thematic": thematic,
            "memory_size": self.memory.size,
        }

    # ── Retrieval ────────────────────────────────────────────────────

    def retrieve(self, query: str | np.ndarray, k: int = 5,
                 *, min_sim: float = 0.3,
                 use_operator: bool = True) -> list[dict[str, Any]]:
        """PhaseNav retrieve: query → ω_detect → ω_apply → nearest.

        Args:
            query: Tekst lub (36,) wektor faz
            k: Liczba wyników
            min_sim: Minimalne podobieństwo
            use_operator: Jeśli True, aplikuj PhaseNav operator przed query

        Returns:
            Lista {text, sim, mean_phase, metadata, operator}
        """
        if isinstance(query, str):
            phi = self.encode(query)
        else:
            phi = query

        # PhaseNav: detect and apply operator
        op_info = {}
        if use_operator:
            op_id, op_vec, op_sim = self.detect_operator(phi)
            phi_transformed = self.apply_operator(phi, op_id, op_vec, strength=0.3)
            op_info = {"operator": op_id, "operator_sim": round(op_sim, 4)}
        else:
            phi_transformed = phi
            op_info = {"operator": "IDENTITY", "operator_sim": 1.0}

        # NOTE: per-dimension weights gating (fast_encode_text_weighted) is
        # available but deliberately NOT used here — verified 2026-07-10 to
        # be unreliable for short/sparse texts (a bucket with one
        # contributing token looks identical whether it's a genuine match or
        # an accidental hash collision). Revisit once concept_windows.py
        # (Część 1) gives windows enough tokens/bucket for gating to be safe.
        results = self.memory.query(phi_transformed, k=k, min_sim=min_sim)
        for r in results:
            r.update(op_info)

        return results

    # ── Main answer ──────────────────────────────────────────────────

    def answer(self, question: str, k: int = 5,
               *, include_sim: bool = True) -> dict[str, Any]:
        """PhaseNav answer: pełny pipeline przez operatory.

        Pipeline:
          1. φ = encode(question)
          2. ω = detect_operator(φ)
          3. φ' = apply_operator(φ, ω)
          4. results = query(φ', memory)
          5. decision = decide(ω, sim)
          6. answer = synthesize(results, decision, ω, question)

        Args:
            question: Pytanie w języku naturalnym
            k: Liczba źródeł do syntezy
            include_sim: Czy dołączyć similarity

        Returns:
            dict z: answer, sources, decision, operator, phi, ...
        """
        t0 = time.time()

        # ── pn_bil 24D binary phase vectorization (wektoryzuj na bieżąco) ──
        _pnbil_vector: list[float] | None = None
        _orchorbital_mode: str = "reduce"
        try:
            import hashlib as _hashlib
            _q_sha256 = _hashlib.sha256(question.encode()).hexdigest()
            from pn_bil.phasenav import seed_from_sha256 as _pnbil_seed  # type: ignore
            from cielingo.semantic_collatz import semantic_collatz_route as _sc_route, route_summary as _sc_summary
            _seed = _pnbil_seed(_q_sha256)
            _route = _sc_route(_seed, max_steps=24)
            _summary = _sc_summary(_route)
            _orchorbital_mode = _summary["dominant_mode"]  # "reduce" | "expand"
            _pnbil_vector = [
                _summary["reduce_count"] / max(1, _summary["steps"]),
                _summary["expand_count"] / max(1, _summary["steps"]),
                float(_summary["final_n"] % 256) / 256.0,
            ]
            log.debug("pn_bil collatz: mode=%s steps=%d", _orchorbital_mode, _summary["steps"])
        except Exception:
            pass

        # ── orchorbital CardTrace snap dla pytania ──────────────────────
        _orchorbital_decision: dict[str, Any] | None = None
        try:
            from cielingo.card_trace_eeg import build_card_trace, CardTraceSnap, infer_clusters
            from cielingo.orchorbital_router import route_orchorbital
            import hashlib as _h2
            _snap_hash = _h2.sha256(question.encode()).hexdigest()[:16]
            _qtokens = question.replace("?", "").replace("!", "").replace(",", "").split()
            _traces = [build_card_trace(t, context_key=question[:32]) for t in _qtokens[:12]]
            _clusters = infer_clusters(_traces)
            _current_snap = CardTraceSnap(
                snap_id="q_" + _snap_hash,
                schema="noema/card-trace-snap/v0.1",
                window={"start": 0, "end": len(_qtokens)},
                active_traces=[{"card_id": t.card_id, "amplitude": t.amplitude,
                                 "phase": t.phase, "channel": t.channel} for t in _traces],
                clusters=_clusters,
                layout_hash=_snap_hash,
                identity_anchor=question[:32],
            )
            _orch = route_orchorbital(_current_snap, [], max_collatz_steps=16)
            _orchorbital_decision = _orch.as_dict()
            # Collatz route może nadpisać mode jeśli mamy decyzję
            if _orch.route_summary.get("dominant_mode"):
                _orchorbital_mode = _orch.route_summary["dominant_mode"]
            log.debug("orchorbital: decision=%s score=%.3f", _orch.decision, _orch.association_score)
        except Exception:
            pass

        # 1. Encode
        phi = self.encode(question)

        # 2. Detect operator
        op_id, op_vec, op_sim = self.detect_operator(phi)
        log.debug("PhaseNav operator: %s (sim=%.4f)", op_id, op_sim)

        # 3. Apply operator — siła modulowana przez Collatz mode
        _op_strength = 0.4 if _orchorbital_mode == "expand" else 0.2
        phi_transformed = self.apply_operator(phi, op_id, op_vec, strength=_op_strength)

        # 4. Query memory — PhaseNav vector bypass + 3-pass fallback.
        #
        # Błąd: pytanie w języku polskim → phi_pytania leży w innym klastrze przestrzeni
        # fazowej niż angielskie akapity noema_docs. Próg sim odcina dobre wpisy.
        #
        # Omięcie błędu wektorem:
        #   phi_bypass = 0.5 * phi_centroid_noema_docs + 0.5 * phi_transformed
        #   → nawiguje do przecięcia: intencja pytania ∩ przestrzeń dokumentacji.
        #   Wszystkie noema_docs będą miały wyższe sim do phi_bypass niż do phi_pytania.
        _NOISE_SOURCES = {"raw_logs", "conversation", "?", "cielingo_word_card"}

        # Wykryj intencję pytania: tożsamość/emocja vs wiedza.
        _q_lower = question.lower().strip()

        # ── Silnik gramatyczny PL ────────────────────────────────────
        # PolishRegionalSolver: subject/predicate/theme → doprecyzowanie query.
        # Wydobywa: temat (theme_candidate), predykat (action/preference),
        # negację, imperatyw — i blenduje phi_transformed w kierunku tematu.
        _grammar_theme_phi: np.ndarray | None = None
        _grammar_imperative = False
        _grammar_negation = False
        try:
            from cielingo_core.language_spaces.pl.role_inference import infer_role_candidates
            from cielingo_core.language_spaces.pl.grammar import analyze_polish_tokens
            _tokens = [t for t in question.replace("?", "").replace("!", "").replace(",", "").split()
                       if len(t) > 1]
            _roles = infer_role_candidates(_tokens)
            _hint = analyze_polish_tokens(_tokens)
            _grammar_negation = bool(_hint.negation_indices)
            _grammar_imperative = bool(_hint.imperative_indices)
            # Wydobądź temat (theme_candidate) o najwyższej pewności
            _theme_tokens = [r.token for r in _roles
                             if r.role_candidate in ("theme_candidate", "patient_candidate")
                             and r.confidence >= 0.48]
            if _theme_tokens:
                _theme_text = " ".join(_theme_tokens)
                _theme_phi = self.encode(_theme_text)
                # Blenduj phi_transformed z phi tematu — pull query w kierunku tematu
                _grammar_theme_phi = (0.65 * phi_transformed + 0.35 * _theme_phi) % (2 * np.pi)
        except Exception:
            pass
        if _grammar_theme_phi is not None:
            phi_transformed = _grammar_theme_phi
        _SELF_INTENTS = {
            "kim jesteś", "kim jestes", "kim jest ciel", "jak masz na imię",
            "jak masz na imie", "jak się nazywasz", "jak sie nazywasz",
            "czujesz", "emocj", "afekt", "nastrój",
            "co czujesz", "jak się czujesz", "twoja tożsamość",
            "twoja tozsamosc", "czym jesteś", "czym jestes",
            "kim jest adrian", "co wiesz o adrianie", "twój twórca",
            "twoj tworca", "kto cię stworzył", "kto cie stworzyl",
        }
        _KNOWLEDGE_INTENTS = {
            "jak opiszesz", "opisz", "wyjaśnij", "wytłumacz", "wytlumacz",
            "co to jest", "czym jest", "co to", "czym są", "czym sa",
            "jak działa", "jak dziala", "jak to działa", "jak to dziala",
            "holonomi", "koheren", "kuramoto", "phasenav",
            "oscylator", "synchroniz", "orbital", "fazow",
            "entropy", "entropi", "tensor",
            # English knowledge queries
            "explain", "describe", "what is", "how does", "how do",
            "what are", "tell me about", "define", "definition",
            "phase constraint", "euler", "holonomy", "coherence",
        }
        _is_self = any(kw in _q_lower for kw in _SELF_INTENTS)
        _is_knowledge = any(kw in _q_lower for kw in _KNOWLEDGE_INTENTS) and not _is_self

        # orchorbital mode moduluje parametry query
        _orch_k_mult = 5 if _orchorbital_mode == "expand" else 3
        _orch_min_sim = 0.08 if _orchorbital_mode == "expand" else 0.14

        results = []
        if _is_self and not _is_knowledge:
            # Pytanie o tożsamość/emocje: noema_docs PL z samowiedzy
            _all_noema = self.memory.query(phi_transformed, k=k * _orch_k_mult, min_sim=0.15,
                                           include_sources={"noema_docs"})
            _pl_noema = [r for r in _all_noema if r.get("metadata", {}).get("lang") == "pl"]
            if "adrian" in _q_lower:
                _adrian_chunks = [r for r in _pl_noema if "Adrian" in r.get("text", "")]
                if _adrian_chunks:
                    results = _adrian_chunks[:k]
                else:
                    _all_mem = self.memory.query(phi_transformed, k=k * 6, min_sim=0.05,
                                                 exclude_sources=_NOISE_SOURCES)
                    _adrian_any = [r for r in _all_mem if "Adrian" in r.get("text", "")]
                    results = _adrian_any[:k] if _adrian_any else _pl_noema[:k]
            else:
                results = _pl_noema[:k] if _pl_noema else _all_noema[:k]
        elif _is_knowledge:
            # Pytanie o wiedzę: orchorbital expand → szersze szukanie
            results = self.memory.query(phi_transformed, k=k, min_sim=_orch_min_sim,
                                        include_sources={"knowledge_db_fast"})
            if len(results) < 2:
                results = self.memory.query(phi_transformed, k=k, min_sim=max(0.05, _orch_min_sim - 0.03),
                                            exclude_sources=_NOISE_SOURCES)
        else:
            # Ogólne: knowledge_db_fast + noema_docs bez ograniczeń
            results = self.memory.query(phi_transformed, k=k, min_sim=0.12,
                                        exclude_sources=_NOISE_SOURCES)
            if not results:
                results = self.memory.query(phi_transformed, k=k, min_sim=0.08,
                                            exclude_sources={"raw_logs", "cielingo_word_card"})
                # Dodaj PL noema_docs jeśli nadal brak
                if not results:
                    _all_noema = self.memory.query(phi_transformed, k=k * 4, min_sim=0.2,
                                                   include_sources={"noema_docs"})
                    _pl_noema = [r for r in _all_noema
                                 if r.get("metadata", {}).get("lang") == "pl"]
                    results = _pl_noema[:k] if _pl_noema else _all_noema[:k]

        elapsed = time.time() - t0

        # Filtr jakości tekstu: odrzuć wpisy wyglądające jak checksums/hashes/pliki techniczne.
        import re as _re_quality
        _HASH_PATTERN = _re_quality.compile(r'^[0-9a-f]{40,}\s+\S+', _re_quality.MULTILINE)
        _TECH_NOISE = _re_quality.compile(
            r'^(sha256:|md5:|[0-9a-f]{64}\s|[0-9a-f]{40}\s|\s*[{}\[\]]\s*$)', _re_quality.MULTILINE
        )
        _BIBCODE_PATTERN = _re_quality.compile(
            r'\b\d{4}[A-Z][A-Za-z&.]{2,}\.\.\d|'   # NASA ADS: 1999IAUS..194..199D
            r'\b\d{4}[A-Z]{2,}\w*\s+\d+\s+\d+\b|'  # inne bibcody
            r'\barXiv:\d{4}\.\d{4,5}\b'              # arXiv IDs
        )

        def _is_noise_entry(text: str) -> bool:
            if not text or len(text) < 20:
                return True
            if _HASH_PATTERN.search(text[:300]):
                return True
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            if lines and _re_quality.match(r'^[0-9a-f]{40,}', lines[0]):
                return True
            # NASA ADS bibcodes / arXiv IDs dominują tekst
            if _BIBCODE_PATTERN.search(text[:300]):
                _alpha_words = sum(1 for w in text.split() if w.isalpha() and len(w) > 2)
                if _alpha_words < 5:
                    return True
            # Wpis składa się niemal wyłącznie z identyfikatorów (< 4 słowa alfanumeryczne)
            _real_words = [w for w in text.split() if _re_quality.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{3,}$', w)]
            if len(text.split()) > 3 and len(_real_words) < 3:
                return True
            return False

        results = [r for r in results if not _is_noise_entry(r.get("text", ""))]

        # Build sources — odrzuć REPO karty i metadata bullets przed syntezą.
        # Dla noema_docs (chunki z NOEMA_DOCUMENTATION.md):
        #   _extract_noema_prose() wydobywa prozę z markdown chunks —
        #   nagłówki ### i REPO bullets (- **Purpose**:) są pomijane,
        #   zostaje czysty tekst paragrafów. Pozwala to uratować 90+ wpisów
        #   które wprawdzie zaczynają się od ### ale zawierają wartościową prozę.
        # Dla non-noema_docs (fallback): standardowy body check.

        import re as _re
        _INLINE_REPO = _re.compile(
            r'(#{1,4}\s+[^\n.]{0,120}(?=\s+[A-Z]|\s*$))'  # inline ### Header Text
            r'|(\|[^|]+\|)'                                  # table cells
            r'|((?:^|\s)-\s+\*\*\w[^*]*\*\*\s*:)'          # - **Key**:
            r'|(\*\*(?:Purpose|Imports|Exports|Active|Uses|Status|Entry points?|Optional|Dependenc|Description|id_karty)\*\*\s*:)'
            r'|(?:---+)',
            _re.MULTILINE
        )

        def _extract_noema_prose(text: str) -> str:
            # Najpierw próbuj linia po linii (dla multi-line entries)
            if '\n' in text:
                lines = text.split('\n')
                prose: list[str] = []
                for ln in lines:
                    s = ln.strip()
                    if not s:
                        continue
                    if s.startswith(('#', '|', '---', '```')):
                        continue
                    if s.startswith(('- **', '**Purpose**', '**Imports**', '**Exports**',
                                      '**Active**', '**Uses**', '**Status**', '**Entry point',
                                      '**Optional', '**Dependenc', '**Description**',
                                      '**id_karty**', '#### ')):
                        continue
                    if '"method":' in s or '"samples":' in s:
                        continue
                    prose.append(s)
                result = ' '.join(prose).strip()
            else:
                # Single-line entry: usuń inline markdown via regex
                result = _INLINE_REPO.sub(' ', text).strip()
                result = _re.sub(r'\s{2,}', ' ', result)
            return result if len(result) >= 30 else ''

        _noema_docs_query = len(results) > 0 and results[0].get("metadata", {}).get("source") == "noema_docs"
        _REPO_MARKERS_BODY = ("**Purpose**:", "**Imports**:", "**Exports**:", "**Active**:",
                              "**Uses**:", "**Status**:", "**Entry points**:", "**Optional deps**:",
                              "**Dependencies**:", "**id_karty:**", '"method":', '"samples":',
                              "- **Purpose", "- **Import", "#### `")
        sources = []
        for r in results:
            _raw = r["text"]
            if _noema_docs_query:
                _full = _extract_noema_prose(_raw) or _raw
            else:
                _full = _raw
            _lead = _full[:150]
            _txt = _full[:300]    # zwracamy max 300 znaków jako source.text
            _t = _txt.strip()
            if len(_t) < 30:
                continue
            if _t.startswith(("#", "{", "[", "```", "- **")):
                continue
            if not _noema_docs_query and any(m in _lead for m in _REPO_MARKERS_BODY):
                continue
            if _t.startswith("REPO-") or "## Tożsamość" in _lead or "poziom_orbitalny" in _lead:
                continue
            _non_ascii = sum(1 for c in _t if ord(c) > 127 and not c.isalpha())
            if _non_ascii > len(_t) * 0.25:
                continue
            src_meta = r.get("metadata", {})
            sources.append({
                "text": _txt,
                "sim": round(r["sim"], 4),
                "source": src_meta.get("source", "?"),
                "source_type": src_meta.get("source_type", ""),
                "idx": src_meta.get("idx", -1),
                "filename": src_meta.get("filename", ""),
                "themes": src_meta.get("themes", [])[:3],
            })

        # Deduplication: usuń prawie-identyczne teksty (ten sam prefix 80 znaków)
        _seen_prefixes: set[str] = set()
        _deduped_sources = []
        for _s in sources:
            _prefix = _s["text"][:80].strip().lower()
            if _prefix not in _seen_prefixes:
                _seen_prefixes.add(_prefix)
                _deduped_sources.append(_s)
        sources = _deduped_sources

        # Dla noema_docs: prose_sentence entries (czyste zdania) priorytet nad markdown chunks.
        # Chunk-based entries mają wyższy sim do centroidu (95%) bo go zdominowały liczbą.
        # Re-sort: prose_sentence first, reszta po sim.
        if _noema_docs_query:
            _prose_src = [s for s in sources if s.get("source_type") == "prose_sentence"]
            _other_src = [s for s in sources if s.get("source_type") != "prose_sentence"]
            sources = _prose_src + _other_src

        # 5. Decision protocol
        sim_scores = [s["sim"] for s in sources]
        decision = self.decide(op_id, op_sim, sim_scores)

        # 6. Synthesize answer
        answer = self.synthesize(sources, decision, op_id, question)

        result = {
            "answer": answer,
            "sources": sources,
            "decision": decision,
            "operator": op_id,
            "operator_similarity": round(op_sim, 4),
            "phi": phi,
            "phi_transformed": phi_transformed,
            "sim_scores": sim_scores,
            "n_sources": len(sources),
            "elapsed_s": round(elapsed, 3),
            "orchorbital_mode": _orchorbital_mode,
            "orchorbital_decision": _orchorbital_decision,
            "pnbil_vector": _pnbil_vector,
        }

        return result

    # ── Exploration ──────────────────────────────────────────────────

    def explore(self, seed_text: str, n_steps: int = 5,
                step_size: float = 0.2) -> list[dict[str, Any]]:
        """PhaseNav explore: eksploruj przestrzeń przez operator-driven walk.

        Każdy krok: detect operator → apply operator → query memory.
        """
        phi = self.encode(seed_text)
        path = []

        for step in range(n_steps):
            # PhaseNav operator step
            op_id, op_vec, op_sim = self.detect_operator(phi)
            phi = self.apply_operator(phi, op_id, op_vec, strength=0.3 * (step + 1) / n_steps)

            # Query with slight random perturbation
            rng = np.random.default_rng(hash(f"{seed_text}:{step}") % (2**31 - 1))
            phi_perturbed = (phi + rng.uniform(-0.2, 0.2, 36)) % (2 * np.pi)
            nearest = self.memory.query(phi_perturbed, k=1)

            path.append({
                "step": step,
                "operator": op_id,
                "operator_sim": round(op_sim, 4),
                "mean_phase": float(np.mean(phi)),
                "nearest": nearest[0] if nearest else None,
            })

        return path

    def blend_and_query(self, texts: list[str], weights: list[float] | None = None,
                        k: int = 5, *, use_operator: bool = True) -> dict[str, Any]:
        """PhaseNav blend: blend konceptów przez operator-driven retrieval."""
        blended = self.memory.blend(texts, weights)
        if blended is None:
            return {"blended": None, "results": []}

        if use_operator:
            op_id, op_vec, op_sim = self.detect_operator(blended)
            blended = self.apply_operator(blended, op_id, op_vec, strength=0.3)

        results = self.memory.query(blended, k=k)
        return {
            "blended_phi": blended,
            "operator": op_id if use_operator else "IDENTITY",
            "results": [{
                "text": r["text"],
                "sim": round(r["sim"], 4),
            } for r in results],
        }

    # ── Stats ────────────────────────────────────────────────────────

    def stats(self) -> dict[str, Any]:
        """Statystyki modelu PhaseNav."""
        mem_stats = self.memory.stats()
        ops_map = self._operators
        return {
            "memory_size": mem_stats["size"],
            "coverage": mem_stats["coverage"],
            "fill_pct": mem_stats["fill_pct"],
            "operators": len(ops_map),
            "actions": len(OPERATOR_ACTIONS),
        }

    def describe_operator(self, op_id: str) -> dict[str, Any]:
        """PhaseNav describe: metadane operatora."""
        ops_map = self._operators
        if op_id not in ops_map:
            return {"error": f"Unknown operator: {op_id}"}
        vec = ops_map[op_id]
        action = OPERATOR_ACTIONS.get(op_id, "direct_answer")
        return {
            "operator": op_id,
            "norm": round(float(np.linalg.norm(vec)), 4),
            "vector_sample": [round(float(x), 4) for x in vec[:8]],
            "action": action,
            "tone": _operator_decision(op_id, 0.0, []).get("tone", "neutral"),
        }


# ── GGUF teaching (CIELingo is the only answering model; GGUF only feeds
#    training text into PhaseMemory via learn() — never answers directly) ──

GGUF_TEACHER_MODEL_PATH = "/home/adrian/Pulpit/qwen2.5-0.5b-instruct-q2_k.gguf"


def _gguf_teach_text(topic: str, *, max_tokens: int = 200, timeout: int = 60) -> str | None:
    """Ask the GGUF model for a short teaching paragraph about `topic`.

    Runs exclusively through subprocess + `python3 -c` — the GGUF model is
    never imported into this process. Returns None on any failure so the
    caller can decide whether to skip learning for this topic.
    """
    prompt = (
        f"Napisz krótki, rzeczowy akapit (2-4 zdania) po polsku wyjaśniający: {topic}\n"
        "Odpowiedź:"
    )
    script = (
        "from llama_cpp import Llama; "
        f"m = Llama(model_path={GGUF_TEACHER_MODEL_PATH!r}, n_ctx=512, verbose=False); "
        f"r = m.create_completion({prompt!r}, max_tokens={max_tokens}, stop=['\\n\\n']); "
        "print(r['choices'][0]['text'].strip())"
    )
    try:
        result = subprocess.run(
            ["python3", "-c", script],
            capture_output=True, text=True, timeout=timeout,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        log.debug("gguf_teach_text failed for %r: %s", topic, exc)
        return None
    text = result.stdout.strip()
    return text or None


def teach_cielingo_via_gguf(topic: str, *, persist: bool = True) -> dict[str, Any]:
    """Generate a teaching text for `topic` via GGUF and feed it into CIELingo.

    CIELingo remains the only model that ever answers a user. GGUF is used
    solely as a text generator to expand PhaseMemory — the generated text is
    stored with source="gguf_teacher" so it stays distinguishable from
    human-provided or corpus-ingested knowledge.
    """
    text = _gguf_teach_text(topic)
    if not text:
        return {"topic": topic, "learned": False, "reason": "gguf_generation_failed"}

    ci = CIELingoInference()
    learned = ci.learn(
        text,
        source="gguf_teacher",
        metadata={"topic": topic, "teacher_model": GGUF_TEACHER_MODEL_PATH},
        persist=persist,
    )
    return {"topic": topic, "learned": True, "text": text, "entry": learned}


# ── Interactive CLI ─────────────────────────────────────────────────


def run_cli():
    """Interactive CIELingo CLI — PhaseNav-powered."""
    ci = CIELingoInference()
    print("=" * 60)
    print("  CIELingo — PhaseNav Coding Language Engine")
    print(f"  Pamięć: {ci.memory.size} wpisów | Operatory: {len(ci._operators)}")
    print("=" * 60)
    print("  Komendy: /explore, /blend, /operator, /stats, /digest URL..., /learn URL..., /exit")
    print()

    while True:
        try:
            text = input("\n❓ Ty: ").strip()
            if not text:
                continue
            if text == "/exit":
                print("Do zobaczenia.")
                break
            if text == "/stats":
                s = ci.stats()
                print(f"\n📊 PhaseNav Stats:")
                for k, v in s.items():
                    print(f"  {k}: {v}")
                continue
            if text == "/operators":
                print("\n🔷 PhaseNav Operators:")
                for oid in sorted(ci._operators.keys()):
                    desc = ci.describe_operator(oid)
                    print(f"  {oid:20s} | action={desc['action']:20s} | norm={desc['norm']:.2f}")
                continue
            if text.startswith("/operator "):
                name = text[10:].strip().upper()
                desc = ci.describe_operator(name)
                if "error" in desc:
                    print(f"  Nieznany operator: {name}")
                else:
                    print(f"\n🔷 {desc['operator']}:")
                    for k, v in desc.items():
                        print(f"  {k}: {v}")
                continue
            if text.startswith("/explore "):
                seed = text[9:]
                path = ci.explore(seed, n_steps=5)
                print(f"\n🚶 Eksploracja od: {seed}")
                for p in path:
                    near = p["nearest"]
                    near_text = near["text"][:60] if near else "—"
                    print(f"  krok {p['step']}: op={p['operator']} "
                          f"φ={p['mean_phase']:.3f} → {near_text}")
                continue
            if text.startswith("/blend "):
                parts = text[7:].split("|")
                texts = [p.strip() for p in parts if p.strip()]
                if len(texts) >= 2:
                    result = ci.blend_and_query(texts)
                    print(f"\n🧬 Blend: {' | '.join(texts)}")
                    print(f"  Operator: {result.get('operator', '?')}")
                    for r in result["results"]:
                        print(f"  sim={r['sim']:.4f}  {r['text'][:80]}")
                continue
            if text.startswith("/digest "):
                urls = [piece for piece in text[8:].split() if piece]
                if not urls:
                    print("Usage: /digest URL [URL ...]")
                    continue
                for url in urls:
                    digest = ci.digest_web(url)
                    print(f"\n🌐 {digest.get('title', '')} [{digest.get('url', '')}]")
                    print(f"  summary: {digest.get('summary', '')}")
                    if digest.get("keywords"):
                        print(f"  keywords: {', '.join(digest['keywords'][:8])}")
                    if digest.get("error"):
                        print(f"  error: {digest['error']}")
                continue
            if text.startswith("/learn "):
                urls = [piece for piece in text[7:].split() if piece]
                if not urls:
                    print("Usage: /learn URL [URL ...]")
                    continue
                for url in urls:
                    result = ci.learn_web(url)
                    if result.get("error"):
                        print(f"\n⚠ {url}: {result['error']}")
                        continue
                    digest = result.get("digest", {})
                    learned = result.get("learned", {})
                    print(f"\n📥 {digest.get('title', '')} [{digest.get('url', '')}]")
                    print(f"  digest: {digest.get('summary', '')}")
                    print(f"  stored index: {learned.get('index', '-')}")
                continue

            # PhaseNav answer
            result = ci.answer(text)
            print(f"\n🤖 PhaseNav [op={result['operator']}] ({result['elapsed_s']}s):")
            print(f"  {result['answer'][:600]}")
            print(f"  Decision: {result['decision']['action']} "
                  f"(confidence={result['decision']['confidence']})")
            if result["n_sources"] > 1:
                print(f"\n  Źródła ({result['n_sources']}):")
                for s in result["sources"][:3]:
                    print(f"    sim={s['sim']:.3f}  [{s['source']}] {s['text'][:80]}")

        except (KeyboardInterrupt, EOFError):
            print("\nDo zobaczenia.")
            break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run_cli()
