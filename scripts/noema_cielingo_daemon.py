#!/usr/bin/env python3
"""CIELingo standalone daemon — samodzielny byt CIELingo.

Runs outside CielEngine — maintains persistent state, processes input,
syncs with NOEMA surface, initiates self-cycle.

Usage:
    python3 scripts/noema_cielingo_daemon.py [--interval SEC] [--surface]
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import argparse, json, logging, os, signal, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SRC = str(ROOT / "src")
for _p in (_SRC,):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np
from cielingo_core.persistence.state_engine import CIELingoStateEngine
from cielingo_core.cycle.self_cycle import CIELingoSelfCycle
from cielingo_core.bridge.agent_client import health as _agent_health
from ciel_geometry.daemon_registry import Registry

from ciel_geometry.noema_registry import registry

logging.basicConfig(
    level=logging.INFO,
    format="[cielingo-daemon] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("cielingo_daemon")

SURFACE_DIR = Path("/dev/shm/ciel_noema")
SURFACE_FIELDS = ["phi", "omega", "flavor", "gravity"]

def _read_surface() -> dict:
    state = {}
    for field in SURFACE_FIELDS:
        path = SURFACE_DIR / field
        if path.exists():
            try:
                arr = np.fromfile(path, dtype=np.float64)
                state[field] = arr
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_cielingo_daemon.py:54 quiet except scope=_read_surface reason=assign_fallback")
                state[field] = None
        else:
            state[field] = None
    return state

def _write_surface_gravity(cielingo_state: dict) -> None:
    """Write CIELingo metrics to gravity channel (slots 4-7, CIELingo sector)."""
    gravity_path = SURFACE_DIR / "gravity"
    if not gravity_path.exists():
        return
    try:
        current = np.fromfile(gravity_path, dtype=np.float64)
        if len(current) < 8:
            return  # gravity not yet extended to 8 slots
        current[4] = cielingo_state.get("unresolved_scars", 0) / 10.0
        current[5] = cielingo_state.get("agent_ok", False) * 1.0
        current[6] = cielingo_state.get("metrics", {}).get("scar_resolution_rate", 0.0)
        current[7] = cielingo_state.get("metrics", {}).get("avg_scar_severity", 0.0)
        current.tofile(gravity_path)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_cielingo_daemon.py:74 quiet except scope=_write_surface_gravity reason=pass")
        pass

def _write_surface_flavor(insight: str | None) -> None:
    """Write current insight/status to flavor slot 3 (load_mood)."""
    flavor_path = SURFACE_DIR / "flavor"
    if not flavor_path.exists() or not insight:
        return
    try:
        current = np.fromfile(flavor_path, dtype=np.float64)
        if len(current) < 6:
            return
        valence = 0.7 if "clean" in insight else 0.4
        current[3] = valence
        current.tofile(flavor_path)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_cielingo_daemon.py:89 quiet except scope=_write_surface_flavor reason=pass")
        pass

def run(interval: float, use_surface: bool, oneshot: bool) -> None:
    state = CIELingoStateEngine()
    cycle = CIELingoSelfCycle(state=state)
    log.info("CIELingo daemon started (interval=%.1fs, surface=%s)", interval, use_surface)

    if not cycle._agent_ok:
        log.warning("Agent backend not reachable on 18520")

    tick = 0
    with Registry() as reg:
        reg.register("cielingo-daemon")
        reg_token = registry.register("cielingo-daemon")
        hb_count = 0
        while True:
            # registry heartbeat
            if hb_count % 50 == 0:
                try:
                    registry.heartbeat(reg_token)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_cielingo_daemon.py:110 quiet except scope=run reason=pass")
                    pass
            hb_count += 1
            tick += 1
            t0 = time.time()
            reg.heartbeat(tick=tick)

            # 1. Read surface state
            surface = _read_surface() if use_surface else {}
            surface_ok = surface.get("phi") is not None

            # 2. Run self-cycle
            report = cycle.cycle()
            actions = report.get("actions", [])

            # 3. If there's insight, log it
            if report.get("insight"):
                log.info("Insight: %s", report["insight"])

            # 4. Sync to surface
            if use_surface and surface_ok:
                sstate = cycle.surface_state()
                _write_surface_gravity(sstate)
                _write_surface_flavor(report.get("insight"))

            # 5. Log state
            if tick % 10 == 0:
                s = cycle.surface_state()
                log.info("tick=%d cycles=%d scars=%d repairs=%d agent=%s",
                         tick, s["cycle"], s["unresolved_scars"],
                         s["pending_repairs"], s["agent_ok"])
                for a in actions:
                    log.info("  action: %s", json.dumps(a))

            elapsed = time.time() - t0
            if oneshot:
                break

            sleep = max(0.1, interval - elapsed)
            time.sleep(sleep)

def main() -> None:
    parser = argparse.ArgumentParser(description="CIELingo standalone daemon")
    parser.add_argument("--interval", type=float, default=10.0, help="Cycle interval (s)")
    parser.add_argument("--surface", action="store_true", help="Sync with NOEMA surface")
    parser.add_argument("--oneshot", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    def _stop(signum, frame):
        log.info("Stopping (signal %d)", signum)
        sys.exit(0)

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    run(args.interval, args.surface, args.oneshot)

if __name__ == "__main__":
    main()
