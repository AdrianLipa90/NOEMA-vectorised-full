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
from ciel_geometry.resonance_bridge import DEFAULT_IMAGINAL_SURFACE_ROOT
from ciel_geometry.agent_attractor import apply_agent_attractor, agent_attractor_state
from ciel_geometry.nonlocal_channel import get_channel


def _channel_groups_and_ops(ch) -> tuple[dict, list]:
    """NonlocalChannel has no groups()/operator_names() API — it's a φ-RAG
    channel, not an operator-algebra object. Degrade to empty metadata
    instead of crashing every log/db cycle (was: AttributeError every ~1s,
    causing systemd to restart this daemon repeatedly)."""
    groups = ch.groups() if hasattr(ch, "groups") else {}
    op_names = ch.operator_names() if hasattr(ch, "operator_names") else []
    return groups, op_names

DB_PATH = Path("/media/adrian/New Volume/NOEMA_LIBRARY/agent_db/agent_lock.db")
# Was Path("/dev/shm/ciel_noema") — the REAL surface root, not the
# imaginal one. IMAGINAL_ROOT was defined but never actually used to open
# a second surface; instead the caller worked around the missing wiring
# with `phi * 1j`, treating phase values as imaginary-axis coefficients.
# apply_agent_attractor() is real-only (uses % on phi throughout) and
# crashes on complex input (TypeError: ufunc 'remainder' not supported).
# ciel_noema_resonance_bridge.py's real/imaginal dual-surface sync shows
# the actual pattern this repo uses: a second, fully real mmap surface
# tree at ciel_noema_imaginal/, not a complex-number encoding of the real
# one. Fixed to point at the real imaginal surface and open it properly.
IMAGINAL_ROOT = DEFAULT_IMAGINAL_SURFACE_ROOT

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
    ensure_surface(root=IMAGINAL_ROOT)
    imaginal_surface = open_surface(root=IMAGINAL_ROOT)
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
            # Imaginal attractor — operates on the real imaginal surface's
            # own phi/g arrays (a genuine second real surface), not a
            # complex-number encoding of the real one.
            i_phi = np.array(imaginal_surface["phi"], dtype=np.float64)
            i_g = np.array(imaginal_surface["g"], dtype=np.float64)
            i_result = apply_agent_attractor(i_phi, i_g * 0.5)
            imaginal_surface["phi"][:] = i_phi
            imaginal_surface["g"][:] = i_g
            flush_surface(imaginal_surface)

            tick = int(surface["tick"][0])

            if now - last_log >= log_interval:
                ch_groups, op_names = _channel_groups_and_ops(ch)
                op_vals = {name: round(float(r_result.get(name, 0)), 4) for name in op_names[:5]}
                print(
                    # apply_agent_attractor() returns 'coherence'/'m2_coherence',
                    # never 'phi_mean'/'m1' — those .get() calls always fell
                    # back to their default (0), so this line always printed
                    # R=0.0000 I=0.0000 m1=0.0000 regardless of real state.
                    f"[AGENT] tick={tick} R={r_result.get('coherence', 0):.4f} "
                    f"I={i_result.get('coherence', 0):.4f} "
                    f"m2={r_result.get('m2_coherence', 0):.4f}"
                )
                last_log = now

            if now - last_db >= db_interval:
                phi_list = [round(float(v), 6) for v in phi]
                omega_list = [round(float(v), 6) for v in omega]
                ch_groups, op_names = _channel_groups_and_ops(ch)
                # Was math.exp(1j*p) — math.exp doesn't accept complex
                # numbers (TypeError: must be real number, not complex).
                # np is already used for this exact exp(i*phi) pattern
                # elsewhere in this file; no new import needed.
                ch_phi = [abs(sum(np.exp(1j * p) for p in phi)) / len(phi)]
                mean_phi = float(np.mean(phi))
                # Was `float(np.mean(np.imag(phi * 1j)))` — algebraically
                # just np.mean(phi) again (imag(x*i) == x for real x), a
                # meaningless recomputation left over from the phi*1j hack.
                # Now a genuine mean phase of the real imaginal surface.
                i_phi_mean = float(np.mean(i_phi))
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
                            i_phi_mean,
                            # Was np.exp(1j*phi*1j) == exp(-phi), a real
                            # decay with no phase meaning. Now the real
                            # imaginal surface's own coherence, same
                            # formula as the real surface's above.
                            float(np.abs(np.mean(np.exp(1j * i_phi)))),
                            "active"
                        )
                    )
                    conn.commit()
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_agent_lock.py:145 quiet except scope=main reason=pass")
                    raise
                    pass
                last_db = now

            if now - last_nl >= nonlocal_interval:
                try:
                    # Was ch.status() — NonlocalChannel has no status() method
                    # (has .state property instead) and the result was never
                    # used below anyway; dead call removed rather than guessed at.
                    resp = ch.broadcast({"source": "agent_lock", "content": {"tick": tick, "status": "alive"}})
                    # Was ch.listen(responses=1) — listen() has no responses=
                    # kwarg (signature: channel, min_resonance, max_age) and,
                    # same as the ch.status() case above, the return value was
                    # never used — fixed 2026-07-10, this TypeError had been
                    # masked until now by the broadcast() hash(dict) crash
                    # above always firing first every cycle.
                    ch.listen()
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_agent_lock.py:154 quiet except scope=main reason=pass")
                    raise
                    pass
                nl_cycle += 1
                last_nl = now

            time.sleep(0.1)

        except Exception:
            print(f"[AGENT] Error: {traceback.format_exc()}", file=sys.stderr)
            time.sleep(0.25)

    conn.close()
    # Was flush_surface() with no argument — flush_surface() requires the
    # surface dict it's flushing; flush both real and imaginal surfaces on
    # shutdown, matching the pattern already used mid-loop at line 123.
    flush_surface(surface)
    flush_surface(imaginal_surface)

if __name__ == "__main__":
    main()
