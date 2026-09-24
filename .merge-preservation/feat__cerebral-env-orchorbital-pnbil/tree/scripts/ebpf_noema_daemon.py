"""eBPF NOEMA Sensor Daemon — tracepoint → surface, real-time.

Usage:
    sudo python3 scripts/ebpf_noema_daemon.py [--interval 1.0]
"""

from __future__ import annotations

import argparse
import os
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
from ciel_geometry.daemon_base import CielDaemon
from ciel_geometry.ebpf_noema_loader import EBPFSensor
from ciel_geometry.noema_surface_mmap import open_surface, DEFAULT_SURFACE_ROOT


class EBPFDaemon(CielDaemon):
    NAME = "ebpf"
    INTERVAL = 1.0
    REGISTER = False

    def __init__(self):
        super().__init__()
        self._sensor = EBPFSensor()

    def setup(self):
        self._surface = open_surface(DEFAULT_SURFACE_ROOT)
        self.log.info("loading eBPF program...")
        self._sensor.start()
        self.log.info("running at %.1fs interval", self.INTERVAL)

    def tick(self):
        snap = self._sensor.snapshot()
        self._sensor.write_surface(self._surface, snap)
        if snap["tick"] % 5 == 0:
            R = float(abs(np.mean(np.exp(1j * snap["phi"]))))
            self.log.info(
                "tick=%s R=%.4f CS=%.0f F=%s",
                snap["tick"], R,
                snap["raw"].get("ctx_switches", 0),
                [round(float(f), 2) for f in snap["flavor"]],
            )

    def shutdown(self):
        self._sensor.stop()
        self.log.info("stopped")


def main():
    ap = argparse.ArgumentParser(description="eBPF NOEMA Sensor Daemon")
    ap.add_argument("--interval", type=float, default=1.0)
    args = ap.parse_args()
    daemon = EBPFDaemon()
    daemon.INTERVAL = args.interval
    daemon.run()


if __name__ == "__main__":
    main()
