"""NOEMA Neutrino Phase Channel daemon — 8×3 PMNS flavor mixing na HTRI bus.

Uruchamia cykliczne obliczenia neutrino phase bus:
  φ → ε : faza oscylatorów → kąt mieszania PMNS
  D_f → Λ : wymiar fraktalny → kosmologiczna stała D_cosmological
  τ ↔ φ : sprzężenie closure tau z fazą docelową
  HTRI bus : 8 kanałów × 3 smaki jako medium komunikacyjne

Usage:
    python scripts/ciel_noema_neutrino_daemon.py [--interval SEC]
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
import logging
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.neutrino_phase_channel import (
    neutrino_bus_snapshot,
    apply_neutrino_bus_to_surface,
    compute_neutrino_phase_bus,
    D_f_to_lambda,
)
from ciel_geometry.noema_registry import registry
from ciel_geometry.noema_surface_mmap import (
    ensure_surface,
    open_surface,
    flush_surface,
)

logging.basicConfig(
    level=logging.INFO,
    format="[neutrino] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Orbital manifest path for reading D_f
ORBITAL_MANIFEST = ROOT / "integration" / "Orbital" / "main" / "manifests" / "sectors_global.json"
ORBITAL_REPORT_DIR = ROOT / "integration" / "reports" / "global_orbital_coherence_pass"

def _read_D_f(surface: dict | None = None) -> float:
    """Odczytuje D_f z powierzchni (flavor[5]) lub manifestu."""
    if surface is not None:
        try:
            flavor = np.asarray(surface["flavor"], dtype=np.float64)
            D_f = float(flavor[5])
            if 1.5 <= D_f <= 3.0:
                return D_f
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_neutrino_daemon.py:64 quiet except scope=_read_D_f reason=pass")
            pass
    try:
        if ORBITAL_MANIFEST.exists():
            import json
            doc = json.loads(ORBITAL_MANIFEST.read_text(encoding="utf-8"))
            meta = doc.get("metadata", {})
            D_f = meta.get("D_f", 2.57)
            return float(D_f)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_neutrino_daemon.py:73 quiet except scope=_read_D_f reason=pass")
        pass
    return 2.57

def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Neutrino Phase Channel daemon")
    parser.add_argument("--interval", type=float, default=2.0, help="Neutrino bus cycle interval (default: 2.0s)")
    args = parser.parse_args()

    log.info("Starting Neutrino Phase Channel daemon (interval=%.1fs)", args.interval)

    surface = ensure_surface()
    log.info("Surface OK: tick=%s, phi_mean=%.4f", surface["tick"][0], surface["phi"].mean())

    reg_token = registry.register("neutrino")

    import signal
    _running = True
    def _stop(signum, frame):
        nonlocal _running
        _running = False
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    cycle = 0
    last_report = time.monotonic()
    try:
        while _running:
            try:
                D_f = _read_D_f(surface)
                bus = neutrino_bus_snapshot(surface, D_f=D_f)

                # Apply bus result to surface (Kuramoto owns flavor[4] — neutrino writes to bus only)
                apply_neutrino_bus_to_surface(surface, bus, D_f=D_f, write_flavor=False, write_g=True)

                # Seed PMNS mixing matrix into intra-channel 3×3 blocks
                # Tworzy właściwą strukturę PMNS w g matrix → epsilon > 0
                g_view = np.asarray(surface["g"], dtype=np.float64)
                from ciel_geometry.noema_surface_mmap import seed_neutrino_mixing
                seed_neutrino_mixing(g_view, scale=float(surface["flavor"][4]) * 0.3)

                flush_surface(surface)

                cycle += 1
                registry.heartbeat(reg_token)
                now = time.monotonic()
                if now - last_report >= 5.0:
                    log.info(
                        "cycle=%d  D_f=%.3f  Λ=%.4f  bus_capacity=%.4f  flavor[4]=%.4f  flavor[5]=%.4f",
                        cycle, D_f,
                        bus.get("global_D", 0),
                        bus.get("bus_capacity", 0),
                        float(surface["flavor"][4]),
                        float(surface["flavor"][5]),
                    )
                    # Best channel
                    channels = bus.get("channels", {})
                    if channels:
                        best_ch = max(channels, key=lambda k: channels[k].get("epsilon", 0))
                        best_eps = channels[best_ch].get("epsilon", 0)
                        log.info("  best channel: %s  ε=%.4f  prob_sem_nl=%.4f",
                                 best_ch, best_eps,
                                 channels[best_ch].get("semantic_to_nonlocal", {}).get("prob", 0))
                    last_report = now
            except Exception as e:
                log.error("Neutrino bus error: %s", e)
                import traceback
                traceback.print_exc()
                time.sleep(1)
            time.sleep(args.interval)
    finally:
        registry.unregister(reg_token)
        log.info("Unregistered from NOEMA registry")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
