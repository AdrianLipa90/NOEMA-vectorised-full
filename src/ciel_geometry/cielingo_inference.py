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
import time
from pathlib import Path
from typing import Any

import numpy as np

log = logging.getLogger(__name__)

MEMORY_PATH = Path("/tmp/cielingo_phase_memory")

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

    # Confidence based on similarity landscape
    if max_sim > 0.85 and avg_sim > 0.6:
        confidence = "high"
    elif max_sim > 0.7 and avg_sim > 0.4:
        confidence = "medium"
    elif max_sim > 0.5:
        confidence = "low"
    else:
        confidence = "none"

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

    action = decision["action"]
    confidence = decision["confidence"]
    tone = decision["tone"]

    best = sources[0]["text"]
    top_sims = [s["sim"] for s in sources[:3]]
    best_sim = top_sims[0] if top_sims else 0.0

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
        answer = f"💭 {best}"

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
        # Direct answer (IDENTITY, TRANSFORM, etc.)
        if confidence == "high" and len(sources) > 1 and sources[1]["sim"] > 0.75:
            answer = f"{best}\n\nPowiązane: {sources[1]['text']}"
        else:
            answer = best

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
        self._ops_map = None
        self._thematic_db = None

    @property
    def _encoder(self):
        if self._encoder_fn is None:
            from ciel_geometry.cielingo_phase_encoder import fast_encode_text
            self._encoder_fn = fast_encode_text
        return self._encoder_fn

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
        phi = self.encode(text)
        meta = dict(metadata or {})
        meta.setdefault("source", source)
        idx = self.memory.add(text, phi, source=source, metadata=meta)
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

        # 1. Encode
        phi = self.encode(question)

        # 2. Detect operator
        op_id, op_vec, op_sim = self.detect_operator(phi)
        log.debug("PhaseNav operator: %s (sim=%.4f)", op_id, op_sim)

        # 3. Apply operator
        phi_transformed = self.apply_operator(phi, op_id, op_vec, strength=0.3)

        # 4. Query memory with transformed phase.
        # ~98% of the memory is "raw_logs" (private session/chat dumps, not
        # curated knowledge) vs ~2% "knowledge_db" (actually indexed
        # documents). Exclude raw_logs by default so factual questions get
        # real document matches instead of chat-log noise (and don't risk
        # surfacing private conversation content, including token-looking
        # fragments, as an "answer"). Fall back to the unfiltered pool only
        # if excluding raw_logs leaves nothing above the similarity bar.
        results = self.memory.query(phi_transformed, k=k, min_sim=0.15, exclude_sources={"raw_logs"})
        if not results:
            results = self.memory.query(phi_transformed, k=k, min_sim=0.15)

        elapsed = time.time() - t0

        # Build sources
        sources = []
        for r in results:
            src_meta = r.get("metadata", {})
            sources.append({
                "text": r["text"][:300],
                "sim": round(r["sim"], 4),
                "source": src_meta.get("source", "?"),
                "idx": src_meta.get("idx", -1),
                "filename": src_meta.get("filename", ""),
                "themes": src_meta.get("themes", [])[:3],
            })

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
