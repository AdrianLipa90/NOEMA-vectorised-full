"""NOEMA Linux Sensor Daemon — mapuje system na powierzchnię /dev/shm/ciel_noema.

Usage:
    sudo python scripts/ciel_noema_linux_sensor_daemon.py

Zapisuje na powierzchnię:
    phi[0..23]   → wymiary systemowe (CPU, mem, IO, net, procs)
    omega[0..23] → prędkość zmian (1. pochodna)
    flavor[0..5] → zagregowane metryki
    tick         → licznik snapshotów
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.daemon_base import CielDaemon
from ciel_geometry.linux_sensor import LinuxSensor, top_processes
from ciel_geometry.noema_surface_mmap import DEFAULT_SURFACE_ROOT


class LinuxSensorDaemon(CielDaemon):
    NAME = "sensor"
    INTERVAL = 1.0

    def __init__(self):
        super().__init__()
        self._sensor = LinuxSensor()
        self._prev_fingerprint = ""

    def setup(self):
        if not (self.SURFACE_ROOT / "phi").exists():
            self.log.error("powierzchnia nie istnieje: %s", self.SURFACE_ROOT)
            sys.exit(1)
        self._open_surface()
        self._setup_registry()
        self.log.info("start — %s, interval=%.1fs", self.SURFACE_ROOT, self.INTERVAL)

    def tick(self):
        snap = self._sensor.snapshot()
        self._sensor.write_surface(self._surface, snap)

        if snap.tick % 5 == 0:
            pn = self._sensor.process_phasenav(snap)
            fp = pn["harmonic_fingerprint"]
            op = pn["operator"]
            td = pn["thinking_delta"]
            fl = pn["flavor"]

            if fp != self._prev_fingerprint:
                self.log.info("[%s] φ:%s ∥ %s ∥ δΦ:%.4f ∥ F:%s", snap.tick, fp, op, td, fl)
                self._prev_fingerprint = fp

            if snap.tick % 30 == 0:
                top = top_processes(5)
                if top:
                    self.log.info("── top 5 procesów ──")
                    for p in top:
                        pp = p["phasenav"]
                        self.log.info(
                            "  PID %6d %-24s CPU:%.1fs → %s (%s)",
                            p["pid"], p["comm"][:24], p["cpu_sec"],
                            pp["operator_id"], pp["harmonic_fingerprint"],
                        )


def main():
    ap = argparse.ArgumentParser(description="NOEMA Linux Sensor Daemon")
    ap.add_argument("--root", type=str, default=str(DEFAULT_SURFACE_ROOT))
    args = ap.parse_args()
    daemon = LinuxSensorDaemon()
    daemon.SURFACE_ROOT = Path(args.root)
    daemon.run()


if __name__ == "__main__":
    main()
