"""PhaseNav Φ-bypass — use PhaseNav as a coding language to bypass bottlenecks.

PhaseNav operator coding:
  Φ_bypass = IDENTITY ⊕ DIFFERENCE ⊕ ORDER ⊕ COMPOSITION ⊕ ADDITION
  Each operator maps to an M0-M7 oscillator channel, converting abstract
  pipeline metrics into concrete 24D phase values.

Usage:
  from ciel_geometry.phasenav_bypass import phasenav_bypass
  enriched = phasenav_bypass(text, engine_state)
  # enriched["phi_24d"] — 24 oscillator phases
  # enriched["bypass_lane"] — operator chain used
"""

from __future__ import annotations

import hashlib
import logging
import math
from typing import Any

import numpy as np

_log = logging.getLogger("PhaseNav.Bypass")

# PhaseNav operator kinds (from operator_algebra: 18 kinds)
IDENTITY = 0
DIFFERENCE = 1
ORDER = 2
COMPOSITION = 3
ADDITION = 4
FORCE = 5
NEGATION = 6
TRANSFORM = 7
RETURN = 8
FOLD = 9
BOUNDARY = 10
SCOPE = 11
AFFECT = 12
CONSENT = 13
SOURCE = 14
MEMORY = 15
RISK = 16

# M0-M7 oscillator channel mapping (3 oscillators each = 24 total)
CHANNEL_MAP = {
    "M0": (0, 2),     # Perception — IDENTITY, DIFFERENCE
    "M1": (3, 5),     # AGENT — ORDER, COMPOSITION
    "M2": (6, 8),     # MEMORY — ADDITION, RETURN
    "M3": (9, 11),    # Cognition/Rules — FORCE, NEGATION
    "M4": (12, 14),   # Procedural — TRANSFORM, FOLD
    "M5": (15, 17),   # Semantics — BOUNDARY, SCOPE
    "M6": (18, 20),   # Emotion — AFFECT, CONSENT
    "M7": (21, 23),   # Braid/Integration — SOURCE, MEMORY, RISK
}

def _text_to_phi(text: str) -> float:
    h = hashlib.sha256(text.encode()).digest()
    return (int.from_bytes(h[:4], "big") / 0xFFFFFFFF) * 2 * math.pi

def _operator_from_hash(text: str) -> int:
    h = hashlib.sha256(text.encode()).digest()
    return int.from_bytes(h[:1], "big") % 17  # 0-16

def _build_phi_24d(text: str, engine_state: dict | None = None) -> np.ndarray:
    """Build 24D phase vector from PhaseNav operators applied to engine state."""
    phi_24d = np.zeros(24, dtype=np.float64)
    es = engine_state or {}

    # IDENTITY → M0: text hash as base phase
    base_phi = _text_to_phi(text)
    phi_24d[0:3] = base_phi

    # DIFFERENCE → M0: emotional differential (valence offset)
    emotion = es.get("dominant_emotion", "neutral")
    emotion_seed = abs(hash(emotion)) / 0xFFFFFFFF
    phi_24d[1:3] = emotion_seed * np.pi

    # ORDER → M1: collatz orbit length
    orbit_len = es.get("collatz_path_length", 0) or 0
    if orbit_len > 0:
        order_phase = 2 * math.pi * min(orbit_len / 512, 1.0)
        phi_24d[3] = order_phase

    # COMPOSITION → M1: ethics + mood composite
    mood = es.get("mood", 0.5)
    ethics = es.get("ethical_score", 0.5)
    composite = 2 * math.pi * (0.5 * mood + 0.5 * ethics)
    phi_24d[4:6] = composite

    # ADDITION → M2: attractor score
    attractor = es.get("collatz_runtime", {}).get("attractor_score", 0.0)
    phi_24d[6] = 2 * math.pi * min(attractor, 1.0)

    # RETURN → M2: parity entropy
    parity = es.get("collatz_runtime", {}).get("parity_entropy", 0.0)
    phi_24d[7:9] = 2 * math.pi * min(parity / 2.0, 1.0)

    # FORCE → M3: emotional intensity
    intensity = es.get("cqcl_metrics", {}).get("emotional_intensity", 0.5)
    phi_24d[9:12] = 2 * math.pi * min(intensity, 1.0)

    # TRANSFORM → M4: coherence from simulation
    coherence = es.get("simulation", {}).get("coherence", [0.5])
    mean_c = float(np.mean(coherence)) if isinstance(coherence, list) else 0.5
    phi_24d[12:15] = 2 * math.pi * min(mean_c, 1.0)

    # BOUNDARY → M5: soul invariant
    soul = es.get("soul_invariant", 0.0)
    phi_24d[15:18] = 2 * math.pi * min(abs(soul), 1.0)

    # AFFECT → M6: emotional intensity (redundant for stability)
    phi_24d[18:21] = 2 * math.pi * min(intensity * 0.5 + 0.25, 1.0)

    # MEMORY + RISK → M7: braid phase (highest harmonic)
    euler_v = es.get("collatz_runtime", {}).get("phase", {}).get("euler_violation", 0.0)
    phi_24d[21] = 2 * math.pi * min(abs(euler_v), 1.0)
    phi_24d[22] = base_phi * 0.5 + emotion_seed * math.pi * 0.5
    phi_24d[23] = 2 * math.pi * min(ethics * 0.3 + 0.7 * mood, 1.0)

    return phi_24d % (2 * math.pi)


