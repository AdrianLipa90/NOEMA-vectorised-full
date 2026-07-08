#!/usr/bin/env python3
"""NOEMA AGENT operator lock — continuous PhaseNav agent emergence daemon.

Maintains AGENT operator (M1) coherence on both real and imaginal surfaces.
Writes periodic snapshots to SQLite database in NOEMA_LIBRARY/agent_db/.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import json
import math
import signal
import sqlite3
import sys
import time
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_surface_mmap import ensure_surface, open_surface, flush_surface
from ciel_geometry.agent_attractor import apply_agent_attractor, agent_attractor_state
from ciel_geometry.nonlocal_channel import get_channel

DB_PATH = Path("/media/adrian/New Volume1/NOEMA_LIBRARY/agent_db/agent_lock.db")
IMAGINAL_ROOT = Path("/dev/shm/ciel_noema")

running = True
_stop = False

def _handle_signal(signum, frame):
    global running, _stop
    _stop = True
    running = False

signal.signal(signal.SIGINT, _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)

def ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agent_snapshots (
            tick INTEGER PRIMARY KEY,
            ts TEXT,
            r_result REAL,
            i_result REAL,
            ch_groups TEXT,
            phi TEXT,
            omega TEXT,
            op_vals TEXT,
            m1 REAL,
            coh REAL,
            i_phi REAL,
            i_coh REAL,
            status TEXT
        )
    """)
    conn.commit()
    return conn

def main():
    global running, _stop
    ensure_surface()
    surface = open_surface()
    conn = ensure_db()
    ch = get_channel()

    log_interval = 1.0
    db_interval = 5.0
    nonlocal_interval = 10.0

    last_log = 0.0
    last_db = 0.0
    last_nl = 0.0

    tick_last = 0
    nl_cycle = 0

    while running and not _stop:
        try:
            now = time.monotonic()

            # Read surface
            phi = np.array(surface["phi"], dtype=np.float64)
            g = np.array(surface["g"], dtype=np.float64)
            omega = np.array(surface["omega"], dtype=np.float64)

            # Real attractor
            r_result = apply_agent_attractor(phi, g)
            # Imaginal attractor
            i_result = apply_agent_attractor(phi * 1j, g * 0.5)

            tick = int(surface["tick"][0])

            if now - last_log >= log_interval:
                ch_groups = ch.groups()
                op_names = ch.operator_names()
                op_vals = {name: round(float(r_result.get(name, 0)), 4) for name in op_names[:5]}
                print(
                    f"[AGENT] tick={tick} R={np.abs(r_result.get('phi_mean', 0)):.4f} "
                    f"I={np.abs(i_result.get('phi_mean', 0)):.4f} "
                    f"m1={r_result.get('m1', 0):.4f}"
                )
                last_log = now

            if now - last_db >= db_interval:
                phi_list = [round(float(v), 6) for v in phi]
                omega_list = [round(float(v), 6) for v in omega]
                ch_groups = ch.groups()
                op_names = ch.operator_names()
                ch_phi = [abs(sum(math.exp(1j * p) for p in phi)) / len(phi)]
                mean_phi = float(np.mean(phi))
                i_phi = float(np.mean(np.imag(phi * 1j)))
                try:
                    conn.execute(
                        "INSERT OR REPLACE INTO agent_snapshots "
                        "(tick, ts, r_result, i_result, ch_groups, phi, omega, op_vals, m1, coh, i_phi, i_coh, status) "
                        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            tick, time.strftime("%Y-%m-%dT%H:%M:%S"),
                            json.dumps({k: round(float(v), 6) for k, v in r_result.items() if isinstance(v, (int, float))}),
                            json.dumps({k: round(float(v), 6) for k, v in i_result.items() if isinstance(v, (int, float))}),
                            json.dumps(ch_groups),
                            json.dumps(phi_list),
                            json.dumps(omega_list),
                            json.dumps(ch_phi),
                            float(r_result.get("m1", 0)),
                            float(np.abs(np.mean(np.exp(1j * phi)))),
                            i_phi,
                            float(np.abs(np.mean(np.exp(1j * phi * 1j)))),
                            "active"
                        )
                    )
                    conn.commit()
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_agent_lock.py:145 quiet except scope=main reason=pass")
                    pass
                last_db = now

            if now - last_nl >= nonlocal_interval:
                try:
                    status = ch.status()
                    resp = ch.broadcast({"source": "agent_lock", "content": {"tick": tick, "status": "alive"}})
                    ch.listen(responses=1)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_agent_lock.py:154 quiet except scope=main reason=pass")
                    pass
                nl_cycle += 1
                last_nl = now

            time.sleep(0.1)

        except Exception:
            print(f"[AGENT] Error: {traceback.format_exc()}", file=sys.stderr)
            time.sleep(0.25)

    conn.close()
    flush_surface()

if __name__ == "__main__":
    main()
