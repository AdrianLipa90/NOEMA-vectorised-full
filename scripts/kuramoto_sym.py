#!/usr/bin/env python3
"""Kuramoto 24-oscillator simulation — CIEL experiment tracker.

Usage:
    python3 scripts/kuramoto_sym.py                    # default: sweep kappa
    python3 scripts/kuramoto_sym.py --mode sweep       # sweep kappa from 0.0 to 2.0
    python3 scripts/kuramoto_sym.py --mode single      # single run with given kappa
    python3 scripts/kuramoto_sym.py --kappa 1.5        # single run at kappa=1.5
    python3 scripts/kuramoto_sym.py --kappas 0.0 2.0   # sweep range
    python3 scripts/kuramoto_sym.py --steps 20000      # more steps
    python3 scripts/kuramoto_sym.py --no-plot          # skip plots (headless)
    python3 scripts/kuramoto_sym.py --archive          # force archive to experiment dir

Results go to ~//media/adrian/New Volume1/CIEL_memories/experiments/kuramoto_sym/ by default.
Each run gets a unique timestamped experiment ID.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

HAS_MPL = False
try:
    import matplotlib
    matplotlib.use("Agg")  # no display needed
    import matplotlib.pyplot as plt

    HAS_MPL = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/kuramoto_sym.py:38 quiet except scope=<module> reason=pass")
    pass

# ── Config ───────────────────────────────────────────────────────────────────

N_OSCILLATORS = 36
DT = 1e-3  # 1 ms → 1000 Hz simulation rate
BASE_FREQ = 7.83  # Schumann / alpha-theta EEG boundary
FREQ_SPREAD = 2.0  # standard deviation of intrinsic frequencies

EXPERIMENT_DIR = (
    Path(P.RESULTS)
    / "projects"
    / "kuramoto_substrate"
    / "v1.0"
)
EXPERIMENT_SUBDIRS = ["raw_data", "plots", "configs", "logs", "archive"]
GLOBAL_REGISTRY = Path(P.RESULTS) / "meta" / "global_experiments.csv"
PROJECT_ID = "kuramoto_substrate"

# ── Kuramoto core ─────────────────────────────────────────────────────────────


def intrinsic_frequencies(
    n: int = N_OSCILLATORS,
    base: float = BASE_FREQ,
    spread: float = FREQ_SPREAD,
    seed: int | None = None,
) -> np.ndarray:
    """Generate intrinsic frequencies ω_i around base frequency."""
    rng = np.random.default_rng(seed)
    return base + rng.normal(0, spread, n)


def run_kuramoto(
    kappa: float,
    *,
    n: int = N_OSCILLATORS,
    dt: float = DT,
    steps: int = 10000,
    omega: np.ndarray | None = None,
    seed: int | None = None,
) -> dict[str, Any]:
    """Run Kuramoto simulation for N oscillators.

    Returns dict with full time series: phases, R(t), Σ_i(t), dφ_i(t), ω, κ, ...
    """
    if omega is None:
        omega = intrinsic_frequencies(n, seed=seed)

    # Convert ω to angular velocity: ω_i = 2π * f_i
    omega_rad = 2 * np.pi * omega

    # Init phases uniformly random in [0, 2π)
    rng = np.random.default_rng(seed)
    phases = rng.uniform(0, 2 * np.pi, n)

    # Storage
    R_t = np.zeros(steps)
    psi_t = np.zeros(steps)
    phases_t = np.zeros((steps, n))
    windings_t = np.zeros((steps, n), dtype=np.int32)
    dphi_t = np.zeros((steps, n))
    t_t = np.arange(steps) * dt
    winding_count = np.zeros(n, dtype=np.int32)

    for i in range(steps):
        # Complex mean field: Z = (1/N) Σ e^(iφⱼ) = R·e^(iψ)
        Z = np.mean(np.exp(1j * phases))
        psi = np.angle(Z)
        R = abs(Z)

        # Kuramoto step via Euler's identity: e^(iφ) drives each φ toward ψ
        # dφ_i/dt = ω_i + κ·R·sin(ψ - φ_i)  — O(N), no matrix
        dphi = omega_rad + kappa * R * np.sin(psi - phases)
        phases += dphi * dt

        # Winding number (natural via complex, tracked for diagnostics)
        crossing = phases >= 2 * np.pi
        winding_count += crossing.astype(np.int32)
        phases %= 2 * np.pi

        # Store
        phases_t[i] = phases
        R_t[i] = R
        psi_t[i] = psi
        windings_t[i] = winding_count.copy()
        dphi_t[i] = dphi

    # Compute potential energy over time
    cos_matrix = 1 - np.cos(phases_t[:, :, np.newaxis] - phases_t[:, np.newaxis, :])
    potential_t = np.sum(cos_matrix, axis=(1, 2)) / (2 * n)

    return {
        "kappa": kappa,
        "n": n,
        "dt": dt,
        "steps": steps,
        "omega": omega.tolist(),
        "omega_rad": omega_rad.tolist(),
        "t": t_t.tolist(),
        "phases": phases_t.tolist(),
        "R": R_t.tolist(),
        "psi": psi_t.tolist(),
        "windings": windings_t.tolist(),
        "dphi": dphi_t.tolist(),
        "potential": potential_t.tolist(),
        "seed": seed,
        "R_final": float(R_t[-1]),
        "R_mean": float(np.mean(R_t[-1000:])),  # mean over last second
        "R_std": float(np.std(R_t[-1000:])),
    }


# ── Experiment management ─────────────────────────────────────────────────────


def experiment_id() -> str:
    return datetime.now(timezone.utc).strftime("K%Y%m%d_%H%M%S")


def ensure_dirs() -> Path:
    for d in EXPERIMENT_SUBDIRS:
        (EXPERIMENT_DIR / d).mkdir(parents=True, exist_ok=True)
    return EXPERIMENT_DIR


def save_experiment(
    result: dict[str, Any],
    *,
    eid: str | None = None,
    notes: str = "",
) -> Path:
    """Save simulation result with full provenance to experiment dir."""
    base = ensure_dirs()
    if eid is None:
        eid = experiment_id()

    # Config
    config = {
        "experiment_id": eid,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "n": result["n"],
            "kappa": result["kappa"],
            "dt": result["dt"],
            "steps": result["steps"],
            "seed": result["seed"],
            "base_freq": BASE_FREQ,
            "freq_spread": FREQ_SPREAD,
        },
        "notes": notes,
    }
    cfg_path = base / "configs" / f"{eid}_config.json"
    cfg_path.write_text(json.dumps(config, indent=2, ensure_ascii=False))

    # Raw data (lightweight — only essential time series, omit full phase matrix)
    raw = {
        "experiment_id": eid,
        "kappa": result["kappa"],
        "n": result["n"],
        "steps": result["steps"],
        "t": result["t"],
        "R": result["R"],
        "psi": result["psi"],
        "windings": result["windings"],
        "dphi": result["dphi"],
        "potential": result["potential"],
        "omega": result["omega"],
        "R_final": result["R_final"],
        "R_mean": result["R_mean"],
        "R_std": result["R_std"],
        "phases_sample": result["phases"][::100],  # decimate 100x
    }
    raw_path = base / "raw_data" / f"{eid}_raw.json"
    raw_path.write_text(json.dumps(raw, cls=_NumpyEncoder, indent=1, ensure_ascii=False))

    # Project log
    log_path = base / "logs" / "experiments.csv"
    header = not log_path.exists()
    with open(log_path, "a") as f:
        if header:
            f.write("experiment_id,timestamp,kappa,n,steps,R_final,R_mean,R_std,notes\n")
        f.write(
            f"{eid},{config['timestamp']},{result['kappa']},{result['n']},"
            f"{result['steps']},{result['R_final']:.6f},{result['R_mean']:.6f},"
            f"{result['R_std']:.6f},{notes}\n"
        )

    # Global registry
    if GLOBAL_REGISTRY:
        gheader = not GLOBAL_REGISTRY.exists()
        with open(GLOBAL_REGISTRY, "a") as f:
            if gheader:
                f.write("project_id,experiment_id,timestamp,kappa,n,steps,R_final,R_mean,R_std,notes\n")
            f.write(
                f"{PROJECT_ID},{eid},{config['timestamp']},{result['kappa']},{result['n']},"
                f"{result['steps']},{result['R_final']:.6f},{result['R_mean']:.6f},"
                f"{result['R_std']:.6f},{notes}\n"
            )

    return base


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ── Plotting ──────────────────────────────────────────────────────────────────


def plot_results(result: dict[str, Any], eid: str, base: Path) -> list[Path]:
    """Generate and save plots for a simulation run. Returns list of plot paths."""
    if not HAS_MPL:
        return []

    paths = []
    n = result["n"]
    t = np.array(result["t"])
    R = np.array(result["R"])
    phases = np.array(result["phases"])
    potential = np.array(result["potential"])
    windings = np.array(result["windings"])
    dphi = np.array(result["dphi"])
    kappa = result["kappa"]

    # 1. Order parameter R(t)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(t, R, color="royalblue", lw=0.8)
    ax.axhline(np.mean(R[-1000:]), color="red", ls="--", lw=0.5, label=f"R_mean={result['R_mean']:.4f}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("R = |⟨e^(iφ)⟩|")
    ax.set_title(f"Kuramoto Order Parameter — κ={kappa:.3f}, N={n}")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    p = base / "plots" / f"{eid}_R.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(p)

    # 2. Phase heatmap φ_i(t)
    fig, ax = plt.subplots(figsize=(12, 6))
    extent = [t[0], t[-1], 0, n]
    im = ax.imshow(
        phases.T,
        aspect="auto",
        cmap="twilight",
        extent=extent,
        origin="lower",
        interpolation="nearest",
        vmin=0,
        vmax=2 * np.pi,
    )
    plt.colorbar(im, ax=ax, label="Phase φ (rad)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Oscillator index")
    ax.set_title(f"Phase evolution — κ={kappa:.3f}, N={n}")
    p = base / "plots" / f"{eid}_phases.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(p)

    # 3. Instantaneous frequency (dφ_i)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(t, dphi[:, :6] / (2 * np.pi), lw=0.5, alpha=0.8)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("f_i = dφ_i / 2π (Hz)")
    ax.set_title(f"Instantaneous frequencies (first 6 oscillators) — κ={kappa:.3f}")
    ax.grid(True, alpha=0.3)
    p = base / "plots" / f"{eid}_freq.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(p)

    # 4. Mean phase ψ(t) evolution
    psi = np.unwrap(np.array(result["psi"]))
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(t, psi, color="seagreen", lw=0.8)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("ψ(t) — mean phase (rad)")
    ax.set_title(f"Mean phase drift — κ={kappa:.3f}")
    ax.grid(True, alpha=0.3)
    p = base / "plots" / f"{eid}_meanphase.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(p)

    # 5. Potential energy
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(t, potential, color="darkorange", lw=0.8)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("V(t) — potential energy")
    ax.set_title(f"Phase network potential — κ={kappa:.3f}")
    ax.grid(True, alpha=0.3)
    p = base / "plots" / f"{eid}_potential.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(p)

    return paths


# ── Kappa sweep ────────────────────────────────────────────────────────────────


def sweep_kappa(
    kappas: list[float],
    *,
    steps: int = 10000,
    seed: int | None = None,
    notes: str = "",
) -> list[dict[str, Any]]:
    """Run Kuramoto at each kappa value, save all results."""
    base = ensure_dirs()
    sweep_id = experiment_id() + "_SWEEP"
    results = []
    omega = intrinsic_frequencies(N_OSCILLATORS, seed=seed)

    for k in kappas:
        eid = experiment_id() + f"_K{k:.3f}"
        print(f"  κ={k:.3f} ...", end=" ", flush=True)
        t0 = time.perf_counter()
        r = run_kuramoto(k, steps=steps, omega=omega, seed=seed)
        elapsed = time.perf_counter() - t0
        print(f"R_final={r['R_final']:.4f}, R_mean={r['R_mean']:.4f} ({elapsed:.1f}s)")
        save_experiment(r, eid=eid, notes=notes)
        paths = plot_results(r, eid, base)
        results.append(r)

    # Sweep summary
    sweep_data = {
        "sweep_id": sweep_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "n": N_OSCILLATORS,
        "steps": steps,
        "kappas": [r["kappa"] for r in results],
        "R_final": [r["R_final"] for r in results],
        "R_mean": [r["R_mean"] for r in results],
        "R_std": [r["R_std"] for r in results],
    }
    sw_path = base / "raw_data" / f"{sweep_id}_sweep.json"
    sw_path.write_text(json.dumps(sweep_data, indent=1, ensure_ascii=False))

    # Sweep plot R(κ)
    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(
            [r["kappa"] for r in results],
            [r["R_mean"] for r in results],
            "o-", color="royalblue", lw=1.5, markersize=4,
        )
        ax.fill_between(
            [r["kappa"] for r in results],
            [r["R_mean"] - r["R_std"] for r in results],
            [r["R_mean"] + r["R_std"] for r in results],
            alpha=0.2, color="royalblue",
        )
        ax.axhline(0.5, color="red", ls="--", lw=0.5, label="R=0.5 (partial sync)")
        ax.set_xlabel("Coupling κ")
        ax.set_ylabel("R (mean over last second)")
        ax.set_title(f"Kuramoto bifurcation diagram — N={N_OSCILLATORS}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        p = base / "plots" / f"{sweep_id}_bifurcation.png"
        fig.savefig(p, dpi=150, bbox_inches="tight")
        plt.close(fig)

    return results


# ── CLI ────────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Kuramoto 24-oscillator simulation")
    parser.add_argument("--mode", choices=["single", "sweep"], default="sweep")
    parser.add_argument("--kappa", type=float, default=1.0, help="Coupling (single mode)")
    parser.add_argument("--kappas", type=float, nargs=2, default=[0.0, 2.0], help="Sweep range")
    parser.add_argument("--steps", type=int, default=10000, help="Simulation steps")
    parser.add_argument("--n-kappas", type=int, default=21, help="Points in sweep")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed")
    parser.add_argument("--notes", type=str, default="", help="Experiment notes")
    parser.add_argument("--project-version", type=str, default="v1.0", help="Project version directory")
    parser.add_argument("--no-plot", action="store_true", help="Skip plotting")
    parser.add_argument("--archive", action="store_true", help="Archive old runs")
    args = parser.parse_args()

    # Set version directory
    global EXPERIMENT_DIR
    EXPERIMENT_DIR = EXPERIMENT_DIR.parent / args.project_version

    if args.archive:
        print("Archive mode: compress old runs...")
        import shutil
        base = ensure_dirs()
        for d in EXPERIMENT_SUBDIRS:
            src = base / d
            if src.exists():
                dst = base / "archive" / f"{d}_{experiment_id()}.tar.gz"
                print(f"  {d} → {dst}")
        return 0

    global HAS_MPL
    if args.no_plot:
        HAS_MPL = False

    seed = args.seed or int(time.time()) % 100000
    print(f"Kuramoto {N_OSCILLATORS} oscillators, {args.steps} steps, seed={seed}")
    print(f"Results: {EXPERIMENT_DIR}")

    if args.mode == "single":
        print(f"\nSingle run: κ={args.kappa}")
        eid = experiment_id() + f"_K{args.kappa:.3f}"
        r = run_kuramoto(args.kappa, steps=args.steps, seed=seed)
        print(f"  R_final={r['R_final']:.6f}, R_mean={r['R_mean']:.6f}, R_std={r['R_std']:.6f}")
        save_experiment(r, eid=eid, notes=args.notes)
        plot_results(r, eid, ensure_dirs())

    else:
        k0, k1 = args.kappas
        kappas = np.linspace(k0, k1, args.n_kappas).tolist()
        print(f"  Sweep: κ ∈ [{k0:.1f}, {k1:.1f}], {len(kappas)} points")
        sweep_kappa(kappas, steps=args.steps, seed=seed, notes=args.notes)

    print(f"\nDone. Results in {EXPERIMENT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
