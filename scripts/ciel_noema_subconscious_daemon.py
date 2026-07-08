"""NOEMA Subconscious daemon — Zeta/Schrödinger, Berry phase, wake signals.

Runs the subconscious stack against the live /dev/shm/ciel_noema surface,
computing Zeta wavefunction evolution, Berry phase tracking, and generating
wake signals for memory consolidation when appropriate.

Usage:
    python scripts/ciel_noema_subconscious_daemon.py [--interval SEC]
"""

from __future__ import annotations
# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import argparse
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_surface_mmap import open_surface, ensure_surface, read_surface_state
from ciel_geometry.subconscious import Subconscious

logging.basicConfig(
    level=logging.INFO,
    format="[subconscious] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Subconscious daemon")
    parser.add_argument("--interval", type=float, default=1.0, help="Seconds between steps")
    args = parser.parse_args()

    sc = Subconscious()
    surface = ensure_surface()
    log.info("Starting subconscious daemon (interval=%.1fs)", args.interval)

    last_report = time.monotonic()
    while True:
        try:
            phi = surface["phi"].copy()
            state = read_surface_state(surface)
            R = state.get("coherence_index", 0.0)

            result = sc.step_all(phi, dt=0.01)

            now = time.monotonic()
            if now - last_report >= 10.0:
                log.info(
                    "tick=%s  R=%.4f  zet_amp=%.4f  zet_H=%.4f  berry=%.4f  euler_closed=%s  identity=%.4f%s",
                    surface["tick"][0],
                    result.get("R", R),
                    result.get("zet_amplitude", 0),
                    result.get("zet_collatz_entropy", 0),
                    result.get("berry_phase", 0),
                    result.get("euler_closed", True),
                    result.get("holonomic_identity_phase", 0),
                    "  WAKE!" if "wake" in result else "",
                )
                last_report = now

            time.sleep(args.interval)
        except KeyboardInterrupt:
            log.info("Shutting down")
            break
        except Exception as e:
            log.error("Error: %s", e)
            time.sleep(1.0)

    return 0

if __name__ == "__main__":
    sys.exit(main())
