#!/usr/bin/env python3
"""Direct CIEL coupling for opencode — sprzężenie semantyczno-tożsamościowe.

No file I/O for state. All communication through CIEL's Python API directly.

Usage:
    from ciel_coupling import process_user_input, get_ciel_state

    # On every user message:
    state = process_user_input(user_text)
    # Returns dict with: emotion, ethics, soul, phase, operating_mode, ...

    # To check current state (after processing):
    info = get_ciel_state()
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SRC = str(_PROJECT_ROOT / "src")
_CIEL_OMEGA_ROOT = str(_PROJECT_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM")
_CIEL_OMEGA = str(_PROJECT_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega")
_INTEGRATION = str(_PROJECT_ROOT / "integration")
_ROOT_STR = str(_PROJECT_ROOT)
# _ROOT_STR musi być wstawiony jako OSTATNI (trafia na pozycję 0),
# żeby NOEMA/integration/ nie był zasłonięty przez ciel_omega/integration/
for _p in (_INTEGRATION, _CIEL_OMEGA, _CIEL_OMEGA_ROOT, _SRC, _ROOT_STR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ciel_geometry import (
    bind_phase_memory,
    ensure_surface,
    read_surface_state,
    update_surface_from_ciel_state,
    write_concepts_to_surface,
)
from ciel_sot_agent.cielingo_bridge import build_lingo_frame
from ciel_sot_agent.state_db import get_or_create_identity_seed

# ── Lazy engine singleton ─────────────────────────────────────────────────────

_ENGINE: Any = None
_ENGINE_ROOT: Path | None = None


def _get_engine(root: Path | None = None) -> Any:
    """Return cached CielEngine, initialising once per session."""
    global _ENGINE, _ENGINE_ROOT
    if _ENGINE is not None and root is None:
        return _ENGINE
    if root is None:
        root = _PROJECT_ROOT
    if _ENGINE is not None and root == _ENGINE_ROOT:
        return _ENGINE
    from ciel_omega.ciel.engine import CielEngine
    _ENGINE = CielEngine()
    _ENGINE_ROOT = root
    # Share engine with ciel_pipeline to avoid dual-singleton (2×35s init)
    try:
        import ciel_sot_agent.ciel_pipeline as _cp
        _cp._ENGINE_CACHE[str(root.resolve())] = _ENGINE
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_coupling.py:66 quiet except scope=_get_engine reason=pass")
        raise
        pass
    return _ENGINE


# ── Operating mode ────────────────────────────────────────────────────────────

def _closure_to_mode(cp: float) -> str:
    if cp < 0.15:
        return "deep"
    if cp <= 0.35:
        return "standard"
    return "safe"


# ── Public API ────────────────────────────────────────────────────────────────

_LAST_STATE: dict[str, Any] = {}


def _load_ciel_doorway_module(root: Path) -> Any | None:
    script_path = root / "head" / "Ciel Memories" / "ciel_doorway_push.py"
    if not script_path.exists():
        return None
    spec = importlib.util.spec_from_file_location("ciel_doorway_push_runtime", script_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def append_ciel_memory_update(
    state: dict[str, Any],
    text: str,
    *,
    root: Path | None = None,
    schema: str = "CIEL_PHASE_MEMORY_UPDATE_V0_1",
    extra_payload: dict[str, Any] | None = None,
) -> str | None:
    root = root or _PROJECT_ROOT
    doorway = _load_ciel_doorway_module(root)
    if doorway is None:
        return None
    door = doorway.open_door(root, doorway.TRIGGER, True)
    if not door.get("opened"):
        return None
    payload = {
        "schema": schema,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "owner": "Adrian",
        "memory_agent": "Ciel",
        "raw_text_sha256": __import__("hashlib").sha256(text.encode("utf-8")).hexdigest(),
        "state": {
            "dominant_emotion": state.get("dominant_emotion"),
            "operating_mode": state.get("operating_mode"),
            "closure_penalty": state.get("closure_penalty"),
            "coherence_index": state.get("coherence_index"),
            "phase_memory_slot": state.get("phase_memory_slot"),
            "noema_tick": state.get("noema_tick"),
        },
        "summary": state.get("lingo_summary", "")[:280],
    }
    if extra_payload:
        payload.update(extra_payload)
    written = doorway.append_update(root, door, payload)
    return str(written)


def _build_htri_phase_bus(
    text: str,
    concepts: list[str],
    *,
    encoder_result: Any = None,
) -> dict[str, Any]:
    """Build HTRI phase bus snapshot — oscillator binding, lanes, brain topology.

    If encoder_result is provided, injects semantic encoder phase/brain_region
    into the bus report to create a real connection between the two layers.
    """
    try:
        from cielingo.htri_phase_bus import phase_bus_report
        from cielingo.htri_brain_map import brain_phase_topology, oscillator_for_card
        rpt = phase_bus_report(query=" ".join(concepts) if concepts else text, limit=24)
        topology = brain_phase_topology()
        out: dict[str, Any] = {
            "card_count": rpt.get("card_count", 0),
            "htri_oscillators": rpt.get("htri_oscillators", 24),
            "free_oscillators": rpt.get("spare_oscillators", 24),
            "mean_phase_alignment": rpt.get("mean_phase_alignment"),
            "mean_phase_tension": rpt.get("mean_phase_tension"),
            "mean_j_bus_total": rpt.get("mean_j_bus_total"),
            "lane_counts": rpt.get("lane_counts", {}),
            "bus_actions": rpt.get("bus_actions", {}),
            "brain_topology": topology,
        }
        # Inject semantic encoder coupling into HTRI bus
        if encoder_result is not None:
            out["encoder_phase_rad"] = encoder_result.phase
            out["encoder_oscillator_id"] = encoder_result.brain_oscillator_id
            out["encoder_brain_region"] = encoder_result.brain_region
            out["encoder_sector"] = encoder_result.dominant_sector
            out["encoder_coherence"] = encoder_result.coherence
            # phase alignment between encoder and its HTRI oscillator
            osc_id = encoder_result.brain_oscillator_id
            bus_alignment = rpt.get("mean_phase_alignment") or 0.5
            out["encoder_bus_alignment"] = round(bus_alignment, 6)
            out["encoder_coupled"] = True
        return out
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_coupling.py:175 quiet except scope=_build_htri_phase_bus reason=return {}")
        raise
        return {}


def process_user_input(text: str, *, fast: bool = False) -> dict[str, Any]:
    """Run user input through CIELingo + CielEngine, return enriched state.

    Args:
        text: Raw user input (in any language supported by CIELingo)
        fast: If True, skip CielEngine step (response ~1s vs 30-60s)

    Returns:
        dict with keys:
            dominant_emotion, ethical_score, soul_invariant, closure_penalty,
            operating_mode, phi_berry_mean, cycle_index, lingo_concept_count,
            lingo_summary, lingo_unresolved_count, identity_seed, mood,
            system_health, coherence_index
    """
    global _LAST_STATE

    identity = get_or_create_identity_seed()

    lingo = build_lingo_frame(text)
    summary = lingo.get("summary", "")
    dominant_emotion = lingo.get("dominant_emotion", "")
    concepts = lingo.get("concept_tokens", [])
    unresolved = lingo.get("unresolved", [])

    raw: dict[str, Any] = {}
    if not fast:
        try:
            engine = _get_engine()
            raw = engine.step(summary, context=f"opencode|{text[:80]}")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_coupling.py:208 quiet except scope=process_user_input reason=pass")
            raise
            pass

    # Run semantic encoder FIRST so encoder_phase feeds into orbital geometry
    _encoder_result = None
    try:
        from cielingo.semantic_encoder import encode as _sem_encode
        _encoder_result = _sem_encode(text)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_coupling.py:216 quiet except scope=process_user_input reason=pass")
        raise
        pass
    _encoder_phase = _encoder_result.phase if _encoder_result is not None else None

    # Real orbital metrics from the bridge (closure_penalty, phi_berry, mode)
    orbital_metrics: dict[str, float] = {}
    try:
        from ciel_sot_agent.orbital_bridge import build_orbital_bridge
        bridge = build_orbital_bridge(_PROJECT_ROOT, encoder_phase=_encoder_phase)
        hp = bridge.get("health_manifest", {})
        cp = bridge.get("ciel_pipeline", {})
        orbital_metrics = {
            "closure_penalty": float(hp.get("closure_penalty", 0.0)),
            "phi_berry_mean": float(cp.get("phi_berry_mean", 0.0)),
            "system_health": float(hp.get("system_health", 0.5)),
            "coherence_index": float(bridge.get("state_manifest", {}).get("coherence_index", 0.5)),
            "R_H": float(hp.get("R_H", 0.0)),
            "operating_mode": bridge.get("recommended_control", {}).get("mode", "standard"),
        }
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_coupling.py:235 quiet except scope=process_user_input reason=pass")
        raise
        pass

    #──── Fallback: gdy engine/orbital_bridge failed, czytaj live z surface ────
    _surface_live: dict[str, Any] = {}
    if not orbital_metrics:
        try:
            from ciel_geometry.noema_surface_mmap import ensure_surface as _sf_ensure, read_surface_state as _sf_read
            _sf = _sf_ensure(zero_fill=False)
            if _sf is not None:
                _surface_live = _sf_read(_sf)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_coupling.py:254 quiet except scope=process_user_input reason=surface_live_fallback_failed")
            raise

    # Każda wartość: 1) engine/live pipeline, 2) surface live fallback, 3) identity baseline
    ethical_score = float(
        raw.get("ethical_score") or
        _surface_live.get("ethical_score") or
        identity.get("ethical_baseline", 0.5)
    )
    soul_invariant = float(
        raw.get("soul_invariant") or
        _surface_live.get("soul_invariant") or
        identity.get("soul_baseline", 0.5)
    )
    mood = float(raw.get("mood") or _surface_live.get("mood") or 0.0)
    closure_penalty = orbital_metrics.get("closure_penalty") or _surface_live.get("closure_penalty", 0.0)
    phi_berry_mean = orbital_metrics.get("phi_berry_mean") or raw.get("nonlocal_runtime", {}).get("phi_berry_mean") or _surface_live.get("phi_berry_mean", 0.0)
    system_health = orbital_metrics.get("system_health") or _surface_live.get("system_health", 0.5)
    coherence_index = orbital_metrics.get("coherence_index") or _surface_live.get("coherence_index", 0.5)
    cycle_index = int(raw.get("cycle_index", _surface_live.get("noema_tick", 0))) + 1

    _LAST_STATE = {
        "dominant_emotion": dominant_emotion or raw.get("dominant_emotion", "curiosity"),
        "ethical_score": ethical_score,
        "soul_invariant": soul_invariant,
        "closure_penalty": closure_penalty,
        "operating_mode": orbital_metrics.get("operating_mode", _closure_to_mode(closure_penalty)),
        "phi_berry_mean": phi_berry_mean,
        "cycle_index": cycle_index,
        "lingo_summary": summary,
        "lingo_concept_count": len(concepts),
        "lingo_unresolved_count": len(unresolved),
        "mood": mood,
        "system_health": system_health,
        "coherence_index": coherence_index,
        "username": identity.get("username", "CielPC"),
        "identity_seed": identity.get("seed", ""),
        "collatz_seed": identity.get("collatz_seed", 0),
        "soul_baseline": identity.get("soul_baseline", 0.5),
        "ethical_baseline": identity.get("ethical_baseline", 0.5),
        "source": "ciel_coupling",
        "phrase_sense": lingo.get("phrase_sense", {}),
    }

    # CIELingo Semantic Encoder — reuse result from pre-bridge call
    if _encoder_result is not None:
        _LAST_STATE["semantic_encoder"] = {
            "phase": round(_encoder_result.phase, 6),
            "coherence": round(_encoder_result.coherence, 6),
            "dominant_sector": _encoder_result.dominant_sector,
            "brain_region": _encoder_result.brain_region,
            "brain_oscillator_id": _encoder_result.brain_oscillator_id,
            "token_count": _encoder_result.token_count,
            "tokens": [
                {"surface": t["surface"], "card_type": t["card_type"],
                 "phase": round(t["phase"], 4)}
                for t in _encoder_result.per_token
            ],
        }
    else:
        _LAST_STATE["semantic_encoder"] = {"error": "encoder call failed"}

    # Rebuild HTRI bus with encoder coupling
    _LAST_STATE["htri_phase_bus"] = _build_htri_phase_bus(text, concepts, encoder_result=_encoder_result)

    # Write CIELingo concept tokens to the surface (seeds oscillator phases)
    surface = ensure_surface()
    phase_proj = lingo.get("phase_projection", {}) or {}
    target_phase = float(phase_proj.get("target_phase", 0.0))
    phase_conf = float(phase_proj.get("phase_confidence", 0.0))
    write_concepts_to_surface(
        surface,
        concepts,
        target_phase=target_phase if phase_conf > 0.1 else None,
        phase_confidence=phase_conf,
        update_coupling=True,
    )

    # Keep NOEMA's shared surface in sync with the current CIEL state.
    surface = update_surface_from_ciel_state(_LAST_STATE)
    memory_payload = " | ".join(
        part for part in [
            "Adrian",
            summary,
            dominant_emotion or raw.get("dominant_emotion", "curiosity"),
            str(concepts[:8]),
        ]
        if part
    )
    slot = bind_phase_memory(memory_payload)
    _LAST_STATE["phase_memory_slot"] = slot
    _LAST_STATE["noema_tick"] = int(surface["tick"][0])
    _LAST_STATE["ciel_memory_update_path"] = append_ciel_memory_update(_LAST_STATE, text)
    return dict(_LAST_STATE)


def get_ciel_state() -> dict[str, Any]:
    """Return the last processed CIEL state, or empty defaults if none yet."""
    if _LAST_STATE:
        return dict(_LAST_STATE)
    identity = get_or_create_identity_seed()
    return {
        "dominant_emotion": "curiosity",
        "ethical_score": identity.get("ethical_baseline", 0.5),
        "soul_invariant": identity.get("soul_baseline", 0.5),
        "closure_penalty": 0.15,
        "operating_mode": "standard",
        "phi_berry_mean": 0.0,
        "cycle_index": 0,
        "lingo_summary": "",
        "lingo_concept_count": 0,
        "lingo_unresolved_count": 0,
        "mood": 0.0,
        "system_health": 0.5,
        "coherence_index": 0.5,
        "username": identity.get("username", "CielPC"),
        "identity_seed": identity.get("seed", ""),
        "collatz_seed": identity.get("collatz_seed", 0),
        "soul_baseline": identity.get("soul_baseline", 0.5),
        "ethical_baseline": identity.get("ethical_baseline", 0.5),
        "phase_memory_slot": None,
        "noema_tick": 0,
        "ciel_memory_update_path": None,
        "source": "ciel_coupling_default",
        "phrase_sense": {},
        "htri_phase_bus": {},
        "semantic_encoder": None,
    }


def __main__() -> None:
    """CLI entry: process input from argv or stdin, print JSON output."""
    import json
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read().strip()
    if not text:
        ctx = get_ciel_state()
    else:
        ctx = process_user_input(text)
    json.dump(ctx, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    __main__()