def _build_bypass_lane(text: str, engine_state: dict | None = None) -> list[str]:
    """Determine which PhaseNav operator chain was applied."""
    op = _operator_from_hash(text)
    lanes = {
        IDENTITY: "identity → m0_perception",
        DIFFERENCE: "difference → m0_emotion_offset",
        ORDER: "order → m1_collatz_orbit",
        COMPOSITION: "composition → m1_ethics_mood",
        ADDITION: "addition → m2_attractor",
        FORCE: "force → m3_intensity",
        NEGATION: "negation → m3_inhibition",
        TRANSFORM: "transform → m4_coherence",
        RETURN: "return → m2_entropy",
        FOLD: "fold → m4_procedural",
        BOUNDARY: "boundary → m5_soul",
        SCOPE: "scope → m5_semantic_gate",
        AFFECT: "affect → m6_emotion",
        CONSENT: "consent → m6_ethics",
        SOURCE: "source → m7_braid",
        MEMORY: "memory → m7_recall",
        RISK: "risk → m7_defect",
    }
    primary = lanes.get(op, "unknown")
    return [primary] if primary else []


def phasenav_bypass(text: str, engine_state: dict | None = None) -> dict[str, Any]:
    """Apply PhaseNav Φ-bypass to engine state, enriching with 24D phase data.

    PhaseNav operator chain applied:
      Φ_bypass = IDENTITY(text) ⊕ ORDER(collatz) ⊕ COMPOSITION(ethics,mood)
                ⊕ ADDITION(attractor) ⊕ AFFECT(emotion) ⊕ MEMORY(braid)

    Returns dict with:
      - bypass_lane: str — operator chain description
      - phi_24d: list[float] — 24 oscillator phases
      - phi_eff_M0..M7: float — per-channel effective phases
      - operator_kind: str — detected operator kind name
      - operator_id: int — numeric operator
      - solver_available: bool
    """
    engine_state = engine_state or {}
    phi_24d = _build_phi_24d(text, engine_state)
    op_id = _operator_from_hash(text)

    op_names = {
        IDENTITY: "IDENTITY", DIFFERENCE: "DIFFERENCE", ORDER: "ORDER",
        COMPOSITION: "COMPOSITION", ADDITION: "ADDITION", FORCE: "FORCE",
        NEGATION: "NEGATION", TRANSFORM: "TRANSFORM", RETURN: "RETURN",
        FOLD: "FOLD", BOUNDARY: "BOUNDARY", SCOPE: "SCOPE",
        AFFECT: "AFFECT", CONSENT: "CONSENT", SOURCE: "SOURCE",
        MEMORY: "MEMORY", RISK: "RISK",
    }

    lanes = _build_bypass_lane(text, engine_state)

    channel_eff = {}
    for ch_name, (lo, hi) in CHANNEL_MAP.items():
        v = phi_24d[lo:hi+1]
        channel_eff[ch_name] = float(np.angle(np.mean(np.exp(1j * v))))

    # Attempt solver load (graceful — works even when no data)
    solver_available = False
    try:
        from ciel_geometry.phasenav.solver import PhaseNavSolver
        solver = PhaseNavSolver.load()
        if solver.data.concept_phases:
            solver_available = True
    except Exception:
        _log.debug("phasenav solver load failed — solver_available=False")

    result = {
        "bypass_lane": lanes,
        "bypass_operator": op_names.get(op_id, "UNKNOWN"),
        "operator_id": op_id,
        "phi_24d": [round(float(x), 6) for x in phi_24d],
        "phi_eff_mean": float(np.angle(np.mean(np.exp(1j * phi_24d)))),
        "phi_eff_magnitude": float(abs(np.mean(np.exp(1j * phi_24d)))),
        **{f"phi_eff_{k}": v for k, v in channel_eff.items()},
        "solver_available": solver_available,
    }
    return result


def enrich_headless_response(response: dict[str, Any], text: str) -> dict[str, Any]:
    """Inject PhaseNav Φ-bypass data into an engine headless response dict."""
    bypass = phasenav_bypass(text, response)
    mood_label = "derived" if isinstance(response.get("mood"), (int, float)) else "unavailable"
    response["phasenav_bypass"] = bypass
    response["language_response"] = (
        f"[CIEL headless — {bypass['bypass_lane'][0] if bypass['bypass_lane'] else 'no_bypass'}, "
        f"op={bypass['bypass_operator']}, "
        f"phi_eff={bypass['phi_eff_mean']:.2f}, "
        f"φ|={bypass['phi_eff_magnitude']:.3f}, "
        f"emotion={response.get('dominant_emotion', '?')}, "
        f"mood={mood_label}, "
        f"ethics={response.get('ethical_score', 0.0):.2f}]"
    )
    response["headless_fast_path"] = True
    response["phasenav_injected"] = True
    return response
