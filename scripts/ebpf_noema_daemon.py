#!/usr/bin/env python3
"""eBPF NOEMA Sensor Daemon — tracepoint → surface, real-time.

Usage:
    sudo python3 scripts/ebpf_noema_daemon.py [--interval 1.0]
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
import signal
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
_DEFAULT_SITE = os.path.join(str(Path.home()), ".local", "lib", "python3.12", "site-packages")
_UPATH = os.environ.get("PYTHON_SITE_PACKAGES", _DEFAULT_SITE)
if _UPATH not in sys.path:
    sys.path.insert(0, _UPATH)

import numpy as np
from ciel_geometry.ebpf_noema_loader import EBPFSensor
from ciel_geometry.noema_surface_mmap import open_surface, DEFAULT_SURFACE_ROOT

def main():
    ap = argparse.ArgumentParser(description="eBPF NOEMA Sensor Daemon")
    ap.add_argument("--interval", type=float, default=1.0)
    args = ap.parse_args()

    surface = open_surface(DEFAULT_SURFACE_ROOT)
    sensor = EBPFSensor()
    print("[eBPF] loading eBPF program...", flush=True)
    sensor.start()
    print(f"[eBPF] running at {args.interval}s interval", flush=True)

    running = True
    def _handler(signum, frame):
        nonlocal running; running = False
    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)

    while running:
        t0 = time.perf_counter_ns()
        try:
            snap = sensor.snapshot()
            sensor.write_surface(surface, snap)
            if snap["tick"] % 5 == 0:
                R = float(abs(np.mean(np.exp(1j * snap["phi"]))))
                print(f"[eBPF] tick={snap['tick']} R={R:.4f} "
                      f"CS={snap['raw'].get('ctx_switches',0):.0f} "
                      f"F={[round(float(f),2) for f in snap['flavor']]}",
                      flush=True)
        except Exception as e:
            print(f"[eBPF] error: {e}", file=sys.stderr, flush=True)
        elapsed = (time.perf_counter_ns() - t0) / 1e9
        remaining = args.interval - elapsed
        if remaining > 0:
            try:
                time.sleep(remaining)
            except KeyboardInterrupt:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ebpf_noema_daemon.py:68 quiet except scope=main reason=break")
                break

    sensor.stop()
    print("[eBPF] stopped", flush=True)

if __name__ == "__main__":
    main()
