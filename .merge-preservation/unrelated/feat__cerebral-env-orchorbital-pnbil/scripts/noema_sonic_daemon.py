#!/usr/bin/env python3
"""Sonic Screwdriver — probe the full NOEMA warp loop at a glance.

Reads all surface channels and shows:
  - Kuramoto state (phi, omega, g)
  - Semantic gravity (density, γ, mass, unruh)
  - WARP_DRIFT / UNRUH_DRIVE activity
  - Operator chain current state

Usage:
    python scripts/noema_sonic_daemon.py [--watch] [--interval SEC]
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
import logging
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_surface_mmap import (
    ensure_surface,
    N_OSCILLATORS,
    N_GRAVITY,
    N_FLAVORS,
)

logging.basicConfig(
    level=logging.INFO,
    format="[sonic] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

def read_surface_summary(surface) -> dict:
    phi = np.asarray(surface["phi"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)
    gravity = np.asarray(surface["gravity"], dtype=np.float64) if "gravity" in surface else np.zeros(N_GRAVITY)
    tick = int(np.asarray(surface["tick"], dtype=np.uint64)[0])

    z = np.exp(1j * phi)
    R = float(np.abs(z.mean()))
    psi = float(np.angle(z.mean()))
    euler = float(np.abs(np.sum(z)))

    phi_mean = float(np.mean(phi))
    phi_std = float(np.std(phi))
    omega_mean = float(np.mean(omega))
    g_mean = float(np.mean(np.abs(g)))

    flavor_labels = ["coherence", "soul", "ethics", "mood", "openness", "mode"]

    # Holonomy
    holonomy = np.asarray(surface["holonomy"], dtype=np.float64) if "holonomy" in surface else np.zeros(7)

    # Consolidator backend status
    consolidator_status = _check_consolidator_status()

    return {
        "tick": tick,
        "phi": {"mean": round(phi_mean, 4), "std": round(phi_std, 4)},
        "omega_mean": round(omega_mean, 2),
        "R": round(R, 4),
        "psi": round(psi, 4),
        "euler_residual": round(euler, 4),
        "coupling_mean": round(g_mean, 4),
        "flavor": {flavor_labels[i]: round(float(flavor[i]), 4) for i in range(N_FLAVORS)},
        "gravity": {
            "semantic_density": round(float(gravity[0]), 6),
            "tau_dilation": round(float(gravity[1]), 4),
            "mass_total": round(float(gravity[2]), 6),
            "unruh_power": round(float(gravity[3]), 8),
        },
        "warp_active": float(gravity[3]) > 1e-6,
        "tardis_active": float(gravity[1]) > 1.05,
        "holonomy": {
            "mean_connection": round(float(holonomy[0]), 4),
            "gauge_rank": int(holonomy[1]),
            "closure_score": round(float(holonomy[2]), 4),
            "surface_gamma": round(float(holonomy[3]), 4),
            "winding": int(holonomy[5]),
            "mean_curvature": round(float(holonomy[6]), 6),
        },
        "consolidator": consolidator_status,
    }

def _check_consolidator_status() -> dict:
    """Probe consolidator agent backend and daemon status."""
    import socket, json, urllib.request, urllib.error

    agent_alive = False
    try:
        with socket.create_connection(("127.0.0.1", 18520), timeout=0.5):
            agent_alive = True
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sonic_daemon.py:109 quiet except scope=_check_consolidator_status reason=pass")
        raise
        pass

    consolidator_pid = None
    daemon_alive = False
    try:
        from ciel_geometry.daemon_registry import Registry
        for d in Registry().scan():
            if "consolidat" in d.name.lower():
                consolidator_pid = d.pid
                daemon_alive = d.alive
                break
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sonic_daemon.py:121 quiet except scope=_check_consolidator_status reason=pass")
        raise
        pass

    db_path = Path("/media/adrian/New Volume/CIEL_memories/local_test/consolidator.db")
    total = done = pending = 0
    if db_path.exists():
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            total = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
            done = conn.execute("SELECT COUNT(*) FROM files WHERE status='done'").fetchone()[0]
            pending = conn.execute("SELECT COUNT(*) FROM files WHERE status='pending'").fetchone()[0]
            conn.close()
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sonic_daemon.py:134 quiet except scope=_check_consolidator_status reason=pass")
            raise
            pass

    return {
        "backend": "agent" if agent_alive else "offline",
        "daemon": daemon_alive,
        "daemon_pid": consolidator_pid,
        "files_total": total,
        "files_done": done,
        "files_pending": pending,
    }

def _scan_daemons() -> list[dict]:
    """Read daemon registry for all registered daemons."""
    try:
        from ciel_geometry.daemon_registry import Registry
        return [
            {"name": d.name, "pid": d.pid, "tick": d.tick,
             "uptime": round(d.uptime), "status": d.status,
             "cpu": round(d.cpu, 1), "alive": d.alive}
            for d in Registry().scan()
        ]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_sonic_daemon.py:156 quiet except scope=_scan_daemons reason=return []")
        raise
        return []

def sonic_report(surface) -> None:
    s = read_surface_summary(surface)

    # Header
    log.info(f"═══ NOEMA WARP LOOP ═══  tick={s['tick']}")

    # Kuramoto
    log.info(f"φ̄={s['phi']['mean']} σ={s['phi']['std']}  ω̄={s['omega_mean']}Hz  "
             f"R={s['R']}  |Σe^iφ|={s['euler_residual']}  |g|̄={s['coupling_mean']}")

    # Gravity
    g = s['gravity']
    log.info(f"semantic_density={g['semantic_density']}  γ={g['tau_dilation']}  "
             f"mass={g['mass_total']}  unruh={g['unruh_power']}")

    # Status
    warp = "⏎ WARP" if s['warp_active'] else "· latent"
    tardis = "🐢 TARDIS" if s['tardis_active'] else "· 1:1"
    log.info(f"{warp}  {tardis}")

    # Flavor
    f = s['flavor']
    tau_str = f"  τ̄={s.get('tau_mean', 0):.3f}" if 'tau_mean' in s else ""
    log.info(f"coherence={f['coherence']}  mood={f['mood']}  closure={1-f['openness']:.3f}  "
             f"ethics={f['ethics']}{tau_str}")

    # Holonomy
    h = s['holonomy']
    log.info(f"holonomy: ⟨A⟩={h['mean_connection']}  rank={h['gauge_rank']}  "
             f"closure={h['closure_score']}  γ_φ={h['surface_gamma']}  "
             f"winding={h['winding']}  κ̄={h['mean_curvature']}")

    # Consolidator
    c = s['consolidator']
    daemon_icon = "●" if c['daemon'] else "○"
    log.info(f"consolidator: {daemon_icon} backend={c['backend']}  "
             f"files={c['files_done']}/{c['files_total']}  pid={c['daemon_pid']}")

    # Registry daemon scan
    daemons = _scan_daemons()
    if daemons:
        parts = [f"{d['name'][:10]}:{'●' if d['alive'] else '○'}" for d in daemons]
        log.info(f"registry: {'  '.join(parts)}")

def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Sonic Screwdriver")
    parser.add_argument("--watch", action="store_true", help="Continuous probe")
    parser.add_argument("--interval", type=float, default=2.0, help="Probe interval (s)")
    args = parser.parse_args()

    surface = ensure_surface()

    if args.watch:
        log.info(f"Watching warp loop every {args.interval}s — Ctrl+C to stop")
        try:
            while True:
                sonic_report(surface)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            log.info("Sonic off")
    else:
        sonic_report(surface)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
