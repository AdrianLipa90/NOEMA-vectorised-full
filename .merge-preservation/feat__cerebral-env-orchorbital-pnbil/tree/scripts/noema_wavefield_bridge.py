#!/usr/bin/env python3
"""NOEMA Wavefield Bridge — continuous_vector_wavefield_mmap_ring.

Projects NOEMA surface state (phi, g, linux_load) into a 512KB mmap ring
at /dev/shm/ciel_noema/wavefield/wavefield_ring.float32 (256×64×8 float32).

Wavefield channels (axis=2):
  0: phi_re   — real part of oscillator phi (from /dev/shm/ciel_noema/phi)
  1: phi_im   — imaginary part of oscillator phi
  2: pi_re    — time derivative of phi (real), 2-frame buffer
  3: pi_im    — time derivative of phi (imag)
  4: drive    — Kuramoto drive strength (norm of g matrix)
  5: duty     — scaled linux_load [0-1]
  6: w_ir     — coupling W proxy (norm of phi)
  7: w_ri     — conjugate coupling proxy

Usage:
    python3 scripts/noema_wavefield_bridge.py --daemon   # run
    python3 scripts/noema_wavefield_bridge.py --stop      # stop via PID
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import os
import signal
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

try:
    from ciel_geometry.noema_registry import registry
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_wavefield_bridge.py:39 quiet except scope=<module> reason=assign_fallback")
    raise
    registry = None

SURFACE = Path("/dev/shm/ciel_noema")
WAVEDIR = SURFACE / "wavefield"

RING_FILE = WAVEDIR / "wavefield_ring.float32"
META_FILE = WAVEDIR / "wavefield_meta.json"
PID_FILE = WAVEDIR / "wavefield.pid"

RING_LEN = 256
NODES = 64
COMPONENTS = 8
DTYPE = "float32"
SHAPE = (RING_LEN, NODES, COMPONENTS)
BYTES = RING_LEN * NODES * COMPONENTS * np.dtype(DTYPE).itemsize  # 512KB

COMPONENT_NAMES = [
    "phi_re", "phi_im",
    "pi_re", "pi_im",
    "drive", "duty",
    "w_ir", "w_ri",
]

INTERVAL = 0.5  # seconds

_running = True


def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[wavefield] {ts} {msg}", flush=True)


def _init_wavefield_dir() -> None:
    WAVEDIR.mkdir(parents=True, exist_ok=True)

    if not RING_FILE.exists():
        # Create the ring file with zeros
        ring = np.memmap(
            str(RING_FILE), dtype=DTYPE, mode="w+", shape=SHAPE
        )
        ring[:] = 0.0
        ring.flush()
        del ring
        log(f"ring created: {BYTES} bytes ({SHAPE})")

    # Write meta
    meta = {
        "component_names": COMPONENT_NAMES,
        "components": COMPONENTS,
        "dtype": DTYPE,
        "ring_len": RING_LEN,
        "nodes": NODES,
        "shape": list(SHAPE),
        "transport": "continuous_vector_wavefield_mmap_ring",
        "last_slot": 0,
        "last_tick": 0,
        "updated_ms": 0,
    }
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)
    log("meta written")


def _read_surface() -> dict:
    """Read NOEMA surface state. Returns dict with numpy arrays or None."""
    result = {}
    try:
        phi = np.fromfile(SURFACE / "phi", dtype=np.complex128)
        result["phi"] = phi
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_wavefield_bridge.py:110 quiet except scope=_read_surface reason=assign_fallback")
        raise
        result["phi"] = np.zeros(18, dtype=np.complex128)

    try:
        g = np.fromfile(SURFACE / "g", dtype=np.float64)
        result["g"] = g
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_wavefield_bridge.py:116 quiet except scope=_read_surface reason=assign_fallback")
        raise
        result["g"] = np.zeros(1296, dtype=np.float64)

    try:
        linux_load = np.fromfile(SURFACE / "linux_load", dtype=np.float64)
        result["linux_load"] = linux_load
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_wavefield_bridge.py:122 quiet except scope=_read_surface reason=assign_fallback")
        raise
        result["linux_load"] = np.zeros(1, dtype=np.float64)

    try:
        tick = np.fromfile(SURFACE / "tick", dtype=np.int64)
        result["tick"] = tick
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_wavefield_bridge.py:128 quiet except scope=_read_surface reason=assign_fallback")
        raise
        result["tick"] = np.zeros(1, dtype=np.int64)

    return result


def _build_frame(
    surface: dict,
    prev_phi: np.ndarray | None,
) -> np.ndarray:
    """Build one wavefield frame (NODES × COMPONENTS) from surface data."""
    frame = np.zeros((NODES, COMPONENTS), dtype=np.float32)

    phi = surface.get("phi", np.zeros(18, dtype=np.complex128))
    g = surface.get("g", np.zeros(1296, dtype=np.float64))
    linux_load = surface.get("linux_load", np.zeros(1, dtype=np.float64))
    tick = surface.get("tick", np.zeros(1, dtype=np.int64))

    n_osc = len(phi)  # typically 18

    # phi_re / phi_im (ch 0, 1): spread oscillator complex values across nodes
    for k in range(min(n_osc, NODES)):
        frame[k, 0] = float(phi[k].real)
        frame[k, 1] = float(phi[k].imag)
    # Nodes beyond n_osc stay 0

    # pi_re / pi_im (ch 2, 3): time derivative
    if prev_phi is not None:
        dt = float(INTERVAL)
        if dt > 0:
            for k in range(min(n_osc, NODES)):
                dphi = phi[k] - prev_phi[k]
                frame[k, 2] = float(dphi.real) / dt
                frame[k, 3] = float(dphi.imag) / dt

    # drive (ch 4): Kuramoto drive strength from g matrix norm
    g_norm = float(np.linalg.norm(g)) if len(g) > 0 else 0.0
    frame[:, 4] = g_norm

    # duty (ch 5): scaled linux_load [0-1]
    load_val = float(linux_load[0]) if len(linux_load) > 0 else 0.0
    # Scale: linux load average capped at 100 → [0-1]
    duty = min(load_val / 100.0, 1.0)
    frame[:, 5] = duty

    # w_ir (ch 6): coupling W proxy — norm of phi vector
    phi_norm = float(np.linalg.norm(phi)) if n_osc > 0 else 0.0
    frame[:, 6] = phi_norm

    # w_ri (ch 7): conjugate coupling proxy — abs of sum of conj products
    if n_osc > 0:
        w_ri = float(np.abs(np.sum(phi * np.conj(np.roll(phi, 1)))))
    else:
        w_ri = 0.0
    frame[:, 7] = w_ri

    return frame


def _write_ring(ring: np.memmap, slot: int, frame: np.ndarray) -> None:
    """Atomically write one frame into the ring buffer."""
    ring[slot, :, :] = frame
    ring.flush()


def _update_meta(slot: int, tick_val: int) -> None:
    """Update last_slot, last_tick, updated_ms in meta JSON."""
    try:
        meta = json.loads(META_FILE.read_text())
        meta["last_slot"] = slot
        meta["last_tick"] = int(tick_val)
        meta["updated_ms"] = int(time.time() * 1000)
        with open(META_FILE, "w") as f:
            json.dump(meta, f, indent=2)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_wavefield_bridge.py:202 quiet except scope=_update_meta reason=pass")
        raise
        pass


def signal_handler(sig, frame) -> None:
    global _running
    log(f"signal {sig}, exiting")
    _running = False


def main() -> None:
    global _running

    parser = argparse.ArgumentParser(
        description="NOEMA Wavefield Bridge — continuous vector wavefield mmap ring"
    )
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--stop", action="store_true", help="Stop running daemon")
    args = parser.parse_args()

    if args.stop:
        if PID_FILE.exists():
            pid = int(PID_FILE.read_text().strip())
            try:
                os.kill(pid, signal.SIGTERM)
                log(f"sent SIGTERM to pid {pid}")
            except ProcessLookupError:
                log(f"pid {pid} not found, removing stale PID file")
            PID_FILE.unlink(missing_ok=True)
        else:
            log("no PID file found, nothing to stop")
        return

    if not args.daemon:
        parser.print_help()
        sys.exit(1)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    _init_wavefield_dir()

    # Write PID
    PID_FILE.write_text(str(os.getpid()))
    log(f"pid {os.getpid()}")

    # Open mmap ring
    ring = np.memmap(
        str(RING_FILE), dtype=DTYPE, mode="r+", shape=SHAPE
    )

    # Register with daemon registry
    reg_token = None
    if registry is not None:
        try:
            reg_token = registry.register("wavefield_bridge")
            log("registered with daemon registry")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_wavefield_bridge.py:259 quiet except scope=main reason=pass")
            raise
            pass

    slot = 0
    prev_phi: np.ndarray | None = None
    hb_count = 0

    log(f"daemon start — interval={INTERVAL}s, ring={SHAPE}")

    while _running:
        try:
            t0 = time.time()

            # Read surface
            surface = _read_surface()
            current_tick = surface.get("tick", np.zeros(1, dtype=np.int64))

            # Build and write frame
            frame = _build_frame(surface, prev_phi)
            _write_ring(ring, slot, frame)
            _update_meta(slot, current_tick[0] if len(current_tick) > 0 else 0)

            # Store for derivative
            prev_phi = surface["phi"].copy()

            slot = (slot + 1) % RING_LEN

            # Heartbeat
            hb_count += 1
            if hb_count % 20 == 0 and registry is not None and reg_token is not None:
                try:
                    registry.heartbeat(reg_token)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_wavefield_bridge.py:291 quiet except scope=main reason=pass")
                    raise
                    pass

            elapsed = time.time() - t0
            sleep_time = max(0.0, INTERVAL - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)

        except Exception as e:
            log(f"error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(1.0)

    # Cleanup
    del ring
    PID_FILE.unlink(missing_ok=True)
    log("daemon stop")


if __name__ == "__main__":
    main()
