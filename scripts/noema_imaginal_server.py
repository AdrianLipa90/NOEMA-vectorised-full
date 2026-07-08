#!/usr/bin/env python3
"""NOEMA Imaginal Server — daemony jako operatory 24D na imaginal surface.

Używa resonance_bridge.dual_surface_step() jako silnika.
Każdy daemon NOEMY to osobny oscylator na imaginal surface z własną ω.
Real surface = Poincaré section (zamrożony odczyt).

Usage:
    python3 scripts/noema_imaginal_server.py [--interval SEC]
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import argparse
import json
import logging
import math
import signal
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.resonance_bridge import (
    ensure_dual_surfaces,
    dual_surface_step,
    resonance_snapshot,
    DEFAULT_IMAGINAL_SURFACE_ROOT,
    DEFAULT_SURFACE_ROOT,
)
from ciel_geometry.noema_registry import registry
from ciel_geometry.noema_surface_mmap import ensure_surface, open_surface
from ciel_geometry.phase_memory_adapter import bind_phase_memory, query_phase_memory

logging.basicConfig(
    level=logging.INFO,
    format="[imaginal] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

N_OSCILLATORS = 36

# Mapowanie daemonów na oscylatory 24D
DAEMON_CHANNEL_MAP: dict[str, int] = {
    "kuramoto":       0,   # M0 Perceptual / semantic
    "portal":         1,   # M0 / htri
    "orbital":        2,   # M0 / nonlocal
    "linux-sensor":   3,   # M1 Working / semantic
    "neutrino":       4,   # M1 / htri
    "resonance":      5,   # M1 / nonlocal
    "cielingo-sync":  6,   # M2 Episodic / semantic
    "nonlocal-proxy": 7,   # M2 / htri
    "phasenav-hot":   8,   # M2 / nonlocal
    "analog-blend":   9,   # M3 Semantic / semantic
    "consolidator":   10,  # M3 / htri
    "agent-backend":  11,  # M3 / nonlocal
    "archiver":       12,  # M4 Procedural / semantic
}

DAEMON_OMEGA: dict[str, float] = {
    "kuramoto": 0.15, "portal": 0.05, "orbital": 0.08,
    "linux-sensor": 0.20, "neutrino": 0.12, "resonance": 0.10,
    "cielingo-sync": 0.07, "nonlocal-proxy": 0.09, "phasenav-hot": 0.18,
    "analog-blend": 0.06, "consolidator": 0.04, "agent-backend": 0.11,
    "archiver": 0.03,
}


def _set_daemon_omegas():
    """Ustawia ω dla daemonów na imaginal surface."""
    try:
        imaginal = open_surface(root=DEFAULT_IMAGINAL_SURFACE_ROOT)
        omega_arr = np.asarray(imaginal["omega"], dtype=np.float64)
        for dname, idx in DAEMON_CHANNEL_MAP.items():
            if idx < N_OSCILLATORS:
                omega_arr[idx] = DAEMON_OMEGA.get(dname, 0.1)
        imaginal["omega"].flush()
    except Exception as e:
        log.warning("can't set ω: %s", e)


def _read_daemon_phases() -> dict[str, dict]:
    """Odczytuje fazy daemonów z imaginal surface."""
    try:
        imaginal = open_surface(root=DEFAULT_IMAGINAL_SURFACE_ROOT)
        phi_arr = np.asarray(imaginal["phi"], dtype=np.float64)
        omega_arr = np.asarray(imaginal["omega"], dtype=np.float64)
        daemons = {}
        for dname, idx in DAEMON_CHANNEL_MAP.items():
            if idx < len(phi_arr):
                daemons[dname] = {
                    "osc_idx": idx,
                    "phi": round(float(phi_arr[idx]), 4),
                    "omega": float(omega_arr[idx]) if idx < len(omega_arr) else 0.1,
                    "alive": True,
                }
        return daemons
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_imaginal_server.py:108 quiet except scope=_read_daemon_phases reason=return {\"error\": str(e)}")
        return {"error": str(e)}


def _get_coherence(surface_root) -> float:
    """Koherencja globalna z danej powierzchni."""
    try:
        s = open_surface(root=surface_root)
        phi = np.asarray(s["phi"], dtype=np.float64)
        r = sum(math.cos(p) for p in phi)
        im = sum(math.sin(p) for p in phi)
        return round(math.sqrt(r*r + im*im) / N_OSCILLATORS, 4)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_imaginal_server.py:120 quiet except scope=_get_coherence reason=return 0.0")
        return 0.0


def _load_orbital_state() -> dict:
    """Wczytuje orbital state z /tmp/noema_orbital_state.json."""
    try:
        p = Path("/tmp/noema_orbital_state.json")
        if p.exists():
            with open(p) as f:
                return json.load(f)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_imaginal_server.py:131 quiet except scope=_load_orbital_state reason=pass")
        pass
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Imaginal Server — daemony jako operatory")
    parser.add_argument("--interval", type=float, default=1.0, help="Cycle interval (s)")
    parser.add_argument("--save", type=str, default="/tmp/noema_imaginal_state.json",
                        help="Path do zapisu stanu (JSON)")
    args = parser.parse_args()

    log.info("Starting imaginal server — %d daemonów jako operatorów 24D",
             len(DAEMON_CHANNEL_MAP))

    # Inicjalizacja dual surfaces
    try:
        ensure_dual_surfaces()
        log.info("dual surfaces OK")
    except Exception as e:
        log.error("ensure_dual_surfaces: %s", e)
        return 1

    # Registry
    reg_token = registry.register("imaginal")
    log.info("registered in daemon registry")

    # CIEL state dla symulacji
    ciel_state = {
        "closure_penalty": 0.15,
        "coherence_index": 0.85,
        "mood": 0.3,
        "dominant_emotion": "warmth",
        "ethical_score": 0.8,
        "soul_invariant": 0.75,
        "operating_mode": "standard",
    }

    # Signal handling
    _running = True
    def _stop(signum, frame):
        nonlocal _running
        log.info("SIGTERM, shutting down")
        _running = False
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    tick = 0
    last_save = time.monotonic()

    try:
        while _running:
            cycle_start = time.monotonic()

            # 1. Ustaw ω daemonów na imaginal surface
            _set_daemon_omegas()

            # 2. Główny tick: dual_surface_step (imaginal evolution + real projection + resonance)
            try:
                result = dual_surface_step(
                    ciel_state, f"imaginal_tick_{tick}",
                    dt=0.05,
                )
                tick += 1
            except Exception as e:
                log.error("dual_surface_step: %s", e)
                time.sleep(args.interval)
                continue

            # 3. Heartbeat
            registry.heartbeat(reg_token)

            # 4. Feed stan do PhaseNav memory (bind_phase_memory)
            #    Każdy tick = nowy wpis w phase memory ring buffer
            try:
                daemon_text = json.dumps({
                    "source": "imaginal",
                    "tick": tick,
                    "daemons": daemons,
                    "coherence": coherence,
                })
                slot = bind_phase_memory(daemon_text)
                if tick % 10 == 0:
                    log.debug("phase memory slot=%d", slot)
            except Exception as e:
                log.warning("bind_phase_memory: %s", e)

            # 5. Odczytaj fazy daemonów
            daemons = _read_daemon_phases()
            coherence = _get_coherence(DEFAULT_SURFACE_ROOT)

            # 5. Okresowy zapis stanu
            now = time.monotonic()
            if now - last_save >= 5.0:
                last_save = now
                try:
                    snap = resonance_snapshot()
                    orb = _load_orbital_state()
                    state = {
                        "status": "ok",
                        "type": "imaginal",
                        "tick": tick,
                        "uptime_s": round(now - cycle_start + 1, 1),
                        "coherence": coherence,
                        "daemon_count": len(DAEMON_CHANNEL_MAP),
                        "daemons": daemons,
                        "resonance": {
                            "phase_lock": snap.get("phase_lock", 0),
                            "flavor_lock": snap.get("flavor_lock", 0),
                            "resonance_score": snap.get("resonance_score", 0),
                        },
                        "orbital": {
                            "systems": orb.get("systems", 0),
                            "orbits": orb.get("orbits", 0),
                            "coherence": orb.get("coherence", 0),
                        } if orb else None,
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    }
                    with open(args.save, 'w', encoding='utf-8') as f:
                        json.dump(state, f, indent=2, ensure_ascii=False)
                    log.info("tick=%d coh=%.4f daemons=%d saved=%s",
                             tick, coherence, len(daemons), args.save)
                except Exception as e:
                    log.warning("save error: %s", e)

            # Interval
            elapsed = time.monotonic() - cycle_start
            sleep = max(0.01, args.interval - elapsed)
            time.sleep(sleep)

    except Exception as e:
        log.error("Fatal: %s", e)
        return 1
    finally:
        registry.unregister(reg_token)
        log.info("imaginal server stopped (tick=%d)", tick)

    return 0


if __name__ == "__main__":
    sys.exit(main())
