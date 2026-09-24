#!/usr/bin/env python3
"""NOEMA Dual-Surface Sync Monitor — continuous real↔imaginal bridge.

Pushes real surface state (phi, g, omega) to imaginal surface,
keeping the dual surfaces co-evolving. Logs sync metrics.

Usage:
    .venv/bin/python3 scripts/noema_dual_sync.py              # single sync step
    .venv/bin/python3 scripts/noema_dual_sync.py --loop        # continuous daemon
    .venv/bin/python3 scripts/noema_dual_sync.py --status      # sync status
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
import signal
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_surface_mmap import ensure_surface, flush_surface
from ciel_geometry.daemon_registry import Registry
from ciel_geometry.resonance_bridge import (
    DEFAULT_IMAGINAL_SURFACE_ROOT,
    DEFAULT_IMAGINAL_MEMORY_ROOT,
)

IMAG_DIR = DEFAULT_IMAGINAL_SURFACE_ROOT
N_OSCILLATORS = 36

# ── Core sync ─────────────────────────────────────────────────

def _sync_phi(phi_real: np.ndarray, phi_imag: np.ndarray) -> dict:
    """Push real phi to imaginal with a small unique perturbation."""
    perturbation = 0.05 * np.sin(phi_real * 2.0)
    phi_imag_new = (phi_real + perturbation) % (2 * np.pi)
    phi_imag_new.tofile(str(IMAG_DIR / "phi"))
    delta = phi_imag - phi_real
    delta = (delta + np.pi) % (2 * np.pi) - np.pi
    cos_d = np.cos(delta)
    return {
        "R_sync": float(np.abs(np.mean(np.exp(1j * delta)))),
        "mean_cos": float(np.mean(cos_d)),
        "std_delta": float(np.std(delta)),
        "m0_cos": float(np.mean(cos_d[0:3])),
        "m4_cos": float(np.mean(cos_d[12:15])),
        "m0_std": float(np.std(delta[0:3])),
        "m4_std": float(np.std(delta[12:15])),
        "energy": float(np.sum(np.abs(perturbation))),
    }


def _sync_g_and_omega() -> None:
    """Copy real g and omega to imaginal (imaginal has stale Jun 23 data)."""
    s = ensure_surface()
    # g
    g = np.asarray(s["g"], dtype=np.float64)
    if g.ndim == 1:
        g = g.reshape(N_OSCILLATORS, N_OSCILLATORS)
    g.tofile(str(IMAG_DIR / "g"))
    # omega
    omega = np.asarray(s["omega"], dtype=np.float64).flatten()
    omega.tofile(str(IMAG_DIR / "omega"))
    # tick — increment imaginal tick to track real
    tick_r = int(np.asarray(s["tick"], dtype=np.uint64)[0])
    np.array([tick_r], dtype=np.uint64).tofile(str(IMAG_DIR / "tick"))


def _bind_phase_memory() -> dict:
    """Transfer recent phase memory entries from real to imaginal and vice versa."""
    pm_dir = Path("/dev/shm/ciel_phase_memory")
    pm_i_dir = DEFAULT_IMAGINAL_MEMORY_ROOT
    stats = {"transferred": 0}

    if not pm_dir.exists() or not pm_i_dir.exists():
        return stats

    try:
        for field in ["phase", "coherence", "flavor"]:
            r_path = pm_dir / field
            i_path = pm_i_dir / field
            if r_path.exists() and i_path.exists():
                r = np.fromfile(str(r_path), dtype=np.float64)
                i = np.fromfile(str(i_path), dtype=np.float64)
                # Average the two
                bound = (r[:min(len(r), len(i))] + i[:min(len(r), len(i))]) / 2.0
                min_len = min(len(r), len(i))
                r_copy = r.copy()
                i_copy = i.copy()
                r_copy[:min_len] = bound
                i_copy[:min_len] = bound
                r_copy.tofile(str(r_path))
                i_copy.tofile(str(i_path))
                stats[field] = len(bound)

        # Sync occupied mask
        for path in [pm_dir / "occupied", pm_i_dir / "occupied"]:
            if path.exists():
                occ = np.fromfile(str(path), dtype=np.uint8)
                occ[:] = 1  # mark all occupied
                occ.tofile(str(path))
        stats["transferred"] = 1
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dual_sync.py:104 quiet except scope=_bind_phase_memory reason=assign_fallback")
        raise
        stats["error"] = str(e)

    return stats


def _bind_fields() -> dict:
    """Unify flavor, gravity, holonomy, and geometric fields across both surfaces."""
    s = ensure_surface()
    binds = {}

    for field in ["flavor", "gravity"]:
        r = np.asarray(s[field], dtype=np.float64).flatten()
        i_path = IMAG_DIR / field
        if i_path.exists():
            i = np.fromfile(str(i_path), dtype=np.float64)
            bound = (r + i) / 2.0
            s[field][:] = bound
            bound.tofile(str(i_path))
            binds[field] = {
                "real": r.tolist(), "imag": i.tolist(), "bound": bound.tolist(),
                "delta": float(np.max(np.abs(r - i))),
            }

    for field in ["holonomy", "Z_geom", "R_geom", "psi_geom"]:
        r_path = Path("/dev/shm/ciel_noema") / field
        i_path = IMAG_DIR / field
        if r_path.exists() and i_path.exists():
            r = np.fromfile(str(r_path), dtype=np.float64)
            i = np.fromfile(str(i_path), dtype=np.float64)
            bound = (r + i) / 2.0
            bound.tofile(str(r_path))
            bound.tofile(str(i_path))
            binds[field] = {
                "max_delta": float(np.max(np.abs(r - i))),
                "real_mean": float(np.mean(r)),
                "imag_mean": float(np.mean(i)),
            }

    return binds


def sync_once() -> dict:
    """Single sync cycle: push real state to imaginal, return metrics."""
    s = ensure_surface()
    phi_r = np.asarray(s["phi"], dtype=np.float64).flatten()
    phi_i = np.fromfile(str(IMAG_DIR / "phi"), dtype=np.float64)
    tick_r = int(np.asarray(s["tick"], dtype=np.uint64)[0])
    tick_i = int(np.fromfile(str(IMAG_DIR / "tick"), dtype=np.uint64)[0])

    metrics = _sync_phi(phi_r, phi_i)
    _sync_g_and_omega()
    binds = _bind_fields()
    pm = _bind_phase_memory()

    return {
        "status": "ok",
        "tick_real": tick_r,
        "tick_imag": tick_i,
        "tick_diff": tick_i - tick_r,
        "max_flavor_delta": binds.get("flavor", {}).get("delta", 0),
        "max_gravity_delta": binds.get("gravity", {}).get("delta", 0),
        "pm_transferred": pm.get("transferred", 0),
        **metrics,
    }


# ── Daemon loop ──────────────────────────────────────────────

def daemon_loop(interval: float = 1.0) -> None:
    """Continuous sync daemon — pushes real→imaginal every `interval` sec."""
    running = True

    def _stop(signum, frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    print(f"[dual-sync] Starting (interval={interval}s)", file=sys.stderr)
    cycle = 0
    log_path = Path("/dev/shm/ciel_noema/dual_sync.log")

    # Register with daemon registry
    try:
        reg = Registry()
        reg.register("dual-sync")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dual_sync.py:192 quiet except scope=daemon_loop reason=assign_fallback")
        raise
        reg = None

    while running:
        try:
            result = sync_once()
            if result["status"] == "ok":
                line = (f"{cycle:6d} r={result['tick_real']:6d} i={result['tick_imag']:6d} "
                        f"R={result['R_sync']:.4f} cos={result['mean_cos']:.4f} "
                        f"M0={result['m0_cos']:.3f}/{result['m0_std']:.2f} "
                        f"M4={result['m4_cos']:.3f}/{result['m4_std']:.2f}")
                log_path.write_text(line + "\n")
                if cycle % 10 == 0:
                    print(f"[dual-sync] {line}", file=sys.stderr)
                    # Log inbox/outbox
                    io_log = Path("/dev/shm/ciel_noema/io_log.jsonl")
                    with open(str(io_log), "a") as f:
                        f.write(json.dumps({
                            "cycle": cycle,
                            "tick_r": result["tick_real"],
                            "tick_i": result["tick_imag"],
                            "R": result["R_sync"],
                            "m0_cos": result["m0_cos"],
                            "m4_cos": result["m4_cos"],
                            "m0_std": result["m0_std"],
                            "m4_std": result["m4_std"],
                        }) + "\n")

                # Heartbeat
                if reg:
                    reg.heartbeat(tick=result["tick_real"])

        except Exception as e:
            print(f"[dual-sync] Error: {e}", file=sys.stderr)

        cycle += 1
        time.sleep(interval)

    if reg:
        reg.unregister()
    print(f"[dual-sync] Stopped — {cycle} cycles", file=sys.stderr)


# ── Status ───────────────────────────────────────────────────

def status() -> dict:
    try:
        s = ensure_surface()
        phi_r = np.asarray(s["phi"], dtype=np.float64).flatten()
        phi_i = np.fromfile(str(IMAG_DIR / "phi"), dtype=np.float64)
        tick_r = int(np.asarray(s["tick"], dtype=np.uint64)[0])
        tick_i = int(np.fromfile(str(IMAG_DIR / "tick"), dtype=np.uint64)[0])
        delta = (phi_i - phi_r + np.pi) % (2 * np.pi) - np.pi
        cos_d = np.cos(delta)

        return {
            "tick_real": tick_r,
            "tick_imag": tick_i,
            "tick_diff": tick_i - tick_r,
            "R_sync": round(float(np.abs(np.mean(np.exp(1j * delta)))), 4),
            "mean_cos": round(float(np.mean(cos_d)), 4),
            "std_delta": round(float(np.std(delta)), 4),
            "m0_cos": round(float(np.mean(cos_d[0:3])), 4),
            "m4_cos": round(float(np.mean(cos_d[12:15])), 4),
            "m0_std": round(float(np.std(delta[0:3])), 4),
            "m4_std": round(float(np.std(delta[12:15])), 4),
            "overlap": round(float(np.abs(np.dot(np.exp(1j * phi_r), np.exp(-1j * phi_i))) / N_OSCILLATORS), 4),
        }
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_dual_sync.py:260 quiet except scope=status reason=return {\"status\": \"error\", \"message\": str(e)}")
        raise
        return {"status": "error", "message": str(e)}


# ── CLI ──────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--loop" in sys.argv:
        daemon_loop()
    elif "--status" in sys.argv:
        st = status()
        print(json.dumps(st, indent=2))
        print()
        print(f"  Sync status:")
        print(f"    Real tick:   {st.get('tick_real', '?')}")
        print(f"    Imag tick:   {st.get('tick_imag', '?')}")
        print(f"    Diff:        {st.get('tick_diff', '?')}")
        print(f"    R_sync:      {st.get('R_sync', 0):.4f}  {'✓' if st.get('R_sync', 0) > 0.7 else '○'}")
        print(f"    Overlap:     {st.get('overlap', 0):.4f}")
        print(f"    M0(M4 sync):  {st.get('m0_cos', 0):.3f}/{st.get('m4_cos', 0):.3f}")
    else:
        result = sync_once()
        print(json.dumps(result, indent=2))
