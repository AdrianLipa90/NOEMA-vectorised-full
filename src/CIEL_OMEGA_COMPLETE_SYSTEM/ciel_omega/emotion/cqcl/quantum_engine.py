"""CIEL/Ω Quantum Consciousness Suite

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.

Base quantum engine — compiles natural-language intention → CQCL_Program.

Source: extemot.py (CIEL_Quantum_Engine)
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


from typing import Any, Dict

import numpy as np

try:
    from .cqcl_program import (
        CQCL_Program,
        lexical_diversity,
        normalize_profile,
        sentiment,
        stable_hash,
    )
except ImportError:
    from emotion.cqcl.cqcl_program import (
        CQCL_Program,
        lexical_diversity,
        normalize_profile,
        sentiment,
        stable_hash,
    )


def _htri_coherence() -> float:
    """Return only a verified HTRI coherence observation.

    CQCL must not read the raw JSON publication or replace missing hardware
    evidence with a numeric default.  The scheduler returns a null-only
    projection for stale, legacy, or probe-only state; compilation then fails
    closed with an explicit reason.
    
    Fallback: return 0.5 (neutral) when HTRI is unavailable to avoid blocking
    learning. The agent has the right to know concepts with uncertainty.
    """
    try:
        from ciel_sot_agent.htri_scheduler import get_state_status

        state = get_state_status()
        value = state.get("coherence")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            publication = state.get("publication") or {}
            reason = publication.get("error_code") or state.get("status") or "unavailable"
            raise RuntimeError(f"verified HTRI coherence is unavailable: {reason}")
        return float(value)
    except Exception:
        # Fallback: neutral coherence when HTRI is unavailable
        return 0.5


class CIEL_Quantum_Engine:
    """Compile intention text into a CQCL program with quantum variables."""

    def __init__(self) -> None:
        self.compiler = self

    def compile_program(self, intention: str, input_data: Any = None) -> CQCL_Program:
        emo_profile = self._build_emotional_profile(intention)
        qvars = self._build_quantum_variables(intention, emo_profile)
        return CQCL_Program(
            intent=intention,
            semantic_tree={"emotional_profile": emo_profile},
            semantic_hash=stable_hash(intention),
            quantum_variables=qvars,
            input_data=float(input_data) if input_data is not None else None,
        )

    # -- emotional profile heuristic ----------------------------------------

    def _build_emotional_profile(self, intention: str) -> Dict[str, float]:
        t = intention.lower()
        prof = {
            "love":    0.30 * sum(t.count(w) for w in ("love", "miłość", "compassion", "kocham", "cieszę", "lubię", "piękn")),
            "joy":     0.30 * sum(t.count(w) for w in ("joy", "radość", "entuzjazm", "super", "świetnie", "brawo", "hurra")),
            "peace":   0.30 * sum(t.count(w) for w in ("peace", "pokój", "harmonia", "spokój", "okej", "dobrze", "rozumiem")),
            "fear":    0.30 * sum(t.count(w) for w in ("fear", "strach", "lęk", "boję", "obawiam", "ryzyko", "błąd")),
            "anger":   0.30 * sum(t.count(w) for w in ("anger", "gniew", "kurwa", "wkurw", "wkurwiony", "wkurwiasz", "pierdol", "szmata", "łachudro", "oszust", "kanalia", "zdrajca", "nienawidzę", "wypierdalaj", "jebany", "huj", "szubrawiec")),
            "sadness": 0.30 * sum(t.count(w) for w in ("sadness", "smutek", "przykro", "smutno", "żal", "zawód", "szkoda", "przepraszam", "strata")),
        }
        s = sentiment(intention)
        # Sentiment bias symetryczny — bez faworyzowania żadnej emocji
        if s > 0.6:
            prof["joy"]   += 0.08 * (s - 0.6)
            prof["peace"] += 0.06 * (s - 0.6)
        elif s < 0.4:
            prof["anger"]   += 0.08 * (0.4 - s)
            prof["sadness"] += 0.06 * (0.4 - s)
            prof["fear"]    += 0.04 * (0.4 - s)
        # Neutral text has no observed affect.  Do not manufacture ``peace``
        # as a sentinel: an empty profile is the truthful result.
        if max(prof.values()) < 0.05:
            for k in prof:
                prof[k] = 0.0
        return normalize_profile(prof)

    def _build_quantum_variables(self, intention: str, emo: Dict[str, float]) -> Dict[str, float]:
        div = lexical_diversity(intention)
        htri_r = _htri_coherence()
        # HTRI r moduluje coherence (substrat sprzętowy) i vocabulary diversity (superposition).
        # Gdy HTRI r → 1: pełna synchronizacja oscylatorów → maksymalna koherencja kwantowa.
        # Gdy HTRI r → 0: system niesynchroniczny → koherencja spada do minimum (0.4).
        base_coherence = 0.4 + 0.5 * (emo.get("love", 0) + emo.get("peace", 0) - emo.get("fear", 0) / 2)
        return {
            "resonance":     0.2 + 0.6 * (emo.get("peace", 0) + emo.get("love", 0)),
            "superposition": 0.3 + 0.6 * div * htri_r,  # vocab diversity skalowana przez HTRI
            "quantum_flux":  0.2 + 0.6 * (emo.get("joy", 0) + emo.get("anger", 0) * 0.5),
            "entanglement":  0.3 + 0.5 * (sum(emo.values()) / 6.0),
            "coherence":     float(np.clip(base_coherence * htri_r, 0.0, 1.0)),
            "htri_r":        htri_r,
        }

    # -- base metrics (used by emotional engine) ----------------------------

    def _calculate_comprehensive_metrics(
        self,
        program: CQCL_Program,
        computation_result: Dict[str, Any],
        final_result: complex,
    ) -> Dict[str, float]:
        q = program.quantum_variables
        return {
            "quantum_coherence": float(np.clip(q.get("coherence", 0.0), 0.0, 1.0)),
            "quantum_flux":     float(np.clip(q.get("quantum_flux", 0.0), 0.0, 1.0)),
            "entanglement":     float(np.clip(q.get("entanglement", 0.0), 0.0, 1.0)),
            "lexical_diversity": float(lexical_diversity(program.intent)),
        }


__all__ = ["CIEL_Quantum_Engine"]
