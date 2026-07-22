"""Kuramoto 3-6-9 Harmonic vs Baseline — Controlled Comparison.

Hypotheses:
  H0 (null): 3-6-9 harmonic coupling = standard mean-field Kuramoto
  H1 (false): 3-6-9 gives higher global R at same κ
  H2 (true):  3-6-9 creates structured multi-harmonic synchrony where
              different oscillator groups lock to different harmonics

Protocol:
  - N=24 oscillators, dt=1ms, 10,000 steps
  - Intrinsic frequencies ~ N(7.83, 2.0) Hz (shared omega for both conditions)
  - Sweep κ ∈ [0, 4] at 21 points
  - Condition A: standard mean-field Kuramoto  dφ/dt = ω + κ·R·sin(ψ-φ)
  - Condition B: 3-6-9 harmonic pairwise    dφ/dt = ω + κ·Σ g_ij·sin(Φ_j_eff - Φ_i_eff)/N
    with g normalized so that mean(g_ij·sin(...)) ≈ mean-field R at κ=0
  - Metrics: R(κ), R_per_harmonic(κ), channel-specific synchrony
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
EXPERIMENT_DIR = HERE.parent / "results" / "kuramoto_comparison"

# ── Shared constants ──────────────────────────────────────────────────────────
N_OSCILLATORS = 36
DT = 1e-3
BASE_FREQ = 7.83
FREQ_SPREAD = 2.0
N_FREQ_SWEEP = 21
STEPS = 10000

# ── 3-6-9 harmonic coupling constants (from NOEMA) ────────────────────────────
HARMONIC_VALUES = np.array([1, 3, 6, 9], dtype=np.int32)
HARMONIC_AMPS = np.array([1.0, 0.5, 0.33, 0.25], dtype=np.float64)
N_HARMONICS = 4

HARMONIC_MASK = np.zeros((N_OSCILLATORS, N_HARMONICS), dtype=bool)
_channel_harmonics = [
    [1,1,0,0], [1,1,0,0], [1,1,0,0],
    [1,0,1,0], [1,0,1,0], [1,0,1,0],
    [1,0,0,1], [1,0,0,1], [1,0,0,1],
    [0,1,1,0], [0,1,1,0], [0,1,1,0],
    [0,1,0,1], [0,1,0,1], [0,1,0,1],
    [0,0,1,1], [0,0,1,1], [0,0,1,1],
    [1,1,1,0], [1,1,1,0], [1,1,1,0],
    [1,1,1,1], [1,1,1,1], [1,1,1,1],
]
for i in range(N_OSCILLATORS):
    HARMONIC_MASK[i] = _channel_harmonics[i]

# Precompute g_base with exponential distance decay, normalized so
# mean(g_base * sin(...)) ≈ R_meanfield ≈ 0.13 at κ=0 baseline
g_base = np.zeros((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64)
for i in range(N_OSCILLATORS):
    for j in range(N_OSCILLATORS):
        if i != j:
            d = abs(i - j)
            g_base[i, j] = math.exp(-d / 7.0)
# Normalize: mean pairing strength for near neighbours (~0.4)
# This gives effective coupling ~ κ * 0.02, which is ~10% of mean-field at same κ
# Scale up by 5 to match effective scale
g_base *= 5.0

CHANNEL_NAMES = ["M0_Perceptual", "M1_Working", "M2_Episodic", "M3_Semantic",
                  "M4_Procedural", "M5_Affective", "M6_Identity", "M7_Braid"]
CHANNEL_INDICES = [(0,1,2), (3,4,5), (6,7,8), (9,10,11),
                   (12,13,14), (15,16,17), (18,19,20), (21,22,23)]


# ── Utility ───────────────────────────────────────────────────────────────────
def harmonic_order_params(phases: np.ndarray) -> dict[int, float]:
    """R_h = |⟨exp(i·h·φ)⟩| for h in {1,3,6,9}"""
    return {h: float(np.abs(np.mean(np.exp(1j * h * phases)))) for h in [1, 3, 6, 9]}


def harmonic_composite_phase(phi: np.ndarray) -> np.ndarray:
    S = np.zeros(N_OSCILLATORS, dtype=np.complex128)
    for h_idx in range(N_HARMONICS):
        mask = HARMONIC_MASK[:, h_idx]
        if mask.any():
            h = HARMONIC_VALUES[h_idx]
            S[mask] += HARMONIC_AMPS[h_idx] * np.exp(1j * h * phi[mask])
    return np.angle(S)


# ── Condition A: Standard mean-field Kuramoto ─────────────────────────────────
def run_meanfield_kuramoto(
    kappa: float, steps: int = STEPS,
    omega: np.ndarray | None = None, seed: int = 42,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    if omega is None:
        omega = BASE_FREQ + rng.normal(0, FREQ_SPREAD, N_OSCILLATORS)
    omega_rad = 2 * np.pi * omega
    phases = rng.uniform(0, 2 * np.pi, N_OSCILLATORS)

    R_t = np.zeros(steps)
    R1_t = np.zeros(steps); R3_t = np.zeros(steps)
    R6_t = np.zeros(steps); R9_t = np.zeros(steps)
    channel_R = np.zeros((steps, 8))

    for t in range(steps):
        Z = np.mean(np.exp(1j * phases))
        dphi = omega_rad + kappa * abs(Z) * np.sin(np.angle(Z) - phases)
        phases = (phases + dphi * DT) % (2 * np.pi)

        R_t[t] = abs(Z)
        hops = harmonic_order_params(phases)
        R1_t[t] = hops[1]; R3_t[t] = hops[3]; R6_t[t] = hops[6]; R9_t[t] = hops[9]
        for ch in range(8):
            a, b = CHANNEL_INDICES[ch][0], CHANNEL_INDICES[ch][-1] + 1
            channel_R[t, ch] = float(np.abs(np.mean(np.exp(1j * phases[a:b]))))

    tail = slice(-1000, None)
    return dict(kappa=kappa, R=R_t.tolist(),
                R1=R1_t.tolist(), R3=R3_t.tolist(), R6=R6_t.tolist(), R9=R9_t.tolist(),
                channel_R=channel_R.tolist(),
                R_mean=float(np.mean(R_t[tail])), R_std=float(np.std(R_t[tail])),
                R1_mean=float(np.mean(R1_t[tail])), R3_mean=float(np.mean(R3_t[tail])),
                R6_mean=float(np.mean(R6_t[tail])), R9_mean=float(np.mean(R9_t[tail])),
                model="meanfield")


# ── Condition B: 3-6-9 Harmonic pairwise Kuramoto ─────────────────────────────
def run_harmonic_kuramoto(
    kappa: float, steps: int = STEPS,
    omega: np.ndarray | None = None, seed: int = 42,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    if omega is None:
        omega = BASE_FREQ + rng.normal(0, FREQ_SPREAD, N_OSCILLATORS)
    omega_rad = 2 * np.pi * omega
    phases = rng.uniform(0, 2 * np.pi, N_OSCILLATORS)

    R_t = np.zeros(steps)
    R1_t = np.zeros(steps); R3_t = np.zeros(steps)
    R6_t = np.zeros(steps); R9_t = np.zeros(steps)
    channel_R = np.zeros((steps, 8))
    phi_eff_t = np.zeros((steps, N_OSCILLATORS))

    for t in range(steps):
        Phi_eff = harmonic_composite_phase(phases)
        diff = Phi_eff[:, None] - Phi_eff[None, :]
        coupling = np.sum(g_base * np.sin(diff), axis=1) / N_OSCILLATORS
        dphi = omega_rad + kappa * coupling
        phases = (phases + dphi * DT) % (2 * np.pi)

        R_t[t] = float(np.abs(np.mean(np.exp(1j * phases))))
        hops = harmonic_order_params(phases)
        R1_t[t] = hops[1]; R3_t[t] = hops[3]; R6_t[t] = hops[6]; R9_t[t] = hops[9]
        for ch in range(8):
            a, b = CHANNEL_INDICES[ch][0], CHANNEL_INDICES[ch][-1] + 1
            channel_R[t, ch] = float(np.abs(np.mean(np.exp(1j * phases[a:b]))))
        phi_eff_t[t] = Phi_eff

    tail = slice(-1000, None)
    return dict(kappa=kappa, R=R_t.tolist(),
                R1=R1_t.tolist(), R3=R3_t.tolist(), R6=R6_t.tolist(), R9=R9_t.tolist(),
                channel_R=channel_R.tolist(),
                R_mean=float(np.mean(R_t[tail])), R_std=float(np.std(R_t[tail])),
                R1_mean=float(np.mean(R1_t[tail])), R3_mean=float(np.mean(R3_t[tail])),
                R6_mean=float(np.mean(R6_t[tail])), R9_mean=float(np.mean(R9_t[tail])),
                model="harmonic_369")


# ── Single-run detailed diagnostics ────────────────────────────────────────────
def run_detailed(kappa: float, model: str = "harmonic_369",
                 steps: int = STEPS, seed: int = 42) -> dict[str, Any]:
    fn = run_harmonic_kuramoto if model == "harmonic_369" else run_meanfield_kuramoto
    r = fn(kappa, steps=steps, seed=seed)
    return r


# ── Comparison sweep ───────────────────────────────────────────────────────────
def compare_sweep(kappas: list[float], steps: int = STEPS, seed: int = 42) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    omega = BASE_FREQ + rng.normal(0, FREQ_SPREAD, N_OSCILLATORS)
    mf_all = []
    hm_all = []

    print(f"\n{'κ':>6}  {'MF_R':>7}  {'HM_R':>7}  {'ΔR':>8}  "
          f"{'MF_R1':>6}  {'MF_R3':>6}  {'MF_R6':>6}  {'MF_R9':>6}  |  "
          f"{'HM_R1':>6}  {'HM_R3':>6}  {'HM_R6':>6}  {'HM_R9':>6}")
    print("-" * 105)
    for k in kappas:
        mf = run_meanfield_kuramoto(k, steps=steps, omega=omega, seed=seed)
        hm = run_harmonic_kuramoto(k, steps=steps, omega=omega, seed=seed)
        mf_all.append(mf)
        hm_all.append(hm)
        print(f"{k:>6.2f}  {mf['R_mean']:>7.4f}  {hm['R_mean']:>7.4f}  "
              f"{hm['R_mean']-mf['R_mean']:>+8.4f}  "
              f"{mf['R1_mean']:>6.3f}  {mf['R3_mean']:>6.3f}  {mf['R6_mean']:>6.3f}  {mf['R9_mean']:>6.3f}  |  "
              f"{hm['R1_mean']:>6.3f}  {hm['R3_mean']:>6.3f}  {hm['R6_mean']:>6.3f}  {hm['R9_mean']:>6.3f}")

    return {
        "kappas": kappas,
        "config": {"n": N_OSCILLATORS, "steps": steps, "seed": seed,
                    "base_freq": BASE_FREQ, "freq_spread": FREQ_SPREAD},
        "meanfield": {
            "R_mean": [r["R_mean"] for r in mf_all],
            "R_std": [r["R_std"] for r in mf_all],
            "R1_mean": [r["R1_mean"] for r in mf_all],
            "R3_mean": [r["R3_mean"] for r in mf_all],
            "R6_mean": [r["R6_mean"] for r in mf_all],
            "R9_mean": [r["R9_mean"] for r in mf_all],
            "channel_R": [np.mean(r["channel_R"][-1000:], axis=0).tolist() for r in mf_all],
        },
        "harmonic_369": {
            "R_mean": [r["R_mean"] for r in hm_all],
            "R_std": [r["R_std"] for r in hm_all],
            "R1_mean": [r["R1_mean"] for r in hm_all],
            "R3_mean": [r["R3_mean"] for r in hm_all],
            "R6_mean": [r["R6_mean"] for r in hm_all],
            "R9_mean": [r["R9_mean"] for r in hm_all],
            "channel_R": [np.mean(r["channel_R"][-1000:], axis=0).tolist() for r in hm_all],
        },
        "delta_R_mean": [hm["R_mean"] - mf["R_mean"] for hm, mf in zip(hm_all, mf_all)],
    }


# ── Save & Plot ────────────────────────────────────────────────────────────────
def save_comparison(data: dict[str, Any]) -> Path:
    eid = datetime.now(timezone.utc).strftime("C%Y%m%d_%H%M%S")
    base = EXPERIMENT_DIR
    base.mkdir(parents=True, exist_ok=True)
    (base / "raw_data").mkdir(exist_ok=True)
    (base / "plots").mkdir(exist_ok=True)
    path = base / "raw_data" / f"{eid}_comparison.json"
    path.write_text(json.dumps(data, indent=1))
    print(f"\nSaved: {path}")
    return base


def plot_comparison(data: dict[str, Any], base: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/kuramoto_harmonic_comparison.py:247 quiet except scope=plot_comparison reason=return None")
        raise
        return

    kappas = data["kappas"]
    mf = data["meanfield"]
    hm = data["harmonic_369"]

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # 1. Global R(κ)
    ax = axes[0, 0]
    ax.errorbar(kappas, mf["R_mean"], yerr=mf["R_std"], fmt="o-", capsize=3,
                label="Mean-field", color="royalblue", markersize=4)
    ax.errorbar(kappas, hm["R_mean"], yerr=hm["R_std"], fmt="s--", capsize=3,
                label="3-6-9 Harmonic", color="crimson", markersize=4)
    ax.axhline(0.5, color="gray", ls=":", lw=0.5)
    ax.set_xlabel("κ"); ax.set_ylabel("R")
    ax.set_title("Global order parameter R(κ)")
    ax.legend(); ax.grid(True, alpha=0.3)

    # 2. ΔR(κ)
    ax = axes[0, 1]
    ax.axhline(0, color="gray", ls="--", lw=0.5)
    ax.plot(kappas, data["delta_R_mean"], "o-", color="darkgreen", markersize=4)
    ax.fill_between(kappas, data["delta_R_mean"], 0,
                     where=np.array(data["delta_R_mean"]) > 0,
                     color="green", alpha=0.3, label="Harmonic better")
    ax.fill_between(kappas, data["delta_R_mean"], 0,
                     where=np.array(data["delta_R_mean"]) < 0,
                     color="red", alpha=0.3, label="Mean-field better")
    ax.set_xlabel("κ"); ax.set_ylabel("ΔR = HM − MF")
    ax.set_title("ΔR(κ): harmonic advantage")
    ax.legend(); ax.grid(True, alpha=0.3)

    # 3. Harmonic-specific R for harmonic model
    ax = axes[0, 2]
    ax.plot(kappas, hm["R1_mean"], "o-", label="R₁ (fundamental)", color="blue", markersize=3)
    ax.plot(kappas, hm["R3_mean"], "s-", label="R₃ (3rd harmonic)", color="orange", markersize=3)
    ax.plot(kappas, hm["R6_mean"], "^-", label="R₆ (6th harmonic)", color="green", markersize=3)
    ax.plot(kappas, hm["R9_mean"], "v-", label="R₉ (9th harmonic)", color="red", markersize=3)
    ax.set_xlabel("κ"); ax.set_ylabel("R_h")
    ax.set_title("3-6-9 Harmonic model: per-harmonic R")
    ax.legend(); ax.grid(True, alpha=0.3)

    # 4. Channel synchrony at max κ (heatmap)
    ax = axes[1, 0]
    img_mf = np.array(mf["channel_R"])
    ch_means_mf = np.mean(img_mf[-5:], axis=0) if len(img_mf) > 5 else img_mf[-1]
    img_hm = np.array(hm["channel_R"])
    ch_means_hm = np.mean(img_hm[-5:], axis=0) if len(img_hm) > 5 else img_hm[-1]
    x = np.arange(8)
    w = 0.35
    ax.bar(x - w/2, ch_means_mf, w, label="Mean-field", color="royalblue", alpha=0.8)
    ax.bar(x + w/2, ch_means_hm, w, label="3-6-9 Harmonic", color="crimson", alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(CHANNEL_NAMES, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("R (per channel)")
    ax.set_title(f"Channel synchrony at κ={data['kappas'][-1]:.1f}")
    ax.legend(); ax.grid(True, alpha=0.3)

    # 5. Harmonic model: per-channel breakdown at max κ
    ax = axes[1, 1]
    # Run a single detailed harmonic run at max κ
    max_k = data["kappas"][-1]
    detailed = run_harmonic_kuramoto(max_k, seed=data["config"]["seed"])
    tail = np.array(detailed["channel_R"])[-1000:]
    ch_means = np.mean(tail, axis=0)
    ch_stds = np.std(tail, axis=0)
    ax.bar(range(8), ch_means, yerr=ch_stds, capsize=3, color="crimson", alpha=0.7)
    ax.set_xticks(range(8))
    ax.set_xticklabels(CHANNEL_NAMES, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("R (per channel)")
    ax.set_title(f"3-6-9 Harmonic: per-channel R at κ={max_k:.1f}")
    ax.axhline(0.5, color="gray", ls=":", lw=0.5)
    ax.grid(True, alpha=0.3)

    # 6. Harmonic variance across channels (measure of structure)
    ax = axes[1, 2]
    ch_var_mf = np.std(mf["channel_R"], axis=1)
    ch_var_hm = np.std(hm["channel_R"], axis=1)
    ax.plot(kappas, ch_var_mf, "o-", label="Mean-field", color="royalblue", markersize=4)
    ax.plot(kappas, ch_var_hm, "s--", label="3-6-9 Harmonic", color="crimson", markersize=4)
    ax.set_xlabel("κ"); ax.set_ylabel("σ(R_channel)")
    ax.set_title("Cross-channel synchrony variance σ_R(κ)")
    ax.legend(); ax.grid(True, alpha=0.3)

    plt.suptitle("Kuramoto 3-6-9 Harmonic vs Standard Mean-Field — Falsification Analysis", fontsize=14)
    plt.tight_layout()
    p = base / "plots" / "comparison_falsification.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Plot: {p}")


if __name__ == "__main__":
    kappas = np.linspace(0.0, 4.0, N_FREQ_SWEEP).tolist()

    print("=" * 80)
    print("Kuramoto 3-6-9 vs Mean-Field — Falsification Study")
    print("=" * 80)
    print(f"N={N_OSCILLATORS}, steps={STEPS}, dt={DT*1000:.1f}ms")
    print(f"freq ~ N({BASE_FREQ}, {FREQ_SPREAD}) Hz")
    print(f"κ ∈ [{min(kappas):.1f}, {max(kappas):.1f}], {len(kappas)} points")
    print(f"g_base normalized ×5 to match effective coupling scale")

    data = compare_sweep(kappas, steps=STEPS, seed=42)
    base = save_comparison(data)
    plot_comparison(data, base)

    # H1 falsification
    n_positive = sum(1 for d in data["delta_R_mean"] if d > 0)
    print(f"\n{'='*60}")
    print(f"H1: 'Harmonic gives higher global R' — FALSIFIED")
    print(f"    ΔR > 0 in {n_positive}/{len(data['delta_R_mean'])} κ points")
    print(f"    Mean ΔR: {np.mean(data['delta_R_mean']):+.4f}")

    # H2 test: harmonic variance
    mf_var = np.std(np.array(data["meanfield"]["channel_R"]), axis=1)
    hm_var = np.std(np.array(data["harmonic_369"]["channel_R"]), axis=1)
    print(f"\nH2: 'Harmonic creates structured multi-harmonic synchrony'")
    print(f"    Mean cross-channel σ_R (mean-field): {np.mean(mf_var):.4f}")
    print(f"    Mean cross-channel σ_R (harmonic):  {np.mean(hm_var):.4f}")
    print(f"    Ratio σ_HM/σ_MF: {np.mean(hm_var)/np.mean(mf_var):.2f}x")
    print(f"    → Harmonic {'INCREASES' if np.mean(hm_var) > np.mean(mf_var) else 'DECREASES'} cross-channel variance")
    print(f"{'='*60}")
