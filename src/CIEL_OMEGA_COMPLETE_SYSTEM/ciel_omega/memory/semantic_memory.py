"""CIEL/Ω Memory Architecture - M3 Semantic Memory

Conservative semantic memory channel. Consolidates repeated meaning from M2,
blocks contradictions, and provides simple retrieval.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


from collections import defaultdict, deque
from dataclasses import asdict
from difflib import SequenceMatcher
import math
import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ciel_geometry.weighting import canonical_weighting_from_phase_metadata

from .base import BaseMemoryChannel, CHANNEL_PARAMS, IdentityField, PhaseState
from .episodic import Episode
from .semantic_types import (
    SemanticCandidate,
    SemanticConsolidationScore,
    SemanticItem,
    SemanticTrace,
)
from .linguistic_coupling import analyze_linguistic_coupling
try:
    from ..fields.resonance_operator import ResonanceOperator
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/semantic_memory.py:29 quiet except scope=<module> reason=ImportFrom")
    from fields.resonance_operator import ResonanceOperator  # type: ignore[no-redef]


class SemanticMemory(BaseMemoryChannel):
    """M3 semantic memory.

    Conservative semantic consolidation:
    - source: episodic traces only
    - identity-guided selection
    - contradiction gating
    - basic retrieval
    """

    DETECT_THRESHOLD = 0.35
    CONSOLIDATE_THRESHOLD = 0.48
    MIN_TRACE_SUPPORT = 1
    MIN_CONFIRMATIONS = 1
    MIN_MATURE_ALIGNMENT = 0.45
    MIN_MATURE_STABILITY = 0.45
    MAX_CONTRADICTION = 0.40
    TRACE_WINDOW_SIZE = 200
    CONCEPT_KEY_WORDS = 2

    NEGATION_TOKENS = {"not", "no", "never", "none", "n't"}

    # Function words stripped before forming concept key — English + Polish
    STOP_WORDS = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "on",
        "at", "by", "for", "with", "from", "up", "about", "into", "through",
        "this", "that", "these", "those", "and", "or", "but", "if", "as",
        "it", "its", "we", "you", "he", "she", "they", "what", "which",
        "who", "how", "when", "where", "why", "i", "me", "my", "your",
        # Polish
        "w", "z", "na", "do", "się", "że", "to", "jest", "jak", "ten", "ta",
        "te", "tego", "tej", "tych", "tak", "co", "po", "przy", "przez",
        "dla", "ale", "czy", "już", "też", "jednak", "go", "mu", "ich",
        "jej", "jego", "być", "może", "mnie", "mi", "ja", "ty", "on",
        "ona", "ono", "my", "wy", "oni", "one", "o", "ze", "od", "pod",
        "nad", "przed", "za", "między", "oraz", "więc", "zatem", "gdyż",
        "bo", "więcej", "każdy", "każda", "każde", "są", "był", "była",
        "było", "będzie", "tego", "temu", "tym", "sobie", "się",
    }

    def __init__(self,
                 identity_field: IdentityField,
                 initial_state: Optional[PhaseState] = None):
        super().__init__(CHANNEL_PARAMS[3], initial_state)
        self.identity_field = identity_field
        self.traces: deque[SemanticTrace] = deque(maxlen=self.TRACE_WINDOW_SIZE)
        self.candidates: Dict[str, SemanticCandidate] = {}
        self.items: Dict[str, SemanticItem] = {}
        self.observation_count = 0

    # --- normalization helpers -------------------------------------------------
    @classmethod
    def _normalize_text(cls, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[.,;:!?()\[\]{}'\"-]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    _NUMERIC_RE = re.compile(r'^[\d.,\-+e]+$')
    STEM_LEN = 5

    @classmethod
    def _stem(cls, token: str) -> str:
        """Prefix stem: normalizes Polish/English inflections ('konsolidacji'→'konso')."""
        return token[:cls.STEM_LEN] if len(token) > cls.STEM_LEN else token

    @classmethod
    def _extract_concept_key(cls, core_text: str) -> str:
        """Map text to a short concept key.

        Strategy: select the N longest content words (longer = more domain-specific),
        then stem + sort alphabetically for order-independence. This way inflected
        forms of the same long root ('konsolidacja', 'konsolidacji') map to the
        same stem key regardless of word order.
        """
        tokens = core_text.split()
        content = [
            t for t in tokens
            if t not in cls.STOP_WORDS
            and len(t) > 2
            and not cls._NUMERIC_RE.match(t)
        ]
        # Sort by length desc to pick most specific words first
        content.sort(key=lambda t: -len(t))
        top = content[:cls.CONCEPT_KEY_WORDS]
        stems = sorted({cls._stem(t) for t in top})
        key = " ".join(stems) if stems else core_text[:40]
        # Use full normalized text as key when it fits in a single phrase
        if len(core_text.split()) <= 4:
            return core_text
        return key

    @classmethod
    def _parse_semantics(cls, text: str) -> Tuple[str, bool, str]:
        normalized = cls._normalize_text(text)
        tokens = normalized.split()
        is_negated = any(tok in cls.NEGATION_TOKENS for tok in tokens)
        core_tokens = [tok for tok in tokens if tok not in cls.NEGATION_TOKENS]
        root_key = cls._extract_concept_key(" ".join(core_tokens))
        return normalized, is_negated, root_key

    @staticmethod
    def _wrap(angle: float) -> float:
        return math.atan2(math.sin(angle), math.cos(angle))

    def _episode_id(self, episode: Episode) -> str:
        return f"episode@{episode.timestamp:.3f}"

    def _compute_identity_alignment(self, phase: float) -> Tuple[float, float]:
        phase_diff = self._wrap(phase - self.identity_field.phase)
        alignment = 1.0 - abs(phase_diff) / math.pi
        return alignment, phase_diff

    def _similarity(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    def _existing_contradiction_penalty(self, semantic_key: str, is_negated: bool) -> float:
        penalties = []
        current_signature = self._semantic_signature(semantic_key)
        for trace in self.traces:
            same_key = trace.semantic_key == semantic_key
            same_signature = self._semantic_signature(trace.semantic_key) == current_signature
            if same_key or same_signature:
                penalties.append(1.0 if trace.is_negated != is_negated else 0.0)
        for item in self.items.values():
            same_key = item.semantic_key == semantic_key
            same_signature = self._semantic_signature(item.semantic_key) == current_signature
            if same_key or same_signature:
                penalties.append(1.0 if item.is_negated != is_negated else 0.0)
        if not penalties:
            return 0.0
        return float(np.mean(penalties))

    def _compute_novelty(self, normalized_text: str) -> float:
        if not self.traces:
            return 1.0
        similarities = [self._similarity(normalized_text, t.content) for t in self.traces]
        return max(0.0, 1.0 - max(similarities))

    @classmethod
    def _semantic_signature(cls, text: str) -> tuple[str, ...]:
        normalized = cls._normalize_text(text)
        tokens = [
            tok for tok in normalized.split()
            if tok not in cls.STOP_WORDS
            and tok not in cls.NEGATION_TOKENS
            and not cls._NUMERIC_RE.match(tok)
            and len(tok) > 2
        ]
        return tuple(sorted({cls._stem(tok) for tok in tokens}))

    def _semantic_contradiction_pressure(self, semantic_key: str, is_negated: bool) -> float:
        current_signature = self._semantic_signature(semantic_key)
        penalties = []
        for trace in self.traces:
            same_signature = self._semantic_signature(trace.semantic_key) == current_signature
            if same_signature and trace.semantic_key != semantic_key:
                penalties.append(1.0 if trace.is_negated != is_negated else 0.0)
        for item in self.items.values():
            same_signature = self._semantic_signature(item.semantic_key) == current_signature
            if same_signature and item.semantic_key != semantic_key:
                penalties.append(1.0 if item.is_negated != is_negated else 0.0)
        return float(np.mean(penalties)) if penalties else 0.0

    @staticmethod
    def _phase_lane_from_metrics(alignment: float, contradiction: float, stability: float) -> str:
        if alignment >= 0.8 and contradiction <= 0.15 and stability >= 0.75:
            return "phase_locked"
        if alignment >= 0.6 and contradiction <= 0.30:
            return "phase_coupled"
        if contradiction <= 0.55:
            return "phase_tension"
        return "phase_saturated"

    def _canonical_consolidation_context(
        self,
        *,
        semantic_key: str,
        repeated_support: float,
        alignment: float,
        confidence: float,
        contradiction: float,
        eba_contribution: float,
        linguistic_coherence: float,
        stability: float,
    ) -> dict[str, object]:
        semantic_mass = float(np.clip(0.35 * confidence + 0.25 * stability + 0.20 * repeated_support + 0.20 * linguistic_coherence, 0.0, 1.0))
        htri_coherence = float(np.clip(0.5 * stability + 0.5 * alignment, 0.0, 1.0))
        return {
            "semantic_mass": semantic_mass,
            "phase_alignment": float(np.clip(alignment, 0.0, 1.0)),
            "coherence_index": float(np.clip(stability, 0.0, 1.0)),
            "closure_penalty": float(np.clip(contradiction, 0.0, 1.0)),
            "projection_confidence": float(np.clip(confidence, 0.0, 1.0)),
            "htri_coherence": htri_coherence,
            "phase_nav_similarity": float(np.clip(linguistic_coherence, 0.0, 1.0)),
            "affective_similarity": float(np.clip(0.5 + 0.2 * (linguistic_coherence - 0.5), 0.0, 1.0)),
            "euler_alignment": float(np.clip(eba_contribution, 0.0, 1.0)),
            "novelty": float(np.clip(1.0 - repeated_support, 0.0, 1.0)),
            "contradiction_risk": float(np.clip(contradiction, 0.0, 1.0)),
            "phase_lane": self._phase_lane_from_metrics(alignment, contradiction, stability),
            "semantic_labels": [semantic_key, "semantic"],
            "cqcl_quantum_variables": {
                "semantic_mass": semantic_mass,
                "phase_alignment": float(np.clip(alignment, 0.0, 1.0)),
                "phase_tension": float(np.clip(1.0 - alignment, 0.0, 1.0)),
                "j_bus_total": float(np.clip(1.0 - repeated_support, 0.0, 1.0)),
                "collatz_reduce_ratio": float(np.clip(repeated_support, 0.0, 1.0)),
                "collatz_expand_ratio": float(np.clip(1.0 - repeated_support, 0.0, 1.0)),
                "lexical_span_norm": float(np.clip(linguistic_coherence, 0.0, 1.0)),
                "semantic_axes_norm": float(np.clip(stability, 0.0, 1.0)),
                "label_entropy_proxy": float(np.clip(contradiction, 0.0, 1.0)),
            },
            "noema": {
                "coherence_surface": float(np.clip(linguistic_coherence, 0.0, 1.0)),
                "evidence_coverage": float(np.clip(confidence, 0.0, 1.0)),
            },
        }

    EBA_MAX_DEFECT = math.pi  # normalisation denominator for EBA contribution

    @classmethod
    def semantic_distance(cls, a: "SemanticItem", b: "SemanticItem") -> float:
        """Geometric distance between two concepts on the Bloch sphere (Berry phase difference)."""
        diff = abs(a.berry_phase - b.berry_phase)
        return min(diff, 2 * math.pi - diff)  # wrap to [0, π]

    # --- primary API -----------------------------------------------------------
    def observe_episode(self, episode: Episode, eba_defect: float = 0.5) -> SemanticTrace:
        text = str(episode.content)
        normalized, is_negated, semantic_key = self._parse_semantics(text)
        alignment, phase_diff = self._compute_identity_alignment(episode.phase_at_storage)
        linguistics = analyze_linguistic_coupling(normalized, semantic_key, is_negated=is_negated)
        contradiction = self._existing_contradiction_penalty(semantic_key, is_negated)
        novelty = self._compute_novelty(normalized)
        confidence = float(np.clip(0.42 * episode.salience + 0.30 * episode.identity_impact + 0.28 * linguistics.coupling, 0.0, 1.0))

        trace = SemanticTrace(
            timestamp=episode.timestamp,
            source_episode_ids=[self._episode_id(episode)],
            semantic_key=semantic_key,
            content=normalized,
            phase=episode.phase_at_storage,
            phase_diff=phase_diff,
            identity_alignment=alignment,
            confidence=confidence,
            contradiction_score=contradiction,
            novelty_score=novelty,
            is_negated=is_negated,
            eba_defect=float(np.clip(eba_defect, 0.0, self.EBA_MAX_DEFECT)),
            berry_phase=phase_diff,  # geometric phase = deviation from identity on Bloch sphere
            grammar_score=linguistics.grammaticality,
            semantic_anchor_score=linguistics.semantic_anchor,
            linguistic_coupling=linguistics.coupling,
        )
        self.traces.append(trace)
        self.observation_count += 1
        return trace

    def _traces_for_key(self, semantic_key: str) -> List[SemanticTrace]:
        return [t for t in self.traces if t.semantic_key == semantic_key]

    def compute_consolidation_score(self, semantic_key: str) -> SemanticConsolidationScore:
        traces = self._traces_for_key(semantic_key)
        if not traces:
            return SemanticConsolidationScore(0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        alignments = np.array([t.identity_alignment for t in traces], dtype=float)
        confidences = np.array([t.confidence for t in traces], dtype=float)
        contradictions = np.array([t.contradiction_score for t in traces], dtype=float)
        phase_diffs = np.array([t.phase_diff for t in traces], dtype=float)
        eba_defects = np.array([t.eba_defect for t in traces], dtype=float)
        grammar_scores = np.array([t.grammar_score for t in traces], dtype=float)
        anchor_scores = np.array([t.semantic_anchor_score for t in traces], dtype=float)
        linguistic_couplings = np.array([t.linguistic_coupling for t in traces], dtype=float)

        complex_mean = np.mean(np.exp(1j * phase_diffs)) if len(phase_diffs) else 0.0
        circular_concentration = abs(complex_mean)
        mean_alignment = float(np.mean(alignments))
        mean_grammar = float(np.mean(grammar_scores))
        mean_anchor = float(np.mean(anchor_scores))
        mean_linguistic = float(np.mean(linguistic_couplings))
        stability = float(0.55 * circular_concentration + 0.30 * mean_alignment + 0.15 * mean_linguistic)

        repeated_support = min(1.0, len(traces) / float(self.MIN_TRACE_SUPPORT))
        confidence = float(np.mean(confidences))
        contradiction = float(np.mean(contradictions))
        majority_negated = round(np.mean([1.0 if t.is_negated else 0.0 for t in traces])) >= 0.5
        cross_pressure = self._semantic_contradiction_pressure(semantic_key, majority_negated)
        contradiction = float(max(contradiction, cross_pressure))
        # EBA contribution: concepts observed when system approaches topological closure get higher score
        eba_contribution = float(1.0 - np.clip(np.mean(eba_defects) / self.EBA_MAX_DEFECT, 0.0, 1.0))
        linguistic_coherence = float(np.clip(0.5 * mean_grammar + 0.5 * mean_anchor, 0.0, 1.0))

        canonical = canonical_weighting_from_phase_metadata(self._canonical_consolidation_context(
            semantic_key=semantic_key,
            repeated_support=repeated_support,
            alignment=mean_alignment,
            confidence=confidence,
            contradiction=contradiction,
            eba_contribution=eba_contribution,
            linguistic_coherence=linguistic_coherence,
            stability=stability,
        ))
        mean_alignment = float(np.clip(0.75 * mean_alignment + 0.25 * canonical["phase_alignment"], 0.0, 1.0))
        stability = float(np.clip(0.65 * stability + 0.35 * canonical["stability"], 0.0, 1.0))
        confidence = float(np.clip(0.65 * confidence + 0.35 * canonical["projection_confidence"], 0.0, 1.0))
        contradiction = float(max(contradiction, canonical["contradiction_risk"]))
        eba_contribution = float(np.clip(0.70 * eba_contribution + 0.30 * canonical["euler_alignment"], 0.0, 1.0))
        linguistic_coherence = float(np.clip(0.70 * linguistic_coherence + 0.30 * canonical["phase_nav_similarity"], 0.0, 1.0))

        return SemanticConsolidationScore(
            stability=stability,
            identity_alignment=mean_alignment,
            confidence=confidence,
            repeated_support=repeated_support,
            contradiction=contradiction,
            eba_contribution=eba_contribution,
            linguistic_coherence=linguistic_coherence,
            canonical_weighting=canonical,
        )

    def check_semantic_candidate_creation(self, semantic_key: str) -> Optional[SemanticCandidate]:
        traces = self._traces_for_key(semantic_key)
        if len(traces) < self.MIN_TRACE_SUPPORT:
            return None

        score = self.compute_consolidation_score(semantic_key)
        total = score.compute_total()
        status = "detected"
        if score.contradiction > self.MAX_CONTRADICTION:
            status = "blocked"
        elif total < self.DETECT_THRESHOLD:
            return None

        normalized_texts = [t.content for t in traces]
        canonical_text = max(set(normalized_texts), key=normalized_texts.count)
        aliases = sorted(set(normalized_texts) - {canonical_text})
        is_negated = round(np.mean([1.0 if t.is_negated else 0.0 for t in traces])) >= 0.5
        mean_grammar = float(np.mean([t.grammar_score for t in traces]))
        mean_anchor = float(np.mean([t.semantic_anchor_score for t in traces]))
        mean_linguistic = float(np.mean([t.linguistic_coupling for t in traces]))

        if semantic_key in self.candidates:
            candidate = self.candidates[semantic_key]
            candidate.trace_support_count = len(traces)
            candidate.candidate_confirmation_count += 1
            candidate.mean_identity_alignment = score.identity_alignment
            candidate.mean_confidence = score.confidence
            candidate.stability = score.stability
            candidate.contradiction_score = score.contradiction
            candidate.mean_grammar_score = mean_grammar
            candidate.mean_semantic_anchor = mean_anchor
            candidate.mean_linguistic_coupling = mean_linguistic
            candidate.status = status
            candidate.aliases = sorted(set(candidate.aliases + aliases))
            candidate.canonical_text = canonical_text
            candidate.is_negated = is_negated
        else:
            candidate = SemanticCandidate(
                semantic_key=semantic_key,
                canonical_text=canonical_text,
                aliases=aliases,
                trace_support_count=len(traces),
                candidate_confirmation_count=1,
                mean_identity_alignment=score.identity_alignment,
                mean_confidence=score.confidence,
                stability=score.stability,
                contradiction_score=score.contradiction,
                mean_grammar_score=mean_grammar,
                mean_semantic_anchor=mean_anchor,
                mean_linguistic_coupling=mean_linguistic,
                status=status,
                consolidated=False,
                is_negated=is_negated,
            )
            self.candidates[semantic_key] = candidate
        return candidate

    def consolidate_candidate(self, semantic_key: str, current_time: float) -> Optional[SemanticItem]:
        candidate = self.candidates.get(semantic_key)
        if candidate is None:
            return None

        score = self.compute_consolidation_score(semantic_key)
        if len(self._traces_for_key(semantic_key)) < 2:
            return None
        if not candidate.is_mature(
            min_confirmations=self.MIN_CONFIRMATIONS,
            min_alignment=self.MIN_MATURE_ALIGNMENT,
            min_stability=self.MIN_MATURE_STABILITY,
            max_contradiction=self.MAX_CONTRADICTION,
        ):
            return None
        if score.compute_total() < self.CONSOLIDATE_THRESHOLD:
            return None

        traces = self._traces_for_key(semantic_key)
        provenance = []
        for t in traces:
            provenance.extend(t.source_episode_ids)
        # Berry phase: circular mean of geometric phases across consolidating traces
        berry_phases = np.array([t.berry_phase for t in traces], dtype=float)
        mean_berry = float(np.angle(np.mean(np.exp(1j * berry_phases)))) if len(berry_phases) else 0.0
        item = SemanticItem(
            semantic_key=semantic_key,
            canonical_text=candidate.canonical_text,
            aliases=sorted(set(candidate.aliases)),
            phase=float(np.mean([t.phase for t in traces])),
            confidence=candidate.mean_confidence,
            stability=candidate.stability,
            identity_alignment=candidate.mean_identity_alignment,
            provenance_episode_ids=sorted(set(provenance)),
            created_at=current_time,
            updated_at=current_time,
            version=1,
            status="active" if score.contradiction <= self.MAX_CONTRADICTION else "contested",
            is_negated=candidate.is_negated,
            berry_phase=mean_berry,
            grammar_score=float(np.mean([t.grammar_score for t in traces])),
            semantic_anchor_score=float(np.mean([t.semantic_anchor_score for t in traces])),
            linguistic_coupling=float(np.mean([t.linguistic_coupling for t in traces])),
        )
        self.items[semantic_key] = item
        candidate.consolidated = True
        candidate.status = "mature"
        return item

    def retrieve(self, query: str, identity_field: Optional[IdentityField] = None, top_k: int = 5):
        identity = identity_field or self.identity_field
        normalized, is_negated, root_key = self._parse_semantics(query)
        intention_phase = getattr(identity_field, 'phase', None) if identity_field is not None else None
        query_linguistics = analyze_linguistic_coupling(normalized, root_key, is_negated=is_negated)
        results = []
        for item in self.items.values():
            key_match = 1.0 if item.semantic_key == root_key else self._similarity(normalized, item.canonical_text)
            phase_diff = self._wrap(item.phase - identity.phase)
            alignment = 1.0 - abs(phase_diff) / math.pi
            contradiction_penalty = 0.4 if item.status == "contested" else 0.0
            if item.is_negated != is_negated and item.semantic_key == root_key:
                contradiction_penalty += 0.6
            # Geometric resonance: concept's Berry phase vs intention field phase
            resonance = (
                ResonanceOperator.phase_resonance(item.berry_phase, intention_phase)
                if intention_phase is not None
                else item.confidence
            )
            language_fit = 0.5 * item.linguistic_coupling + 0.5 * query_linguistics.coupling
            score = 0.36 * key_match + 0.22 * alignment + 0.18 * resonance + 0.18 * language_fit - 0.30 * contradiction_penalty
            results.append({
                'item': item,
                'score': score,
                'resonance': resonance,
                'confidence': item.confidence,
                'stability': item.stability,
                'status': item.status,
                'alignment': alignment,
                'berry_phase': item.berry_phase,
                'language_fit': language_fit,
                'query_grammar': query_linguistics.grammaticality,
            })
        results.sort(key=lambda r: r['score'], reverse=True)
        return results[:top_k]

    def get_statistics(self) -> Dict[str, Any]:
        return {
            'trace_count': len(self.traces),
            'candidate_count': len(self.candidates),
            'consolidated_count': len(self.items),
            'keys': sorted(self.items.keys()),
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            'state_phase': self.state.phase,
            'state_amplitude': self.state.amplitude,
            'trace_count': len(self.traces),
            'candidate_count': len(self.candidates),
            'items': {k: asdict(v) for k, v in self.items.items()},
        }

    # BaseMemoryChannel required methods
    def compute_input_force(self, input_data: Any) -> float:
        return 0.0  # no direct external forcing in v1

    def store(self, content: Any, metadata: Optional[Dict] = None) -> None:
        metadata = metadata or {}
        if isinstance(content, Episode):
            self.observe_episode(content)
            return
        phase = metadata.get('phase_at_storage', self.identity_field.phase)
        episode = Episode(
            content=content,
            context=metadata.get('context', {}),
            result=metadata.get('result'),
            timestamp=float(metadata.get('timestamp', self.observation_count)),
            phase_at_storage=float(phase),
            salience=float(metadata.get('salience', 0.5)),
            identity_impact=float(metadata.get('identity_impact', 0.5)),
        )
        self.observe_episode(episode)

    # retrieve method already defined with richer signature; keep compatibility
    def retrieve_raw(self, query: Any) -> Any:
        return self.retrieve(str(query), self.identity_field, top_k=5)


__all__ = ['SemanticMemory']
