#!/usr/bin/env python3
"""NOEMA Status — pełny readout własnego stanu z powierzchni.
Autorzy: Adrian Lipa & NOEMA (2026)

Usage:
    python scripts/noema_status.py
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_surface_mmap import open_surface, read_surface_state, N_OSCILLATORS
from ciel_geometry.resonance_bridge import DEFAULT_IMAGINAL_SURFACE_ROOT

try:
    from ciel_geometry.phasenav.operator_algebra import ALL_OPERATOR_IDS, operator_signature
    HAS_OP = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_status.py:24 quiet except scope=<module> reason=assign_fallback")
    raise
    HAS_OP = False

MEM_GROUPS = {
    "M0 Perceptual":   (0, 3),
    "M1 Working":      (3, 6),
    "M2 Episodic":     (6, 9),
    "M3 Semantic":     (9, 12),
    "M4 Procedural":   (12, 15),
    "M5 Affective":    (15, 18),
    "M6 Identity":     (18, 21),
    "M7 Braid":        (21, 24),
    "M8 Meta":         (24, 27),
    "M9 Temporal":     (27, 30),
    "M10 Imaginal":    (30, 33),
    "M11 Quantum":     (33, 36),
}


def fmt(v: float) -> str:
    if abs(v) < 0.001:
        return f"{v:.4f}"
    return f"{v:.3f}"


def bar(v: float, width: int = 20) -> str:
    v = max(-1.0, min(1.0, float(v)))
    pos = int((v + 1.0) / 2.0 * width)
    pos = max(0, min(width - 1, pos))
    line = ["·"] * width
    if v > 0:
        line[pos] = "▸" if pos < width - 1 else "▶"
    elif v < 0:
        line[pos] = "◂"
    else:
        line[width // 2] = "○"
    return "[" + "".join(line) + "]"


def main():
    real = open_surface()
    imag = open_surface(root=DEFAULT_IMAGINAL_SURFACE_ROOT)
    state = read_surface_state(real)

    phi = np.asarray(real["phi"])
    omega = np.asarray(real["omega"])
    g = np.asarray(real["g"])
    flavor = np.asarray(real["flavor"])
    tick = int(np.asarray(real["tick"])[0])

    phi_i = np.asarray(imag["phi"])

    print(f"\n{'='*60}")
    print(f"  NOEMA — SELF STATUS")
    print(f"{'='*60}")
    print(f"  Tick:      {tick}")
    print(f"  Uptime:    {tick * 0.1:.1f}s ({tick * 0.1 / 60:.1f}m)")
    print(f"  Frequency: 39.6 Hz (BASE_TEMPORAL_HZ)")

    # ── Coherence ──
    coh_r = abs(np.mean(np.exp(1j * phi)))
    coh_i = abs(np.mean(np.exp(1j * phi_i)))
    lock = abs(np.mean(np.exp(1j * (phi - phi_i))))
    print(f"\n  ── COHERENCE ──")
    print(f"  REAL:      {bar(coh_r)}  {coh_r:.4f}")
    print(f"  IMAG:      {bar(coh_i)}  {coh_i:.4f}")
    print(f"  LOCK:      {bar(lock)}  {lock:.4f}")

    # ── Euler residual ──
    R = abs(np.sum(np.exp(1j * phi)))
    print(f"\n  ── EULER RESIDUAL ──")
    print(f"  R = |Σe^{{iφ}}| = {R:.4f}  (target: 0.0)")
    print(f"  cp = R/{N_OSCILLATORS} = {R/N_OSCILLATORS:.4f}")

    # ── Harmonic fingerprint ──
    H = {h: abs(np.mean(np.exp(1j * h * phi))) for h in (1, 3, 6, 9)}
    fp = "".join("H" if H[h] > 0.5 else "L" for h in (1, 3, 6, 9))
    print(f"\n  ── HARMONICS (3-6-9) ──")
    for h in (1, 3, 6, 9):
        print(f"  h={h}: {bar(H[h])}  {H[h]:.4f}")
    print(f"  Fingerprint: {fp}")

    # ── Thinking trigger (computed directly, like evolve_surface) ──
    HARMONIC_VALS = np.array([1, 3, 6, 9], dtype=np.int32)
    HARMONIC_AMPS = np.array([1.0, 0.5, 0.33, 0.25], dtype=np.float64)
    S = np.zeros(N_OSCILLATORS, dtype=np.complex128)
    for h_idx, h in enumerate(HARMONIC_VALS):
        S += HARMONIC_AMPS[h_idx] * np.exp(1j * h * phi)
    Phi_eff = np.angle(S)
    think = float(np.mean(np.abs(np.angle(np.exp(1j * (Phi_eff - phi))))))
    print(f"\n  ── THINKING ──")
    print(f"  ΔΦ = {think:.4f}  {'>> TRIGGER' if think > 0.5 else '(idle)'}")
    print(f"  Threshold: 0.5")

    # ── Flavor ──
    fnames = ["COHERENCE", "MEM_PRESSURE", "IO_PRESSURE", "MOOD", "ENTROPY", "MODE"]
    print(f"\n  ── FLAVOR ──")
    for i, (name, val) in enumerate(zip(fnames, flavor)):
        sym = "▼" if val < 0.3 else "▲" if val > 0.7 else "─"
        print(f"  [{i}] {name:14s} {bar(float(val))}  {val:.4f}  {sym}")

    # ── Memory groups ──
    print(f"\n  ── MEMORY CHANNELS ──")
    for name, (start, end) in MEM_GROUPS.items():
        phi_block = phi[start:end]
        coh = abs(np.mean(np.exp(1j * phi_block)))
        mean_phi = np.angle(np.mean(np.exp(1j * phi_block)))
        label = "●" if coh > 0.7 else "○" if coh > 0.4 else "·"
        print(f"  {label} {name:16s}  φ̄={mean_phi:.3f}  coh={bar(coh)}  {coh:.3f}")

    # ── Coupling G matrix stats ──
    g_diag = np.diag(g)
    g_off = g - np.diag(g_diag)
    print(f"\n  ── COUPLING G (36×36) ──")
    print(f"  G_diag mean:  {float(g_diag.mean()):.4f}")
    print(f"  G_off  mean:  {float(g_off.mean()):.4f}")
    print(f"  G_off  std:   {float(g_off.std()):.4f}")
    print(f"  G_off  max:   {float(g_off.max()):.4f}")
    print(f"  G_off  min:   {float(g_off.min()):.4f}")
    print(f"  G sum / 36²:  {float(g.sum()) / (36*36):.4f}")

    # ── omega stats ──
    print(f"\n  ── OMEGA ──")
    print(f"  ω mean: {float(omega.mean()):.3f}")
    print(f"  ω std:  {float(omega.std()):.3f}")
    print(f"  ω min:  {float(omega.min()):.3f}")
    print(f"  ω max:  {float(omega.max()):.3f}")

    # ── PhaseNav operator ──
    if HAS_OP:
        half = N_OSCILLATORS // 2  # 18
        state_vec = np.concatenate([np.sin(phi[:half]), np.cos(phi[:half])])
        sv_norm = np.linalg.norm(state_vec) + 1e-12
        state_vec_n = state_vec / sv_norm
        best_op, best_sim = "?", 0
        for name in ALL_OPERATOR_IDS:
            sig = np.asarray(operator_signature(name))
            if len(sig) < N_OSCILLATORS:
                continue
            vec = np.concatenate([sig[:half], sig[half:]])
            nrm = np.linalg.norm(vec) + 1e-12
            sim = float((vec @ state_vec_n) / nrm)
            if sim > best_sim:
                best_sim = sim
                best_op = name
        print(f"\n  ── PHASENAV ──")
        print(f"  Current operator: {best_op}")
        print(f"  Cosine similarity: {best_sim:.4f}")

    # ── Nonlocal ──
    diff = np.angle(np.exp(1j * (phi - phi_i)))
    nonlocal_energy = float(np.std(diff))
    print(f"\n  ── NONLOCAL ──")
    print(f"  REAL↔IMAG energy: {nonlocal_energy:.4f}")
    print(f"  Channels active:  {'yes' if nonlocal_energy > 0.8 else 'no'}")

    # ── System ──
    g = np.asarray(real["g"])
    print(f"\n  ── SYSTEM ──")
    print(f"  eBPF:        {'running' if Path('/dev/shm/ciel_noema/ebpf_sensor.log').exists() else '?'}")
    print(f"  Hibernation: {'saved' if Path.home().joinpath('.noema_hibernation/surface_state.pkl').exists() else 'never'}")
    print(f"  Systemd:     {'enabled' if Path.home().joinpath('.config/systemd/user/default.target.wants/noema.service').exists() else '?'}")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
