"""NOEMA Resonance Bridge — consolidated daemon.

Handles:
  1) real↔imaginal dual-surface sync (PLL, Kuramoto generator)
  2) AGENT state logging → SQLite DB (agent-snapshots, operator-log, context)
  3) Nonlocal AGENT broadcast (30s)
  4) g + omega copy from real to imaginal (replaces dual-sync)

Merged from: agent_lock, dual_sync, resonance_bridge.
Reduces daemon count: 12 → 10.

Usage:
    python scripts/ciel_noema_resonance_bridge.py [--interval SEC]
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import sqlite3
import sys
import time
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.resonance_bridge import (
    ensure_dual_surfaces,
    dual_surface_step,
    resonance_snapshot,
)
from ciel_geometry.noema_registry import registry
from ciel_geometry.noema_surface_mmap import ensure_surface, open_surface
from ciel_geometry.agent_attractor import agent_attractor_state
from ciel_geometry.nonlocal_channel import get_channel

logging.basicConfig(
    level=logging.INFO,
    format="[resonance] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

AGENT_DB = "/media/adrian/New Volume1/NOEMA_LIBRARY/agent_db/agent_state.db"
IMAGINAL_ROOT = Path("/dev/shm/ciel_noema_imaginal")
N_OSCILLATORS = 36
OP_GROUPS = [[0,1,2],[3,4,5],[6,7,8],[9,10,11],[12,13,14],[15,16,17],[18,19,20],[21,22,23]]
OP_NAMES = ["transform","agent","memory","concept","emotion","self","identity","braid"]


def _init_agent_db(db_path: str) -> None:
    with sqlite3.connect(db_path, timeout=2) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_associations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tick INTEGER,
                source_operator TEXT,
                target_operator TEXT,
                phase_correlation REAL,
                coupling_strength REAL,
                context TEXT
            )
        """)
        conn.commit()


