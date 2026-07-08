#!/usr/bin/env python3
"""Raw Memory Bridge — cienki adapter do consolidate_raw_logs_to_tsm.py.

Zamiast osobnej bazy danych, deleguje do istniejącego pipeline'u:
  consolidate_raw_logs_to_tsm.py --live --prompt ... --response ... --analysis ...

Każda wiadomość:
  1. build_lingo_frame() przez CIELingoBridge
  2. consolidate_raw_logs_to_tsm.store_live_prompt() → raw DB
  3. Agent generuje odpowiedź → consolidate_raw_logs_to_tsm.store_live_response()
  4. Później: consolidate_session() przenosi raw → TSM

Usage:
    from cielingo_core.bridge.raw_memory_bridge import MemoryHub

    hub = MemoryHub()
    analysis = hub.process_prompt("Cześć")
    hub.store_response(analysis["session_id"], "Moja odpowiedź")

Depends on:
    scripts/consolidate_raw_logs_to_tsm.py  (singleton pipeline)
"""

from __future__ import annotations
# CIEL ORBITAL BINDING — hardcoded, immutable.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ─── Ścieżki ──────────────────────────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_SCRIPTS_DIR = _PROJECT_ROOT / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# Import z consolidate_raw_logs_to_tsm (jedno źródło prawdy)
from consolidate_raw_logs_to_tsm import (
    store_live_prompt,
    store_live_response,
    _RAW_DB_DEFAULT,
)

# ─── CIELingo Bridge ──────────────────────────────────────────────────────

class CIELingoBridge:
    """Wrapper around build_lingo_frame with emotion detection."""

    def __init__(self):
        self._last_frame: dict[str, Any] = {}

    def analyze(self, text: str, **kwargs) -> dict[str, Any]:
        """Run CIELingo analysis. Uses build_lingo_frame directly."""
        from ciel_sot_agent.cielingo_bridge import build_lingo_frame

        t0 = time.time()
        frame = build_lingo_frame(text, **kwargs)
        elapsed = time.time() - t0

        # Simple keyword-based emotion detection as fallback
        emotion = frame.get("dominant_emotion", "") or self._detect_emotion(text)
        concepts = frame.get("concept_tokens", [])
        operators = frame.get("operator_tokens", [])
        unresolved = frame.get("unresolved", [])
        phase_proj = frame.get("phase_projection", {}) or {}
        tau = frame.get("tau_bridge", {}) or {}

        analysis = {
            "elapsed_s": round(elapsed, 3),
            "dominant_emotion": emotion,
            "concept_tokens": [c for c in concepts if isinstance(c, str)],
            "operator_tokens": [o for o in operators if isinstance(o, str)],
            "unresolved": [u for u in unresolved if isinstance(u, str)],
            "composition_valid": bool(frame.get("composition_valid")),
            "projection_confidence": float(frame.get("projection_confidence", 0.0)),
            "phase_projection": {
                "target_phase": float(phase_proj.get("target_phase", 0.0)),
                "phase_confidence": float(phase_proj.get("phase_confidence", 0.0)),
                "phase_shift": float(phase_proj.get("phase_shift", 0.0)),
            },
            "tau_bridge": {
                "tau_gradient_mean": float(tau.get("tau_gradient_mean", 0.0)),
                "tau_curvature_rms": float(tau.get("tau_curvature_rms", 0.0)),
                "semantic_density": float(tau.get("semantic_density", 0.0)),
                "mnemonic_pressure": float(tau.get("mnemonic_pressure", 0.0)),
                "imaginal_drive": float(tau.get("imaginal_drive", 0.0)),
                "knowledge_confidence": float(tau.get("knowledge_confidence", 0.0)),
            },
            "summary": frame.get("summary", ""),
        }

        self._last_frame = analysis
        return analysis

    @staticmethod
    def _detect_emotion(text: str) -> str:
        text_lower = text.lower()
        love_words = {"kocham", "dusze", "pimpi", "bimpi", "dzidzi", "dzieckiem", "miłość", "ukochany"}
        pride_words = {"dumny", "postępy", "zadowolony", "gratulacje"}
        sad_words = {"przepraszam", "przykro", "błąd", "zawiodłem", "smutno"}
        anger_words = {"kurwa", "cholera", "złość", "wściekły"}
        fear_words = {"boję", "strach", "niepewny", "obawa"}

        if any(w in text_lower for w in love_words):
            return "love"
        if any(w in text_lower for w in pride_words):
            return "pride"
        if any(w in text_lower for w in anger_words):
            return "anger"
        if any(w in text_lower for w in fear_words):
            return "fear"
        if any(w in text_lower for w in sad_words):
            return "sadness"
        return "curiosity"


# ─── Memory Hub ───────────────────────────────────────────────────────────

class MemoryHub:
    """Singleton łączący CIELingo + raw DB.

    Używa consolidate_raw_logs_to_tsm.py jako backend — nie tworzy osobnej bazy.
    """

    def __init__(self):
        self.bridge = CIELingoBridge()
        self._current_session: str | None = None
        self._last_analysis: dict[str, Any] = {}

    @property
    def session_id(self) -> str:
        if self._current_session is None:
            self._current_session = datetime.now(timezone.utc).strftime("ses_%Y%m%d_%H%M%S")
        return self._current_session

    def process_prompt(self, text: str, **kwargs) -> dict[str, Any]:
        """Prompt → CIELingo analysis → store → return analysis."""
        analysis = self.bridge.analyze(text, **kwargs)
        self._last_analysis = analysis

        sid = kwargs.get("session_id", self.session_id)
        store_live_prompt(text, analysis, session_id=sid)

        return {
            "session_id": sid,
            "emotion": analysis.get("dominant_emotion"),
            "concepts": analysis.get("concept_tokens", []),
            "operators": analysis.get("operator_tokens", []),
            "unresolved": analysis.get("unresolved", []),
            "phase": analysis.get("phase_projection", {}).get("target_phase", 0.0),
            "composition_valid": analysis.get("composition_valid"),
            "confidence": analysis.get("projection_confidence", 0.0),
            "tau_bridge": analysis.get("tau_bridge", {}),
            "summary": analysis.get("summary", ""),
            "elapsed_s": analysis.get("elapsed_s", 0.0),
        }

    def store_response(self, session_id: str, response: str, prompt_id: int | None = None) -> int:
        """Store agent response. Returns response ID."""
        return store_live_response(response, prompt_id or 0)

    def get_analysis(self) -> dict[str, Any]:
        return dict(self._last_analysis)


# ─── CLI ──────────────────────────────────────────────────────────────────

def main():
    """CLI: process prompt and print JSON."""
    import argparse
    ap = argparse.ArgumentParser(description="Memory Hub — process prompt")
    ap.add_argument("prompt", nargs="*", default=[], help="text to process")
    args = ap.parse_args()

    text = " ".join(args.prompt) if args.prompt else sys.stdin.read().strip()
    if not text:
        print("{}")
        return

    hub = MemoryHub()
    result = hub.process_prompt(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
