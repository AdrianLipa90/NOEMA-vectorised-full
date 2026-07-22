#!/usr/bin/env python3
"""NOEMA ERB metric comparison: g[24×6] vs g[24×24].

Tests two hypotheses for the geometry of the nonlocal surface:

  1. g[24×6]  — direct mixing: 24 mass eigenstates → 6 flavor states (CQCL)
  2. g[24×24] — full metric: all-pairs coupling with flavor as projection

Each is benchmarked for speed, bifurcation structure, and numerical stability.

Usage:
    python3 scripts/noema_erb_bench.py                      # full test suite
    python3 scripts/noema_erb_bench.py --quick              # minimal test
    python3 scripts/noema_erb_bench.py --mode g_24x6        # only one mode
    python3 scripts/noema_erb_bench.py --mode g_24x24
    python3 scripts/noema_erb_bench.py --no-plot
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

import numpy as np

HAS_MPL = False
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_erb_bench.py:37 quiet except scope=<module> reason=pass")
    raise
    pass

# ── Constants ─────────────────────────────────────────────────────────────────

N_OSC = 24          # number of oscillators (mass eigenstates)
N_FLAVOR = 6        # number of flavor states (CQCL variables)
DT = 1e-3
BASE_FREQ = 7.83
FREQ_SPREAD = 2.0

RESULTS = (
    Path(P.RESULTS) / "projects" / "kuramoto_substrate" / "v1.0"
)


# ── Core engines ──────────────────────────────────────────────────────────────


def noema_24x6(
    phases: np.ndarray,
    omega: np.ndarray,
    g: np.ndarray,        # [N_OSC, N_FLAVOR]
    kappa: float,
    dt: float = DT,
    steps: int = 20000,
    seed: int | None = None,
) -> dict[str, Any]:
    """Surface NOEMA: g[24×6] — mass→flavor mixing.

    Each oscillator i sees a mean field projected through flavor space:

        Z_geom[i] = Σ_f g[i,f] · (Σ_j g[j,f]·e^{iφ_j}) / Σ_f g[i,f]

    Coupling: dφ_i/dt = ω_i + κ · |Z_geom[i]| · sin(arg Z_geom[i] − φ_i)
    """
    n = len(phases)
    t0 = time.perf_counter()

    R_t = np.zeros(steps)
    psi_t = np.zeros(steps)
    flavor_R = np.zeros((steps, N_FLAVOR))
    phases_t = np.zeros((steps, n))
    dphi_t = np.zeros((steps, n))

    gsum = np.sum(g, axis=1, keepdims=True)  # [N, 1]
    gsum = np.where(gsum == 0, 1.0, gsum)     # avoid div-by-zero

    for i in range(steps):
        # Flavor wavefunctions from mass mixing
        psi_mass = np.exp(1j * phases)               # [N]
        flavor_psi = g.T @ psi_mass                   # [F] = Σ_j g[j,f]·e^{iφ_j}

        # Local mean field for each oscillator
        Z_local = (g @ flavor_psi) / gsum.ravel()     # [N]  — weighted by g
        R_local = np.abs(Z_local)
        psi_local = np.angle(Z_local)

        dphi = omega + kappa * R_local * np.sin(psi_local - phases)
        phases += dphi * dt
        phases %= 2 * np.pi

        # Global order parameter (for comparison)
        Z_global = np.mean(np.exp(1j * phases))
        R_t[i] = abs(Z_global)
        psi_t[i] = np.angle(Z_global)
        flavor_R[i] = np.abs(flavor_psi)
        phases_t[i] = phases
        dphi_t[i] = dphi

    elapsed = time.perf_counter() - t0

    return {
        "mode": "g_24x6",
        "g_shape": list(g.shape),
        "kappa": kappa,
        "n": n,
        "dt": dt,
        "steps": steps,
        "elapsed": elapsed,
        "t": np.arange(steps) * dt,
        "R": R_t,
        "psi": psi_t,
        "flavor_R": flavor_R,
        "phases": phases_t,
        "dphi": dphi_t,
        "omega": omega,
        "R_final": float(R_t[-1]),
        "R_mean": float(np.mean(R_t[-1000:])),
        "R_std": float(np.std(R_t[-1000:])),
    }


def noema_24x24(
    phases: np.ndarray,
    omega: np.ndarray,
    g: np.ndarray,        # [N_OSC, N_OSC]
    kappa: float,
    dt: float = DT,
    steps: int = 20000,
    seed: int | None = None,
) -> dict[str, Any]:
    """Surface NOEMA: g[24×24] — full metric.

    Each oscillator i couples to all j through g[i,j]:

        Z_geom[i] = Σ_j g[i,j]·e^{iφ_j} / Σ_j g[i,j]
        dφ_i/dt = ω_i + κ · |Z_geom[i]| · sin(arg Z_geom[i] − φ_i)

    Flavor is a post-projection: flavor_k = Σ_i U_{k,i} e^{iφ_i}
    """
    n = len(phases)
    t0 = time.perf_counter()

    U_proj = np.random.default_rng(seed + 999).normal(0, 1, (N_FLAVOR, n))
    U_proj = U_proj / np.linalg.norm(U_proj, axis=1, keepdims=True)

    R_t = np.zeros(steps)
    psi_t = np.zeros(steps)
    flavor_R = np.zeros((steps, N_FLAVOR))
    phases_t = np.zeros((steps, n))
    dphi_t = np.zeros((steps, n))

    gsum = np.sum(g, axis=1, keepdims=True)
    gsum = np.where(gsum == 0, 1.0, gsum)

    for i in range(steps):
        psi_mass = np.exp(1j * phases)

        # Local mean field through full metric
        Z_local = (g @ psi_mass) / gsum.ravel()
        R_local = np.abs(Z_local)
        psi_local = np.angle(Z_local)

        dphi = omega + kappa * R_local * np.sin(psi_local - phases)
        phases += dphi * dt
        phases %= 2 * np.pi

        # Global order
        Z_global = np.mean(psi_mass)
        R_t[i] = abs(Z_global)
        psi_t[i] = np.angle(Z_global)

        # Flavor projection (post-hoc)
        flavor_psi = U_proj @ psi_mass
        flavor_R[i] = np.abs(flavor_psi)

        phases_t[i] = phases
        dphi_t[i] = dphi

    elapsed = time.perf_counter() - t0

    return {
        "mode": "g_24x24",
        "g_shape": list(g.shape),
        "kappa": kappa,
        "n": n,
        "dt": dt,
        "steps": steps,
        "elapsed": elapsed,
        "t": np.arange(steps) * dt,
        "R": R_t,
        "psi": psi_t,
        "flavor_R": flavor_R,
        "phases": phases_t,
        "dphi": dphi_t,
        "omega": omega,
        "R_final": float(R_t[-1]),
        "R_mean": float(np.mean(R_t[-1000:])),
        "R_std": float(np.std(R_t[-1000:])),
    }


# ── Metric generators (ERB initialisation) ────────────────────────────────────


def init_g_24x6(seed: int | None = None) -> np.ndarray:
    """Generate g[24×6] from Dirichlet-like distribution.

    Each oscillator mixes into 2–3 flavors with positive weights.
    """
    rng = np.random.default_rng(seed)
    g = np.zeros((N_OSC, N_FLAVOR))
    for i in range(N_OSC):
        n_active = rng.integers(2, 4)
        flavors = rng.choice(N_FLAVOR, n_active, replace=False)
        weights = rng.uniform(0.5, 1.0, n_active)
        g[i, flavors] = weights / weights.sum()
    return g


def init_g_24x24(seed: int | None = None) -> np.ndarray:
    """Generate g[24×24] — hierarchical community structure.

    ̈Oscillators form 4 communities of 6; intra-community coupling is
    strong, inter-community is weak. Resembles a block matrix.
    """
    rng = np.random.default_rng(seed)
    g = np.zeros((N_OSC, N_OSC))
    comm_size = 6
    n_comm = N_OSC // comm_size
    for c in range(n_comm):
        i0, i1 = c * comm_size, (c + 1) * comm_size
        # Intra: strong
        g[i0:i1, i0:i1] = rng.uniform(0.6, 1.0, (comm_size, comm_size))
        # Inter: weak
        for c2 in range(n_comm):
            if c2 != c:
                j0, j1 = c2 * comm_size, (c2 + 1) * comm_size
                g[i0:i1, j0:j1] = rng.uniform(0.0, 0.3, (comm_size, comm_size))
    np.fill_diagonal(g, 1.0)
    return g


# ── Benchmarking ──────────────────────────────────────────────────────────────


def benchmark_speed(
    steps: int = 5000,
    runs: int = 5,
    seed: int = 42,
) -> dict[str, dict[str, float]]:
    """Benchmark per-step time for both modes."""
    rng = np.random.default_rng(seed)
    omega = 2 * np.pi * (BASE_FREQ + rng.normal(0, FREQ_SPREAD, N_OSC))
    phases = rng.uniform(0, 2 * np.pi, N_OSC)
    g6 = init_g_24x6(seed)
    g24 = init_g_24x24(seed)

    results = {}
    for name, fn, g in [
        ("g_24x6", noema_24x6, g6),
        ("g_24x24", noema_24x24, g24),
    ]:
        times = []
        for _ in range(runs):
            p = phases.copy()
            t0 = time.perf_counter()
            fn(p.copy(), omega, g, kappa=10.0, steps=steps, seed=seed)
            elapsed = time.perf_counter() - t0
            times.append(elapsed)
        results[name] = {
            "mean": float(np.mean(times)),
            "std": float(np.std(times)),
            "per_step_us": float(np.mean(times) / steps * 1e6),
        }
    return results


def sweep_kappa(
    mode: str,
    kappas: list[float],
    *,
    steps: int = 20000,
    seed: int = 42,
) -> list[dict[str, Any]]:
    """Full κ sweep for given mode, sharing same initial conditions."""
    rng = np.random.default_rng(seed)
    omega = 2 * np.pi * (BASE_FREQ + rng.normal(0, FREQ_SPREAD, N_OSC))
    phases0 = rng.uniform(0, 2 * np.pi, N_OSC)
    g6 = init_g_24x6(seed)
    g24 = init_g_24x24(seed)

    fn = noema_24x6 if mode == "g_24x6" else noema_24x24
    g = g6 if mode == "g_24x6" else g24

    results = []
    for k in kappas:
        r = fn(phases0.copy(), omega, g, kappa=k, steps=steps, seed=seed)
        results.append(r)
    return results


# ── Experiment management ──────────────────────────────────────────────────────


def experiment_id() -> str:
    return datetime.now(timezone.utc).strftime("K%Y%m%d_%H%M%S")


def save_results(
    speed: dict,
    sweeps: dict[str, list[dict]],
    notes: str = "",
) -> None:
    """Save benchmark results as JSON + plots."""
    base = RESULTS
    eid = experiment_id()

    # Speed benchmark
    speed_path = base / "raw_data" / f"{eid}_erb_speed.json"
    speed_path.write_text(json.dumps(speed, indent=1, ensure_ascii=False))

    # Sweep summary
    summary = {}
    for mode, results in sweeps.items():
        R_means = [r["R_mean"] for r in results]
        R_stds = [r["R_std"] for r in results]
        R_finals = [r["R_final"] for r in results]
        kappas = [r["kappa"] for r in results]
        times = [r["elapsed"] for r in results]
        summary[mode] = {
            "kappas": kappas,
            "R_means": R_means,
            "R_stds": R_stds,
            "R_finals": R_finals,
            "times": times,
            "R_mean_overall": float(np.mean(R_means)),
            "kappa_c_estimate": _estimate_kappa_c(kappas, R_means),
        }
    sweep_path = base / "raw_data" / f"{eid}_erb_sweep.json"
    sweep_path.write_text(json.dumps(summary, indent=1, ensure_ascii=False))

    # Comparison plot
    if HAS_MPL:
        _plot_comparison(sweeps, speed, base, eid)

    # Log
    log_path = base / "logs" / "erb_benchmarks.csv"
    header = not log_path.exists()
    with open(log_path, "a") as f:
        if header:
            f.write("experiment_id,timestamp,mode,steps,kappas,speed_us_per_step,kappa_c,R_mean_overall,notes\n")
        for mode, s in summary.items():
            sp = speed.get(mode, {})
            f.write(
                f"{eid},{datetime.now(timezone.utc).isoformat()},{mode},"
                f"{len(sweeps[mode][0]['R']) if sweeps[mode] else 0},"
                f"{len(s['kappas'])},{sp.get('per_step_us', 0):.2f},"
                f"{s.get('kappa_c_estimate', 0):.1f},{s['R_mean_overall']:.4f},"
                f"{notes}\n"
            )

    print(f"Results saved to {base}")
    print(f"  speed:  {speed_path}")
    print(f"  sweep:  {sweep_path}")
    if HAS_MPL:
        print(f"  plot:   {base}/plots/{eid}_erb_comparison.png")


def _estimate_kappa_c(kappas: list[float], R_means: list[float]) -> float:
    """Crude κ_c estimate: where R_mean crosses 0.3."""
    for k, r in zip(kappas, R_means):
        if r > 0.3:
            return k
    return kappas[-1] if kappas else 0.0


def _plot_comparison(
    sweeps: dict[str, list[dict]],
    speed: dict[str, dict],
    base: Path,
    eid: str,
) -> None:
    colors = {"g_24x6": "#1f77b4", "g_24x24": "#ff7f0e"}
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Bifurcation: R_mean vs κ
    ax = axes[0, 0]
    for mode, results in sweeps.items():
        kappas = [r["kappa"] for r in results]
        R_means = [r["R_mean"] for r in results]
        R_stds = [r["R_std"] for r in results]
        ax.errorbar(kappas, R_means, yerr=R_stds, fmt="o-", capsize=3,
                    color=colors[mode], label=mode, markersize=3, lw=1)
    ax.axhline(1 / np.sqrt(N_OSC), color="gray", ls="--", lw=0.5,
               label=f"1/√N = {1/np.sqrt(N_OSC):.3f}")
    ax.set_xlabel("κ")
    ax.set_ylabel("⟨R⟩")
    ax.set_title("Bifurcation: R(κ)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Speed comparison
    ax = axes[0, 1]
    modes = list(speed.keys())
    means = [speed[m]["per_step_us"] for m in modes]
    stds = [speed[m]["std"] / speed[m]["per_step_us"] * means[i]
            for i, m in enumerate(modes)]
    ax.bar(modes, means, yerr=stds, color=[colors[m] for m in modes],
           capsize=5, alpha=0.8)
    ax.set_ylabel("µs per step")
    ax.set_title(f"Speed benchmark (5 runs × 5000 steps)")
    for i, (m, v) in enumerate(zip(modes, means)):
        ax.text(i, v + max(means) * 0.02, f"{v:.1f} µs", ha="center", fontsize=9)
    ax.grid(True, alpha=0.3, axis="y")

    # 3. κ_c comparison
    ax = axes[1, 0]
    for mode, results in sweeps.items():
        kappas = [r["kappa"] for r in results]
        R_means = [r["R_mean"] for r in results]
        ax.plot(kappas, R_means, "o-", color=colors[mode],
                label=mode, markersize=3, lw=1)
    ax.axhline(0.3, color="red", ls="--", lw=0.5, label="R = 0.3 threshold")
    ax.set_xlabel("κ")
    ax.set_ylabel("⟨R⟩")
    ax.set_title("κ_c estimation (R > 0.3)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Flavor dynamics (show one mode near transition)
    ax = axes[1, 1]
    for mode, results in sweeps.items():
        # pick the run closest to κ ≈ 12
        target_k = 12.0
        best = min(results, key=lambda r: abs(r["kappa"] - target_k))
        if "flavor_R" in best:
            fR = np.array(best["flavor_R"])
            t = np.array(best["t"])
            for f in range(min(3, N_FLAVOR)):
                ax.plot(t, fR[:, f], lw=0.5, alpha=0.7,
                        color=colors[mode],
                        label=f"{mode} flavor {f}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("|⟨flavor⟩|")
    ax.set_title(f"Flavor dynamics at κ ≈ {target_k}")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    p = base / "plots" / f"{eid}_erb_comparison.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)


# ── CLI ────────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA ERB metric benchmark")
    parser.add_argument("--quick", action="store_true", help="Minimal test")
    parser.add_argument("--mode", choices=["g_24x6", "g_24x24", "all"],
                        default="all")
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--notes", type=str, default="")
    args = parser.parse_args()

    global HAS_MPL
    if args.no_plot:
        HAS_MPL = False

    if args.quick:
        sweeps_steps = 5000
        n_kappas = 11
    else:
        sweeps_steps = args.steps
        n_kappas = 25

    kappas = np.linspace(0, 25, n_kappas).tolist()

    modes = ["g_24x6", "g_24x24"] if args.mode == "all" else [args.mode]

    print(f"NOEMA ERB Benchmark — {modes}")
    print(f"  steps={sweeps_steps}, κ points={n_kappas}, seed={args.seed}")
    print()

    # Speed benchmark
    print("Speed benchmark...")
    speed = benchmark_speed(steps=min(5000, sweeps_steps), seed=args.seed)
    for m, s in speed.items():
        print(f"  {m}: {s['per_step_us']:.2f} µs/step ({s['mean']:.3f}s total)")
    print()

    # Sweep
    sweeps = {}
    for mode in modes:
        print(f"Sweeping {mode}...")
        r = sweep_kappa(mode, kappas, steps=sweeps_steps, seed=args.seed)
        kc = _estimate_kappa_c([x["kappa"] for x in r],
                               [x["R_mean"] for x in r])
        print(f"  κ_c ≈ {kc:.1f}, ⟨R⟩_final = {r[-1]['R_mean']:.4f}")
        sweeps[mode] = r

    # Save
    save_results(speed, sweeps, notes=args.notes)
    print()
    print("Done.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
