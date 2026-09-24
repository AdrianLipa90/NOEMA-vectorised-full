"""NOEMA Subconscious daemon — Zeta/Schrödinger, Berry phase, wake signals.

Usage:
    python scripts/ciel_noema_subconscious_daemon.py [--interval SEC]
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.daemon_base import CielDaemon
from ciel_geometry.noema_surface_mmap import read_surface_state
from ciel_geometry.subconscious import Subconscious


class SubconsciousDaemon(CielDaemon):
    NAME = "subconscious"
    INTERVAL = 1.0
    REGISTER = False

    def __init__(self):
        super().__init__()
        self._sc = Subconscious()
        self._last_report = 0.0

    def setup(self):
        self._open_surface()
        self.log.info("Starting subconscious daemon (interval=%.1fs)", self.INTERVAL)
        self._last_report = time.monotonic()

    def tick(self):
        phi = self._surface["phi"].copy()
        state = read_surface_state(self._surface)
        R = state.get("coherence_index", 0.0)
        result = self._sc.step_all(phi, dt=0.01)

        now = time.monotonic()
        if now - self._last_report >= 10.0:
            self.log.info(
                "tick=%s  R=%.4f  zet_amp=%.4f  zet_H=%.4f  berry=%.4f  euler_closed=%s  identity=%.4f%s",
                self._surface["tick"][0],
                result.get("R", R),
                result.get("zet_amplitude", 0),
                result.get("zet_collatz_entropy", 0),
                result.get("berry_phase", 0),
                result.get("euler_closed", True),
                result.get("holonomic_identity_phase", 0),
                "  WAKE!" if "wake" in result else "",
            )
            self._last_report = now


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Subconscious daemon")
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()
    daemon = SubconsciousDaemon()
    daemon.INTERVAL = args.interval
    daemon.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
