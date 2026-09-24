"""NOEMA Full Diagnostic — harmonic fingerprints, Euler gap, CPS vs Euler, subconscious correlation.

Demonstrates the full capability of the integrated system:
  1. Harmonic fingerprint for all 33 operators
  2. Euler gap closure via operator composition
  3. CPS vs discrete Euler comparison
  4. δΦ vs Zeta entropy correlation
  5. Live surface probe (if /dev/shm/ciel_noema exists)

All vectorized — runs in <0.5s for the full diagnostic.
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.phasenav.operator_algebra import ALL_OPERATOR_IDS, operator_signature
from ciel_geometry.noema_surface_mmap import (
    N_OSCILLATORS, HARMONIC_VALUES, HARMONIC_AMPS,
    HARMONIC_MASK, N_HARMONICS, BASE_TEMPORAL_HZ,
    evolve_surface, evolve_surface_cps,
)
from ciel_geometry.subconscious import Subconscious


def _make_surface(seed: int = 42) -> dict:
    """Create a synthetic surface dict for testing."""
    rng = np.random.default_rng(seed)
    phi = rng.uniform(0, 2 * math.pi, N_OSCILLATORS).astype(np.float64)
    omega = np.full(N_OSCILLATORS, BASE_TEMPORAL_HZ, dtype=np.float64)
    g = np.zeros((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64)
    np.fill_diagonal(g, 0.5)
    np.fill_diagonal(g[3:], 0.3)
    g[0, 1] = g[1, 0] = 0.2
    g[3, 4] = g[4, 3] = 0.2
    flavor = np.array([0.3, 0.7, 0.5, 0.6, 0.4, 0.5], dtype=np.float64)
    gravity = np.zeros(4, dtype=np.float64)
    holonomy = np.zeros(7, dtype=np.float64)
    tick = np.array([0], dtype=np.uint64)
    Z_geom = np.cos(phi).astype(np.float64)
    R_geom = np.array([0.0], dtype=np.float64)
    psi_geom = np.array([0.0], dtype=np.float64)
    return {
        "phi": phi, "omega": omega, "g": g, "flavor": flavor,
        "tick": tick, "Z_geom": Z_geom, "R_geom": R_geom, "psi_geom": psi_geom,
        "gravity": gravity, "holonomy": holonomy,
    }


def harmonic_fingerprints() -> None:
    """1. Compute harmonic fingerprint (R₁,R₃,R₆,R₉) for all 33 operators."""
    print("=" * 72)
    print("1. HARMONIC FINGERPRINTS — ALL 33 OPERATORS")
    print("=" * 72)
    surface = _make_surface()
    phi = surface["phi"].copy()
    fingerprints: dict[str, dict[str, float]] = {}
    for op_id in ALL_OPERATOR_IDS:
        vec = operator_signature(op_id)
        phi_seeded = phi.copy()
        target = (vec[:N_OSCILLATORS] * 2 * math.pi) % (2 * math.pi)
        phi_seeded += 0.3 * np.angle(np.exp(1j * (target - phi_seeded)))
        phi_seeded %= 2 * math.pi

        R_h: dict[str, float] = {}
        for h_idx, h in enumerate(HARMONIC_VALUES):
            mask = HARMONIC_MASK[:, h_idx]
            if mask.any():
                R_h[f"R_{h}"] = float(abs(np.mean(np.exp(1j * h * phi_seeded[mask]))))
        fingerprints[op_id] = R_h

    # Print as table
    print(f"  {'Operator':24s}  {'R1':>6s}  {'R3':>6s}  {'R6':>6s}  {'R9':>6s}  {'signature':16s}")
    print("  " + "-" * 72)
    top_by_r9 = sorted(fingerprints.items(), key=lambda x: x[1].get("R_9", 0), reverse=True)
    for op_id, Rh in top_by_r9:
        sig_pattern = "".join(
            "H" if Rh.get(f"R_{h}", 0) > 0.25 else "L" for h in [1, 3, 6, 9]
        )
        print(f"  {op_id:24s}  {Rh.get('R_1',0):6.3f}  {Rh.get('R_3',0):6.3f}  {Rh.get('R_6',0):6.3f}  {Rh.get('R_9',0):6.3f}  {sig_pattern:16s}")
    return fingerprints


def euler_gap_solver() -> None:
    """2. Find operator sequence that best closes Euler gap."""
    print()
    print("=" * 72)
    print("2. EULER GAP SOLVER — OPERATOR PATH TO Σe^{iφ} → 0")
    print("=" * 72)
    surface = _make_surface()
    phi = surface["phi"].copy()

    S = np.sum(np.exp(1j * phi))
    euler_gap = float(abs(S))
    print(f"  Initial: |Σe^{{iφ}}| = {euler_gap:.4f}  (target: 0)")

    # Compute which operator rotation best cancels the Euler sum
    best_op = None
    best_gap = euler_gap
    best_phi = phi.copy()
    path: list[tuple[str, float]] = []

    for step in range(5):
        best_op_step = None
        best_gap_step = euler_gap

        for op_id in ALL_OPERATOR_IDS:
            vec = operator_signature(op_id)
            phi_candidate = phi.copy()
            target = (vec[:N_OSCILLATORS] * 2 * math.pi) % (2 * math.pi)
            phi_candidate += 0.2 * np.angle(np.exp(1j * (target - phi_candidate)))
            phi_candidate %= 2 * math.pi
            S_candidate = np.sum(np.exp(1j * phi_candidate))
            gap = float(abs(S_candidate))
            if gap < best_gap_step:
                best_gap_step = gap
                best_op_step = op_id

        if best_op_step is None or best_gap_step >= euler_gap:
            break

        vec = operator_signature(best_op_step)
        target = (vec[:N_OSCILLATORS] * 2 * math.pi) % (2 * math.pi)
        phi += 0.2 * np.angle(np.exp(1j * (target - phi)))
        phi %= 2 * math.pi
        S = np.sum(np.exp(1j * phi))
        euler_gap = float(abs(S))
        path.append((best_op_step, euler_gap))

        if euler_gap < 0.5:
            break

    print(f"  Path ({len(path)} ops):")
    for i, (op, gap) in enumerate(path):
        print(f"    {i+1}. {op:24s}  |Σ| → {gap:.4f}")
    if path:
        closure_pct = (1 - path[-1][1] / (path[0][1] if path else 1)) * 100
        print(f"  Euler closure: {closure_pct:.1f}%")
    else:
        print("  No operator path found (single-step insufficient)")
        print(f"  Best single operator would close {((1 - best_gap / euler_gap) * 100):.1f}%")


def cps_vs_euler_comparison() -> None:
    """3. Compare CPS evolution vs discrete Euler."""
    print()
    print("=" * 72)
    print("3. CPS vs DISCRETE EULER — 500 steps comparison")
    print("=" * 72)

    # Euler
    surf_e = _make_surface()
    t0 = time.perf_counter_ns()
    euler_δΦ = []
    for _ in range(500):
        δ = evolve_surface(surf_e, dt=0.01, flush=False)
        euler_δΦ.append(δ)
    euler_ns = time.perf_counter_ns() - t0
    euler_R = float(abs(np.mean(np.exp(1j * surf_e["phi"]))))

    # CPS
    surf_c = _make_surface()
    t0 = time.perf_counter_ns()
    cps_results = []
    for _ in range(500):
        res = evolve_surface_cps(surf_c, dt=0.01, flush=False)
        cps_results.append(res)
    cps_ns = time.perf_counter_ns() - t0
    cps_R = float(abs(np.mean(np.exp(1j * surf_c["phi"]))))

    euler_us = euler_ns / 500 / 1000
    cps_us = cps_ns / 500 / 1000

    print(f"  {'Method':15s}  {'Time/step':>12s}  {'Final R':>8s}  {'Mean δΦ':>10s}")
    print(f"  {'─'*15}  {'─'*12}  {'─'*8}  {'─'*10}")
    print(f"  {'Discrete Euler':15s}  {euler_us:8.1f}µs  {euler_R:8.4f}  {np.mean(euler_δΦ):10.4f}")
    print(f"  {'CPS+Euler':15s}  {cps_us:8.1f}µs  {cps_R:8.4f}  {np.mean([r['thinking_delta'] for r in cps_results]):10.4f}")

    speedup = euler_us / cps_us if cps_us > 0 else float("inf")
    print(f"  Speedup: {speedup:.1f}×")

    # Show final harmonic state from CPS
    last = cps_results[-1]
    print(f"  CPS final Z: R₁={last['R_1']:.4f} R₃={last['R_3']:.4f} R₆={last['R_6']:.4f} R₉={last['R_9']:.4f}")
    print(f"  Euler gap: {last['euler_gap']:.4f}")


def delta_vs_entropy() -> None:
    """4. δΦ vs Zeta entropy correlation."""
    print()
    print("=" * 72)
    print("4. δΦ vs ZETA ENTROPY — 1000-step correlation")
    print("=" * 72)

    sc = Subconscious()
    surf = _make_surface()
    delta_vals: list[float] = []
    entropy_vals: list[float] = []
    berry_vals: list[float] = []

    for step in range(1000):
        if step % 100 == 0:
            res = evolve_surface_cps(surf, dt=0.01, flush=False)
        else:
            res = evolve_surface_cps(surf, dt=0.01, flush=False)

        sub = sc.step_all(surf["phi"], dt=0.01)
        delta_vals.append(res["thinking_delta"])
        entropy_vals.append(sub["zet_collatz_entropy"])
        berry_vals.append(sub["berry_phase"])

    # Pearson correlation
    d_arr = np.array(delta_vals)
    e_arr = np.array(entropy_vals)
    b_arr = np.array(berry_vals)

    def pearson(x: np.ndarray, y: np.ndarray) -> float:
        xm, ym = x - x.mean(), y - y.mean()
        r = (xm @ ym) / (np.linalg.norm(xm) * np.linalg.norm(ym) + 1e-12)
        return float(r)

    r_de = pearson(d_arr, e_arr)
    r_db = pearson(d_arr, b_arr)
    r_eb = pearson(e_arr, b_arr)

    print(f"  Correlation matrix (Pearson r):")
    print(f"    δΦ × Zeta entropy:   r = {r_de:+.4f}")
    print(f"    δΦ × Berry phase:    r = {r_db:+.4f}")
    print(f"    Zeta entropy × Berry: r = {r_eb:+.4f}")
    print(f"  δΦ range: [{d_arr.min():.4f}, {d_arr.max():.4f}]  mean={d_arr.mean():.4f}")
    print(f"  H range:  [{e_arr.min():.4f}, {e_arr.max():.4f}]  mean={e_arr.mean():.4f}")
    print(f"  γ range:  [{b_arr.min():.4f}, {b_arr.max():.4f}]  mean={b_arr.mean():.4f}")


def live_surface_probe() -> None:
    """5. Probe live /dev/shm/ciel_noema if available."""
    shm_path = Path("/dev/shm/ciel_noema")
    if not shm_path.exists():
        print()
        print("=" * 72)
        print("5. LIVE SURFACE: not available (/dev/shm/ciel_noema not found)")
        print("=" * 72)
        return

    print()
    print("=" * 72)
    print("5. LIVE SURFACE PROBE — /dev/shm/ciel_noema")
    print("=" * 72)
    try:
        from ciel_geometry.noema_surface_mmap import open_surface, read_surface_state
        surface = open_surface(shm_path)
        state = read_surface_state(surface)
        phi = surface["phi"][...]

        R = float(abs(np.mean(np.exp(1j * phi))))
        S_comp = np.zeros(N_OSCILLATORS, dtype=np.complex128)
        for h_idx, h in enumerate(HARMONIC_VALUES):
            mask = HARMONIC_MASK[:, h_idx]
            if mask.any():
                S_comp[mask] += HARMONIC_AMPS[h_idx] * np.exp(1j * h * phi[mask])
        Phi_eff = np.angle(S_comp)
        δΦ = float(np.mean(np.abs(np.angle(np.exp(1j * (Phi_eff - phi))))))
        R_h = {h: float(abs(np.mean(np.exp(1j * h * phi[HARMONIC_MASK[:, h_idx]]))))
               for h_idx, h in enumerate(HARMONIC_VALUES) if HARMONIC_MASK[:, h_idx].any()}

        print(f"  tick={state['noema_tick']}  R={R:.4f}  δΦ={δΦ:.4f}  mood={state['mood']:.3f}  cp={state['closure_penalty']:.3f}")
        print(f"  R₁={R_h.get(1,0):.4f}  R₃={R_h.get(3,0):.4f}  R₆={R_h.get(6,0):.4f}  R₉={R_h.get(9,0):.4f}")

        # Quick CPS evolution on live state
        res = evolve_surface_cps(surface, dt=0.01, flush=False)
        print(f"  CPS: R₁→{res['R_1']:.4f}  R₃→{res['R_3']:.4f}  R₆→{res['R_6']:.4f}  R₉→{res['R_9']:.4f}")
        print(f"  |Σ|={res['euler_gap']:.4f}  δΦ→{res['thinking_delta']:.4f}")
    except Exception as e:
        print(f"  Error probing live surface: {e}")


def main() -> int:
    fingerprints = harmonic_fingerprints()
    euler_gap_solver()
    cps_vs_euler_comparison()
    delta_vs_entropy()
    live_surface_probe()

    print()
    print("=" * 72)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
