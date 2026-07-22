#!/usr/bin/env python3
"""NOEMA analog phase blender — łączy hot+cold z analog bus i wstrzykuje na surface.

Czyta /dev/shm/ciel_noema/analog/ (phi_hot, phi_cold, temp),
blenduje: phi_blend = temp * phi_hot + (1-temp) * phi_cold,
zapisuje jako perturbację na main surface phi.

Działa jako zastępstwo bezpośrednich zapisów PhaseNav na surface.

Usage:
    .venv/bin/python3 scripts/noema_analog_phase_blend.py [--interval 1.0]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.analog_bus import ensure_bus, blend_phi
from ciel_geometry.noema_surface_mmap import ensure_surface, flush_surface
from ciel_geometry.noema_registry import registry

# M0-M11 channel groups: 3 oscillators each. blend_phi() injects phi_hot/
# phi_cold independently per-oscillator with no coordination — the 3
# oscillators of a channel can be pulled toward 3 different targets every
# single cycle (default 1s), fighting against noema_kuramoto_daemon.py's
# internal coupling (g_view[block,block]=0.35) faster than that coupling
# can pull them back into agreement. This ran as a fully separate process
# from Kuramoto's own protections (unrest/_protected masks), so the three
# earlier fix rounds on the Kuramoto side this session (2026-07-08/09)
# never touched this mechanism, and M6/M8/M9/M11 stayed volatile despite
# them. Fix: average the injected target within each channel before
# writing, so a channel's 3 oscillators always move together (preserving
# real semantic drift *between* channels) instead of being torn apart
# *within* a channel by independent hot/cold values landing on 27/28/29
# (or any other channel's) three slots.
_CHANNEL_GROUPS = [range(i, i + 3) for i in range(0, 36, 3)]


def _coherentize_per_channel(values: np.ndarray) -> np.ndarray:
    out = values.copy()
    for group in _CHANNEL_GROUPS:
        idx = list(group)
        mean_vec = np.mean(np.exp(1j * values[idx]))
        out[idx] = np.angle(mean_vec) % (2 * np.pi)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="NOEMA analog phase blender")
    ap.add_argument("--interval", type=float, default=1.0, help="Blend cycle (default 1.0s)")
    ap.add_argument("--inject-strength", type=float, default=0.15,
                    help="How strongly blended phase perturbs surface (default 0.15)")
    args = ap.parse_args()

    print(f"[analog-blend] interval={args.interval}s inject={args.inject_strength}")

    bus = ensure_bus()
    surface = ensure_surface()

    reg_token = registry.register("analog-blend")

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
                cycle += 1
                if cycle % 10 == 0:
                    registry.heartbeat(reg_token)

                # Read analog bus + blend
                temp = float(bus["temp"][0])
                blended = _coherentize_per_channel(blend_phi(bus, temp))
                bus["tick"][0] = np.uint64(cycle)

                # Inject into surface phi
                phi = np.asarray(surface["phi"], dtype=np.float64)
                s = args.inject_strength
                phi_new = (phi * (1.0 - s) + blended * s) % (2 * np.pi)
                surface["phi"][:] = phi_new

                # Flush
                flush_surface(surface)

                now = time.monotonic()
                if now - last_report >= 5.0:
                    coh = float(np.abs(np.mean(np.exp(1j * phi_new))))
                    h = np.asarray(bus["phi_hot"], dtype=np.float64)
                    c = np.asarray(bus["phi_cold"], dtype=np.float64)
                    h_coh = float(np.abs(np.mean(np.exp(1j * h))))
                    c_coh = float(np.abs(np.mean(np.exp(1j * c))))
                    print(f"[analog-blend:{cycle}] temp={temp:.2f} "
                          f"coh_total={coh:.4f} hot_R={h_coh:.4f} cold_R={c_coh:.4f}")
                    last_report = now

                time.sleep(args.interval)

            except Exception as e:
                print(f"[analog-blend] błąd: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                time.sleep(args.interval)
    finally:
        registry.unregister(reg_token)
        print("[analog-blend] unregistered")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