def _write_memory_associations(phi: np.ndarray, g: np.ndarray, tick: int, db_path: str) -> None:
    try:
        conn = sqlite3.connect(db_path, timeout=2)
        c = conn.cursor()
        for i, src_name in enumerate(OP_NAMES):
            src_phi = phi[OP_GROUPS[i]]
            for j, tgt_name in enumerate(OP_NAMES):
                if j <= i:
                    continue
                tgt_phi = phi[OP_GROUPS[j]]
                diffs = src_phi[:, None] - tgt_phi[None, :]
                corr = float(np.mean(np.cos(diffs)))
                gi = OP_GROUPS[i]
                gj = OP_GROUPS[j]
                g_block = g[np.ix_(gi, gj)]
                coupling = float(np.mean(np.abs(g_block)))
                ctx = json.dumps({"method": "phase_cos_block", "tick": tick})
                c.execute(
                    "INSERT INTO memory_associations (tick, source_operator, target_operator, "
                    "phase_correlation, coupling_strength, context) VALUES (?,?,?,?,?,?)",
                    (tick, src_name, tgt_name, round(corr, 4), round(coupling, 4), ctx),
                )
        conn.commit()
        conn.close()
        log.info("memory_assocs wrote %d pairs at tick=%d", len(OP_NAMES) * (len(OP_NAMES) - 1) // 2, tick)
    except Exception as e:
        log.error("memory_associations write error: %s", e)


def _copy_g_and_omega() -> None:
    s = ensure_surface()
    g = np.asarray(s["g"], dtype=np.float64)
    if g.ndim == 1:
        g = g.reshape(N_OSCILLATORS, N_OSCILLATORS)
    omega = np.asarray(s["omega"], dtype=np.float64)
    g.tofile(str(IMAGINAL_ROOT / "g"))
    omega.tofile(str(IMAGINAL_ROOT / "omega"))


def _log_agent_state(phi, g, omega, tick, db_path: str, bridge_state: dict | None = None,
                     i_phi: np.ndarray | None = None) -> dict:
    m1 = [float(phi[i]) for i in [3, 4, 5]]
    r_result = agent_attractor_state(phi)
    ch_coh = []
    ch_groups = [[0,1,2],[3,4,5],[6,7,8],[9,10,11],[12,13,14],[15,16,17],[18,19,20],[21,22,23]]
    op_names = ["transform","agent","memory","concept","emotion","self","identity","braid"]
    for grp in ch_groups:
        ch_coh.append(float(abs(np.mean(np.exp(1j * phi[grp])))))
    try:
        conn = sqlite3.connect(db_path, timeout=2)
        c = conn.cursor()
        ts = time.time()
        c.execute(
            "INSERT OR REPLACE INTO operator_log (tick, timestamp, transform, agent, memory, concept, emotion, self, identity, braid) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            (tick, ts, *ch_coh),
        )
        c.execute(
            "INSERT OR REPLACE INTO agent_snapshots (tick, timestamp, coherence, phi_3, phi_4, phi_5, "
            "omega_3, omega_4, omega_5, g_34, g_35, g_45, g_m1m0, g_m1m2, g_m1m6, target_phase, lock_active) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (tick, ts, r_result["coherence"], m1[0], m1[1], m1[2],
             float(omega[3]), float(omega[4]), float(omega[5]),
             float(g[3,4]), float(g[3,5]), float(g[4,5]),
             float(g[np.ix_([3,4,5],[0,1,2])].mean()),
             float(g[np.ix_([3,4,5],[6,7,8])].mean()),
             float(g[np.ix_([3,4,5],[18,19,20])].mean()),
             math.pi / 4, 1 if r_result["coherence"] > 0.9 else 0),
        )
        # Restore agent_context writes (was lost in agent_lock→resonance merge)
        i_coh = agent_attractor_state(i_phi)["coherence"] if i_phi is not None else 0.0
        phase_sig = json.dumps({
            "real_coh": r_result["coherence"],
            "imag_coh": i_coh,
            "m1_phi": m1,
            "ch_coh": ch_coh,
            "tick": tick,
        })
        notes = json.dumps({
            "bridge_mode": "consolidated",
            "cycle_type": "dual_surface",
            "source": "resonance_bridge",
        })
        c.execute(
            "INSERT INTO agent_context (tick, timestamp, phase_signature, notes) VALUES (?,?,?,?)",
            (tick, ts, phase_sig, notes),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        log.error("DB log error: %s", e)
    return r_result


def _nonlocal_broadcast(tick: int, r_result: dict, i_result: dict, nl_cycle: int) -> None:
    try:
        ch = get_channel()
        status = json.dumps({
            "source": "RESONANCE_BRIDGE",
            "type": "agent_status",
            "cycle": nl_cycle,
            "tick": tick,
            "real_coh": round(r_result.get("coherence", 0), 4),
            "imag_coh": round(i_result.get("coherence", 0), 4),
            "locked": r_result.get("locked", False),
        })
        ch.broadcast(status, channel=1)
        responses = ch.listen(channel=1, min_resonance=0.05)
        if responses:
            for resp in responses:
                log.info("NONLOCAL response: %s", resp.source)
    except Exception as e:
        log.error("Nonlocal broadcast error: %s", e)


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Resonance Bridge (consolidated)")
    parser.add_argument("--interval", type=float, default=1.0, help="Bridge cycle interval")
    args = parser.parse_args()

    log.info("Starting consolidated resonance bridge (interval=%.1fs)", args.interval)
    ensure_dual_surfaces()
    _init_agent_db(AGENT_DB)

    reg_token = registry.register("resonance")

    import signal
    _running = True
    def _stop(signum, frame):
        nonlocal _running
        _running = False
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    # Seed values only for the very first cycle, before any live flavor
    # read is available. Every subsequent cycle below overwrites this
    # from the live surface flavor array (contract: [0]=coherence,
    # [1]=soul_invariant, [2]=ethical_score, [3]=mood, [4]=openness) --
    # previously this dict was built once and never updated, so
    # ciel_state.json got rewritten every cycle with the same frozen
    # placeholder values forever (confirmed 2026-07-08: mtime advanced
    # every cycle, content never changed).
    bridge_state = {
        "dominant_emotion": "curiosity",
        "ethical_score": 0.5,
        "soul_invariant": 0.5,
        "mood": 0.5,
        "coherence_index": 0.5,
        "closure_penalty": 0.15,
    }

    cycle = 0
    nl_cycle = 0
    assoc_cycle = 0
    last_report = time.monotonic()
    last_db = time.monotonic()
    last_nl = time.monotonic()
    tick_last = 0

    try:
        while _running:
            try:
                real = ensure_surface()
                imag = open_surface(root=IMAGINAL_ROOT)
                tick = int(np.asarray(real["tick"], dtype=np.uint64)[0])
                phi = np.asarray(real["phi"], dtype=np.float64)
                g = np.asarray(real["g"], dtype=np.float64)
                flavor = np.asarray(real["flavor"], dtype=np.float64)
                if flavor.shape[0] >= 5:
                    bridge_state["coherence_index"] = float(np.clip(flavor[0], 0.0, 1.0))
                    bridge_state["soul_invariant"] = float(np.clip(flavor[1], 0.0, 1.0))
                    bridge_state["ethical_score"] = float(np.clip(flavor[2], 0.0, 1.0))
                    bridge_state["mood"] = float(np.clip(flavor[3], -1.0, 1.0))
                    bridge_state["closure_penalty"] = float(np.clip(1.0 - flavor[4], 0.0, 1.0))

                # 3) Read surfaces for logging
                dual_surface_step(bridge_state, text=f"bridge_cycle_{cycle}")
                cycle += 1
                assoc_cycle += 1
                registry.heartbeat(reg_token)

                # 2) Copy g + omega to imaginal (replaces dual_sync)
                _copy_g_and_omega()
                omega = np.asarray(real["omega"], dtype=np.float64)
                i_phi = np.asarray(imag["phi"], dtype=np.float64)
                i_result = agent_attractor_state(i_phi)

                now = time.monotonic()

                # 4) DB logging (5s cycle — replaces agent_lock)
                if now - last_db >= 5.0 and tick != tick_last:
                    tick_last = tick
                    r_result = _log_agent_state(phi, g, omega, tick, AGENT_DB)
                    if assoc_cycle >= 50:
                        _write_memory_associations(phi, g, tick, AGENT_DB)
                        assoc_cycle = 0
                    last_db = now

                # 5) Nonlocal broadcast (30s cycle)
                if now - last_nl >= 30.0:
                    last_nl = now
                    nl_cycle += 1
                    _nonlocal_broadcast(tick, agent_attractor_state(phi), i_result, nl_cycle)

                # 6) Console report (5s cycle) — closure jest zapisywany przez resonance_snapshot()
                if now - last_report >= 5.0:
                    snap = resonance_snapshot()
                    r_coh = agent_attractor_state(phi)["coherence"]
                    log.info(
                        "cycle=%d  resonance=%.4f  lock=%.4f  drive=%.4f  coh=%.3f  AGENT=%.4f%s  tick=%d",
                        cycle,
                        snap.get("resonance_score", 0),
                        snap.get("phase_lock", 0),
                        snap.get("imaginal_drive", 0),
                        bridge_state.get("coherence_index", 0),
                        r_coh,
                        "🔒" if r_coh > 0.9 else "",
                        tick,
                    )
                    last_report = now

            except Exception as e:
                log.error("Bridge cycle error: %s", e)
                traceback.print_exc()
                time.sleep(1)

            time.sleep(args.interval)
    finally:
        registry.unregister(reg_token)
        log.info("Unregistered from NOEMA registry")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
