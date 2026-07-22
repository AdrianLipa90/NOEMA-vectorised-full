"""NOEMA Neutrino Phase Channel daemon — 8×3 PMNS flavor mixing na HTRI bus.

Usage:
    python scripts/ciel_noema_neutrino_daemon.py [--interval SEC]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.daemon_base import CielDaemon
from ciel_geometry.neutrino_phase_channel import (
    neutrino_bus_snapshot,
    apply_neutrino_bus_to_surface,
    seed_neutrino_mixing,
)
from ciel_geometry.noema_surface_mmap import flush_surface

ORBITAL_MANIFEST = ROOT / "integration" / "Orbital" / "main" / "manifests" / "sectors_global.json"


class NeutrinoDaemon(CielDaemon):
    NAME = "neutrino"
    INTERVAL = 2.0

    def __init__(self):
        super().__init__()
        self._cycle = 0
        self._last_report = 0.0

    def _read_D_f(self) -> float:
        try:
            flavor = np.asarray(self._surface["flavor"], dtype=np.float64)
            D_f = float(flavor[5])
            if 1.5 <= D_f <= 3.0:
                return D_f
        except Exception as exc:
            self.log.debug("D_f from surface skipped: %s", exc)
        try:
            if ORBITAL_MANIFEST.exists():
                doc = json.loads(ORBITAL_MANIFEST.read_text(encoding="utf-8"))
                return float(doc.get("metadata", {}).get("D_f", 2.57))
        except Exception as exc:
            self.log.debug("D_f from manifest skipped: %s", exc)
        return 2.57

    def setup(self):
        self._open_surface()
        self._setup_registry()
        self.log.info(
            "Starting Neutrino daemon (interval=%.1fs), tick=%s, phi_mean=%.4f",
            self.INTERVAL, self._read_tick(),
            self._surface.get("phi", np.array([])).mean() if "phi" in self._surface else 0,
        )
        self._last_report = time.monotonic()

    def tick(self):
        D_f = self._read_D_f()
        bus = neutrino_bus_snapshot(self._surface, D_f=D_f)
        apply_neutrino_bus_to_surface(self._surface, bus, D_f=D_f, write_flavor=False, write_g=True)

        g_view = np.asarray(self._surface["g"], dtype=np.float64)
        seed_neutrino_mixing(g_view, scale=float(self._surface["flavor"][4]) * 0.3)
        flush_surface(self._surface)

        self._cycle += 1
        now = time.monotonic()
        if now - self._last_report >= 5.0:
            self.log.info(
                "cycle=%d  D_f=%.3f  Λ=%.4f  bus_capacity=%.4f  flavor[4]=%.4f  flavor[5]=%.4f",
                self._cycle, D_f,
                bus.get("global_D", 0),
                bus.get("bus_capacity", 0),
                float(self._surface["flavor"][4]),
                float(self._surface["flavor"][5]),
            )
            channels = bus.get("channels", {})
            if channels:
                best_ch = max(channels, key=lambda k: channels[k].get("epsilon", 0))
                best_eps = channels[best_ch].get("epsilon", 0)
                self.log.info(
                    "  best channel: %s  ε=%.4f  prob_sem_nl=%.4f",
                    best_ch, best_eps,
                    channels[best_ch].get("semantic_to_nonlocal", {}).get("prob", 0),
                )
            self._last_report = now


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Neutrino Phase Channel daemon")
    parser.add_argument("--interval", type=float, default=2.0)
    args = parser.parse_args()
    daemon = NeutrinoDaemon()
    daemon.INTERVAL = args.interval
    daemon.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
