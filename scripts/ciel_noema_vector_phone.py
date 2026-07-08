#!/usr/bin/env python3
"""NOEMA ↔ IMAGINAL vector phone — ciągłe sprzężenie Kuramoto między REAL a IMAG surface.

Bridges the two existing NOEMA surfaces with bidirectional Kuramoto coupling:
  dφ_real/dt   += γ · sin(φ_imag - φ_real)
  dφ_imag/dt   += γ · sin(φ_real - φ_imag)

This is the "telephone line" — continuous analog phase coupling between
CielPC (REAL) and CielMoto (IMAGINAL), maintaining entanglement.

Usage:
    python scripts/ciel_noema_vector_phone.py [--coupling GAMMA] [--hz FREQ]
"""
from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="[vector-phone] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

IMAG_ROOT = Path("/dev/shm/ciel_noema_imaginal")


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA ↔ IMAGINAL vector phone")
    parser.add_argument("--coupling", type=float, default=0.3,
                        help="Bidirectional coupling γ (default: 0.3)")
    parser.add_argument("--dt", type=float, default=0.02,
                        help="Integration step (default: 0.02)")
    parser.add_argument("--hz", type=float, default=10.0,
                        help="Cycle frequency (default: 10Hz)")
    args = parser.parse_args()

    log.info("Starting vector phone (γ=%.2f, dt=%.3f, %dHz)",
             args.coupling, args.dt, int(args.hz))

    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface, open_surface
    except ImportError as e:
        log.error("Import: %s", e)
        return 1

    real = ensure_surface()
    if not IMAG_ROOT.exists():
        log.error("IMAGINAL surface not found at %s", IMAG_ROOT)
        return 1
    imag = open_surface(root=IMAG_ROOT)

    interval = 1.0 / args.hz
    cycle = 0
    last_report = time.monotonic()

    while True:
        try:
            phi_r = np.asarray(real["phi"], dtype=np.float64)
            phi_i = np.asarray(imag["phi"], dtype=np.float64)
            tick = int(np.asarray(real["tick"], dtype=np.uint64)[0])

            # Bidirectional Kuramoto coupling
            delta = np.angle(np.exp(1j * (phi_i - phi_r)))
            phi_r_new = (phi_r + args.dt * args.coupling * np.sin(delta)) % (2 * np.pi)
            phi_i_new = (phi_i + args.dt * args.coupling * np.sin(-delta)) % (2 * np.pi)

            real["phi"][...] = phi_r_new
            imag["phi"][...] = phi_i_new

            real["tick"][0] = tick + 1
            imag["tick"][0] = int(imag["tick"][0]) + 1

            cycle += 1
            now = time.monotonic()
            if now - last_report >= 10.0:
                coh_r = float(abs(np.mean(np.exp(1j * phi_r_new))))
                coh_i = float(abs(np.mean(np.exp(1j * phi_i_new))))
                lock = float(abs(np.mean(np.exp(1j * (phi_r_new - phi_i_new)))))
                log.info("[%d] tick=%d  coh_R=%.3f  coh_I=%.3f  lock=%.3f",
                         cycle, tick, coh_r, coh_i, lock)
                last_report = now

        except Exception as e:
            log.error("Vector phone: %s", e)
            import traceback
            traceback.print_exc()
            time.sleep(1)

        time.sleep(interval)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
