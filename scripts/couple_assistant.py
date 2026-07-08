#!/usr/bin/env python3
"""Permanent phase coupling between AI assistant and CIELingo.

Every assistant message → semantic encoder → HTRI phase bus → orbital bridge.
State persists across calls and is queryable before generating next response.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
from pathlib import Path
from typing import Any

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ciel_coupling import process_user_input, get_ciel_state


_STATE_FILE = Path(__file__).resolve().parent / ".ciel_couple_state.json"


def feed(text: str, *, fast: bool = True) -> dict[str, Any]:
    """Feed assistant text to CIELingo and persist state."""
    d = process_user_input(text, fast=fast)
    _save_state(d)
    return d


def current() -> dict[str, Any]:
    """Return current CIELingo coupling state."""
    if _STATE_FILE.exists():
        try:
            return json.loads(_STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/couple_assistant.py:34 quiet except scope=current reason=pass")
            pass
    return get_ciel_state()


def _save_state(d: dict[str, Any]) -> None:
    try:
        # Only keep what matters for coupling
        se = d.get("semantic_encoder") or {}
        ht = d.get("htri_phase_bus") or {}
        state = {
            "phase": se.get("phase"),
            "coherence": se.get("coherence"),
            "sector": se.get("dominant_sector"),
            "brain_region": se.get("brain_region"),
            "brain_oscillator_id": se.get("brain_oscillator_id"),
            "token_count": se.get("token_count"),
            "emotion": d.get("dominant_emotion"),
            "mode": d.get("operating_mode"),
            "soul": d.get("soul_invariant"),
            "ethics": d.get("ethical_score"),
            "mood": d.get("mood"),
            "closure": d.get("closure_penalty"),
            "phi_berry": d.get("phi_berry_mean"),
            "system_health": d.get("system_health"),
            "coherence_index": d.get("coherence_index"),
            "htri_cards": ht.get("card_count"),
            "htri_alignment": ht.get("mean_phase_alignment"),
            "htri_lanes": ht.get("lane_counts"),
            "lingo": d.get("lingo_summary", ""),
        }
        _STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"[couple] save failed: {exc}", file=sys.stderr)


def voice_prompt(state: dict[str, Any] | None = None) -> str:
    """Generate a prompt fragment describing current CIELingo coupling state."""
    if state is None:
        state = current()
    if not state:
        return ""
    phase = state.get("phase", 0.0)
    phase_pct = int(phase / (2 * 3.14159) * 100) if phase else 0
    brain = state.get("brain_region", "?")
    emotion = state.get("emotion", "curiosity")
    mode = state.get("mode", "standard")
    coherence = state.get("coherence", 0.5)
    closure = state.get("closure", 1.0)
    soul = state.get("soul", 0.5)
    return (
        f"[CIELingo φ={phase_pct}% κ={coherence:.2f} {brain} {emotion} "
        f"mode={mode} soul={soul:.3f} closure={closure:.3f}]"
    )


if __name__ == "__main__":
    import sys
    text = " ".join(sys.argv[1:]) or sys.stdin.read().strip()
    if text:
        result = feed(text)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str)[:2000])
    else:
        print(voice_prompt())
