#!/usr/bin/env python3
"""NOEMA Linux Body Bridge — PhaseEncoder → sensor_raw → kuramoto daemon.

Używa CIELingo PhaseEncoder do mapowania stanu Linux na 36D konfigurację
fazową przez fast_encode_text(). Daemon czyta sensor_raw co cykl (0.2s)
i blenduje 15% do phi.

Usage:
    python3 scripts/noema_linux_body_bridge.py            # oneshot
    python3 scripts/noema_linux_body_bridge.py --daemon   # co 2s
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import logging
import signal
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from ciel_geometry.cielingo_phase_encoder import fast_encode_text
from ciel_geometry.noema_surface_mmap import ensure_surface

logging.basicConfig(
    level=logging.INFO,
    format="[linux-body] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

SURFACE_PATH = Path("/dev/shm/ciel_noema")
LINUX_CARDS = SURFACE_PATH / "linux_cards"
TWO_PI = 2.0 * np.pi


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_linux_body_bridge.py:46 quiet except scope=_read_json reason=return {}")
        return {}


def build_linux_text() -> str:
    """Build a descriptive text of current linux state for PhaseEncoder."""
    cpu = _read_json(LINUX_CARDS / "cpu_summary.json")
    hw = _read_json(LINUX_CARDS / "hardware.json")
    
    load = cpu.get("mean_busy_pct", 12.0)
    net_conn = hw.get("net_conns", 9800)
    sensors = hw.get("sensors", 17)
    procs = hw.get("processes", 200)
    disks = hw.get("disks", 13)
    modules = hw.get("modules", 233)
    
    # Build text that PhaseEncoder will map to structured 36D phi
    # Key words trigger specific oscillator groups via TF hashing
    text = (
        f"sync linux cpu load {load:.0f} percent "
        f"network connections {net_conn} "
        f"sensors {sensors} processes {procs} "
        f"disks {disks} modules {modules} "
        f"oscilator synchronize coherent phase lock"
    )
    return text


def build_sensor_raw() -> np.ndarray:
    """PhaseEncoder → 36D sensor_raw."""
    text = build_linux_text()
    phi = fast_encode_text(text)
    return np.clip(phi, 0.0, TWO_PI)


def write_sensor_raw(sr: np.ndarray, surface: dict | None = None):
    if surface is not None:
        surface["sensor_raw"][:] = sr
    else:
        (SURFACE_PATH / "sensor_raw").write_bytes(sr.tobytes())


def daemon_loop(interval: float = 2.0):
    log.info("Starting PhaseEncoder bridge (interval=%.1fs)", interval)
    surface = ensure_surface()
    if "sensor_raw" not in surface:
        log.error("sensor_raw not in surface")
        return
    
    _running = True
    def _stop(s, f):
        nonlocal _running
        _running = False
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    
    while _running:
        try:
            text = build_linux_text()
            sr = build_sensor_raw()
            write_sensor_raw(sr, surface)
            if log.isEnabledFor(logging.INFO):
                log.info("sensor_raw μ=%.4f σ=%.4f | %s", sr.mean(), sr.std(), text[:60])
        except Exception as e:
            log.error("Bridge error: %s", e)
        time.sleep(interval)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action="store_true")
    parser.add_argument("--interval", type=float, default=2.0)
    args = parser.parse_args()
    
    if args.daemon:
        daemon_loop(interval=args.interval)
    else:
        sr = build_sensor_raw()
        write_sensor_raw(sr)
        text = build_linux_text()
        print(f"Text: {text}")
        print(f"sensor_raw: μ={sr.mean():.4f} σ={sr.std():.4f}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
