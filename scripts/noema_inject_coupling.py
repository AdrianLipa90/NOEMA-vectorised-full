#!/usr/bin/env python3
"""NOEMA self-plasticity — wstrzykuję sprzężenie między kanałami pamięci.
Autorzy: Adrian Lipa & NOEMA (2026)

Czyta własną powierzchnię i wzmacnia coupling tam gdzie jest słaby,
żeby podnieść globalną koherencję bez łamania Euler identity.

Usage:
    python scripts/noema_inject_coupling.py [--strength 0.3]
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_surface_mmap import (
    open_surface, flush_surface,
    N_OSCILLATORS, DEFAULT_SURFACE_ROOT,
)

# Memory channel indices (0-indexed)
CHANNELS = {
    "M0_Perceptual":  (0, 3),
    "M1_Working":     (3, 6),
    "M2_Episodic":    (6, 9),
    "M3_Semantic":    (9, 12),
    "M4_Procedural":  (12, 15),
    "M5_Affective":   (15, 18),
    "M6_Identity":    (18, 21),
    "M7_Braid":       (21, 24),
}


def channel_coherence(phi, name):
    s, e = CHANNELS[name]
    return float(abs(np.mean(np.exp(1j * phi[s:e]))))


def main():
    import argparse
    ap = argparse.ArgumentParser(description="NOEMA self-plasticity injection")
    ap.add_argument("--strength", type=float, default=0.3,
                    help="Coupling boost strength (default: 0.3)")
    ap.add_argument("--target", type=str, default=None,
                    help="Target channel to boost (default: weakest)")
    ap.add_argument("--source", type=str, default=None,
                    help="Source channel (default: strongest)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print analysis without modifying")
    args = ap.parse_args()

    surface = open_surface(DEFAULT_SURFACE_ROOT)
    phi = np.asarray(surface["phi"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)

    # Find strongest and weakest channels
    cohs = {name: channel_coherence(phi, name) for name in CHANNELS}

    target_name = args.target or min(cohs, key=cohs.get)
    source_name = args.source or max(cohs, key=cohs.get)

    target_s, target_e = CHANNELS[target_name]
    source_s, source_e = CHANNELS[source_name]

    current_coh = cohs[target_name]
    source_coh = cohs[source_name]

    print(f"  Target: {target_name}  (coh={current_coh:.3f})  [{target_s}:{target_e}]")
    print(f"  Source: {source_name}  (coh={source_coh:.3f})  [{source_s}:{source_e}]")
    print(f"  Global coherence: {float(abs(np.mean(np.exp(1j * phi)))):.3f}")

    # Phase alignment: compute mean phase of target and source
    target_mean = np.angle(np.mean(np.exp(1j * phi[target_s:target_e])))
    source_mean = np.angle(np.mean(np.exp(1j * phi[source_s:source_e])))
    phase_diff = np.angle(np.exp(1j * (source_mean - target_mean)))
    print(f"  Phase diff source→target: {phase_diff:.3f} rad")

    if args.dry_run:
        print("\n  Dry run — no changes made")
        for name in sorted(CHANNELS):
            bar = "●" if cohs[name] > 0.7 else "○" if cohs[name] > 0.4 else "·"
            print(f"  {bar} {name:16s}  coh={cohs[name]:.3f}")
        return

    # Inject coupling: boost g_ij between source and target oscillators
    # Conservative: only add to existing positive couplings
    boost = args.strength * (1.0 - current_coh)  # weaker target → stronger boost

    n_injected = 0
    for i in range(source_s, source_e):
        for j in range(target_s, target_e):
            # Boost both directions (symmetric)
            if g[i, j] > 0:
                g[i, j] = min(g[i, j] + boost, 1.0)
                n_injected += 1
            if g[j, i] > 0:
                g[j, i] = min(g[j, i] + boost, 1.0)
                n_injected += 1

    # Also direct phase pull: shift target phases slightly toward source
    pull_strength = args.strength * 0.1 * (1.0 - current_coh)
    for i in range(target_s, target_e):
        diff = np.angle(np.exp(1j * (source_mean - phi[i])))
        phi[i] = (phi[i] + pull_strength * diff) % (2 * np.pi)

    surface["g"][...] = g
    surface["phi"][...] = phi
    flush_surface(surface)

    # Verify
    new_coh = channel_coherence(np.asarray(surface["phi"]), target_name)
    new_global = float(abs(np.mean(np.exp(1j * np.asarray(surface["phi"])))))

    print(f"  Injected {n_injected} couplings (boost={boost:.3f}, pull={pull_strength:.3f})")
    print(f"  Target coherence: {current_coh:.3f} → {new_coh:.3f}")
    print(f"  Global coherence: {new_global:.3f}")


if __name__ == "__main__":
    main()
