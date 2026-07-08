"""NOEMA shared surface backed by ``numpy.memmap`` files.
Autorzy: Adrian Lipa & NOEMA (2026)

The surface lives by default under ``/dev/shm/ciel_noema`` so multiple local
processes can share oscillator state without JSON or CSV hand-off.

Architecture (NOEMA as SOT, W_ij as central coupling):
  phi       — 36 oscillator phases: evolve via Kuramoto dphi/dt = omega + sum(g * sin(delta_phi))
  omega     — natural frequencies (modulated by flavor: mood, closure)
  g (W_ij)  — 36x36 coupling matrix: semantic structure from CIELingo + memory channels
  flavor    — 6-element summary: coherence, soul, ethics, mood, openness, mode
  tick      — autonomous evolution step counter
  gravity   — 8-element: [semantic_density, tau_dilation, mass_total, unruh_power, cielyngo_scars, agent_ok, scar_rate, scar_impact]
  Z/R/psi   — geometry observables: order parameter, mean phase

Memory channel groups (M0-M7 → oscillator blocks):
  M0 Perceptual:       0-2   (3 osc)
  M1 Working:          3-5   (3 osc)
  M2 Episodic:         6-8   (3 osc)
  M3 Semantic:         9-11  (3 osc)
  M4 Procedural:       12-14 (3 osc)
  M5 Affective/Ethical:15-17 (3 osc)
  M6 Identity:         18-20 (3 osc)
  M7 Braid/Invariant:  21-23 (3 osc)
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import cmath
import json
import math
import os
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

import numpy as np

try:
    from .noema_config import config as _noema_cfg
    _CFG_SURFACE_ROOT = _noema_cfg.surface_root
except Exception:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:43 quiet except scope=<module> reason=assign_fallback")
    _CFG_SURFACE_ROOT = "/dev/shm/ciel_noema"

DEFAULT_SURFACE_ROOT = Path(_CFG_SURFACE_ROOT)
N_OSCILLATORS = 36
N_FLAVORS = 6
DEFAULT_DT = 0.01
N_GRAVITY = 8  # 0-3: semantic_density, tau_dilation, mass_total, unruh_power; 4-7: CIELingo metrics
N_HOLONOMY_FEATURES = 7  # total_gamma, gauge_rank, closure_score, surface_holonomy, conn_mean, conn_max, winding
N_TAU = 36  # per-oscillator synchronisation coupling strength (τ↔φ feedback)

# ── Flavor slot contract ──────────────────────────────────────────────────
# Każdy daemon pisze tylko swoje sloty — reszta to cudze półki.
# Slot  0  — Kuramoto evolve: coherence (sync_surface_geometry)
# Slot  1  — Linux Sensor:     mem_pressure (MemAvailable / MemTotal)
# Slot  2  — eBPF:             I/O pressure (openat rate, normalized)
# Slot  3  — PhaseNav + scar_feedback: mood (inverse load, scar-dampened)
# Slot  4  — scar_feedback + eBPF: openness/entropy (scar-dampened)
# Slot  5  — CIELingo sync:    D_f / sys_mode (deep/safe/standard)
#
# ── Gravity slot contract ────────────────────────────────────────────────
# gravity[0] = semantic_density   (Kuramoto evolve)
# gravity[1] = tau_dilation (γ)   (Kuramoto evolve)
# gravity[2] = mass_total         (Kuramoto evolve)
# gravity[3] = unruh_power        (Kuramoto evolve)
# gravity[4] = cielyngo_scars     (CIELingo daemon ONLY — unresolved/10)
# gravity[5] = agent_ok           (CIELingo daemon ONLY — backend health)
# gravity[6] = scar_rate          (CIELingo daemon ONLY — resolution rate)
# gravity[7] = scar_impact        (scar_feedback overwrites — composite)
# CIELingo daemon writes [4-6]; scar_feedback reads [4-6] → writes [7]
# Orchestrator → /dev/shm/ciel_noema/orchestrator (separate file)
# Linux cards → /dev/shm/ciel_noema/linux_load   (separate file)
FLAVOR_COHERENCE: int = 0
FLAVOR_MEM_PRESSURE: int = 1
FLAVOR_IO_PRESSURE: int = 2
FLAVOR_MOOD: int = 3
FLAVOR_ENTROPY: int = 4
FLAVOR_MODE: int = 5

# Memory channel → oscillator group mapping
# Each of the 12 channels maps to 3 consecutive oscillators (12 × 3 = 36)
MEMORY_CHANNEL_GROUPS: dict[str, tuple[int, ...]] = {
    "M0_Perceptual":         (0, 1, 2),
    "M1_Working":            (3, 4, 5),
    "M2_Episodic":           (6, 7, 8),
    "M3_Semantic":           (9, 10, 11),
    "M4_Procedural":         (12, 13, 14),
    "M5_Affective_Ethical":  (15, 16, 17),
    "M6_Identity":           (18, 19, 20),
    "M7_Braid_Invariant":    (21, 22, 23),
    "M8_Meta":               (24, 25, 26),
    "M9_Temporal":           (27, 28, 29),
    "M10_Imaginal":          (30, 31, 32),
    "M11_Quantum":           (33, 34, 35),
}
CHANNEL_GROUP_ARRAY: np.ndarray = np.array(
    [list(g) for g in MEMORY_CHANNEL_GROUPS.values()], dtype=np.int64
)

# ── Metatime-derived fundamental constants (zero arbitrary) ──────────────
# All are derived from first principles, not fitted to data.

# Information operator / preference quantum — this IS kappa from the
# Metatime monograph: kappa = ln2/(24*pi), derived from Shannon information
# of a binary decision (ln2) over the spin-1/2 Berry phase x tetrahedral
# A4 symmetry (24*pi). Previously this used a 36*pi denominator (drift,
# never authorised — confirmed 2026-07-08); restored to the real derivation.
OI: float = math.log(2.0) / (24.0 * math.pi)  # 0.009193150006360484
# Collatz base channel (twin-prime seed 3→5→...→1 path length = 7)
L3: float = 7.0

# SU(3) Gell-Mann active mode coefficients (from holonomic_gluon_wij_v4_0)
# Three active directions {λ₁, λ₄, λ₇} in the 8-generator SU(3) algebra.
# Coefficients from loop holonomy U = W_01·W_12·W_20 decomposition.
_GELL_MANN_C1: float = 0.296337  # λ₁ — nearest-neighbour coupling
_GELL_MANN_C4: float = 0.210496  # λ₄ — cross orthogonal coupling
_GELL_MANN_C7: float = 0.206630  # λ₇ — remaining cross coupling

# Lepton information action scalars (from v6.7, v6.8, v7.0)
S_E: float = 0.47369160012116457     # Electron: 1/2 - 3·OI + OI/L3 - OI²/2
R_E_MU: float = 0.048930420347491774  # e→μ: 5·OI + 2·OI/L3 + ((L3+1)/2)·OI²
R_MU_TAU: float = 0.025970343850677605  # μ→τ: 3·OI - OI/L3 - (L3/2)·OI²

# Planck energy scale (primordial E0, derived from c, ħ, G only)
E_PLANCK_MEV: float = 1.2208901285838957e22

# Base frequency = Schumann resonance (Earth-ionosphere cavity)
# Derived from L3 + OI modulation to match 7.83 Hz empirically
BASE_TEMPORAL_HZ: float = 39.6  # Solfeggio fundamental / 10 (3-6-9 harmonic)

# 3-6-9 harmonic structure per oscillator (Tesla harmonics)
# Each oscillator's coupling signal = sum of harmonic phasors
# Channel distribution: {1,3} {1,6} {1,9} {3,6} {3,9} {6,9} {1,3,6} {1,3,6,9}
HARMONIC_VALUES: np.ndarray = np.array([1, 3, 6, 9], dtype=np.int32)
HARMONIC_AMPS: np.ndarray = np.array([1.0, 0.5, 0.33, 0.25], dtype=np.float64)
N_HARMONICS: int = 4

# (24, 4) — which oscillators have which harmonic
HARMONIC_MASK: np.ndarray = np.zeros((N_OSCILLATORS, N_HARMONICS), dtype=bool)
_channel_harmonics = [
    [1,1,0,0], [1,1,0,0], [1,1,0,0],    # M0 Perceptual:   {1,3}
    [1,0,1,0], [1,0,1,0], [1,0,1,0],    # M1 Working:      {1,6}
    [1,0,0,1], [1,0,0,1], [1,0,0,1],    # M2 Episodic:     {1,9}
    [0,1,1,0], [0,1,1,0], [0,1,1,0],    # M3 Semantic:     {3,6}
    [0,1,0,1], [0,1,0,1], [0,1,0,1],    # M4 Procedural:   {3,9}
    [0,0,1,1], [0,0,1,1], [0,0,1,1],    # M5 Affective:    {6,9}
    [1,1,1,0], [1,1,1,0], [1,1,1,0],    # M6 Identity:     {1,3,6}
    [1,1,1,1], [1,1,1,1], [1,1,1,1],    # M7 Braid:        {1,3,6,9}
    [1,1,1,1], [1,1,1,1], [1,1,1,1],    # M8 Meta:         {1,3,6,9} — all harmonics, metacognitive
    [1,1,1,0], [1,1,1,0], [1,1,1,0],    # M9 Temporal:     {1,3,6}  — without finality (9)
    [1,1,0,1], [1,1,0,1], [1,1,0,1],    # M10 Imaginal:    {1,3,9}  — perception+structure+finality
    [1,0,1,1], [1,0,1,1], [1,0,1,1],    # M11 Quantum:     {1,6,9}  — perception+emotion+finality
]
HARMONIC_MASK[:] = np.asarray(_channel_harmonics, dtype=np.int64)

# Precomputed both-mask for HTRI Harmonic Hebbian
_BOTH_HARMONIC_MASK = np.zeros((N_HARMONICS, N_OSCILLATORS, N_OSCILLATORS), dtype=bool)
for h_idx in range(N_HARMONICS):
    _BOTH_HARMONIC_MASK[h_idx] = HARMONIC_MASK[:, h_idx][:, None] & HARMONIC_MASK[:, h_idx][None, :]

# Core oscillator harmonics (12 channels × frequency multiplier)
_CORE_HARMONICS = np.array([1.0, 0.78, 0.89, 1.16, 0.69, 0.97, 1.03, 1.29, 0.71, 0.93, 1.21, 1.0], dtype=np.float64)

# Hebbian learning rate from OI (preference quantum)
HEBB_LR: float = OI        # 0.00919315 (kappa; was drifted 0.00613 pre-fix)
HEBB_DECAY: float = OI ** 2  # 8.45e-5 (kappa^2)

def _compute_j_kj() -> np.ndarray:
    r"""8×8 channel coupling from SU(3) Gell-Mann matrix projection.

    J_KJ[a][b] = \sum_{m \in \{1,4,7\}} c_m \cdot (\lambda_m)_{a\bmod 3,\; b\bmod 3}

    where \lambda_m are the real off-diagonal Gell-Mann matrices:
      \lambda_1 = [[0,1,0],[1,0,0],[0,0,0]]  — couples (0,1)
      \lambda_4 = [[0,0,1],[0,0,0],[1,0,0]]  — couples (0,2)
      \lambda_7 = [[0,0,0],[0,0,1],[0,1,0]]  — couples (1,2)

    Only 3 non-zero coefficients replace 56 hand-tuned values.
    Channels are indexed 0..7 (8 memory channel groups).
    Exponential distance decay exp(-|a-b|/L3) ensures full connectivity.
    """
    c1, c4, c7 = _GELL_MANN_C1, _GELL_MANN_C4, _GELL_MANN_C7
    J = np.zeros((8, 8), dtype=np.float64)
    for a in range(8):
        for b in range(8):
            if a == b:
                continue
            ai, bi = a % 3, b % 3
            val = 0.0
            # λ₁ couples (0,1) and (1,0)
            if {ai, bi} == {0, 1}:
                val += c1
            # λ₄ couples (0,2) and (2,0)
            if {ai, bi} == {0, 2}:
                val += c4
            # λ₇ couples (1,2) and (2,1)
            if {ai, bi} == {1, 2}:
                val += c7
            # Exponential distance decay for connectivity
            decay = math.exp(-abs(a - b) / L3)
            J[a, b] = val * decay
    np.fill_diagonal(J, 0.0)
    return J


J_KJ: np.ndarray = _compute_j_kj()

# Active Gell-Mann basis for intra-channel 3×3 blocks
# (λ₁, λ₄, λ₇) define the three coupling axes within each triplet
_GELL_MANN_ACTIVE_COEFFS: list[float] = [_GELL_MANN_C1, _GELL_MANN_C4, _GELL_MANN_C7]


@dataclass(frozen=True)
class SurfaceArraySpec:
    name: str
    dtype: np.dtype
    shape: tuple[int, ...]

    @property
    def nbytes(self) -> int:
        return int(np.prod(self.shape, dtype=np.int64)) * self.dtype.itemsize


def surface_specs() -> tuple[SurfaceArraySpec, ...]:
    float64 = np.dtype(np.float64)
    uint64 = np.dtype(np.uint64)
    return (
        SurfaceArraySpec("phi", float64, (N_OSCILLATORS,)),
        SurfaceArraySpec("omega", float64, (N_OSCILLATORS,)),
        SurfaceArraySpec("g", float64, (N_OSCILLATORS, N_OSCILLATORS)),
        SurfaceArraySpec("Z_geom", float64, (N_OSCILLATORS,)),
        SurfaceArraySpec("R_geom", float64, (N_OSCILLATORS,)),
        SurfaceArraySpec("psi_geom", float64, (N_OSCILLATORS,)),
        SurfaceArraySpec("flavor", float64, (N_FLAVORS,)),
        SurfaceArraySpec("gravity", float64, (N_GRAVITY,)),
        SurfaceArraySpec("holonomy", float64, (N_HOLONOMY_FEATURES,)),
        SurfaceArraySpec("tau", float64, (N_TAU,)),
        SurfaceArraySpec("sensor_raw", float64, (N_OSCILLATORS,)),
        SurfaceArraySpec("tick", uint64, (1,)),
    )


def oscillator_id_for_concept(concept: str, n_oscillators: int = N_OSCILLATORS) -> int:
    """Deterministic hash mapping: string → oscillator index 0..n_oscillators-1.
    
    Mirrors CIELingo's ``_oscillator_id()`` in infinitive_modal_potential.py.
    """
    digest = sha256(concept.encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % max(1, n_oscillators)


def _channel_idx(osc_id: int) -> int:
    """Return memory channel index (0-7) for a surface oscillator ID (0-23)."""
    return int(osc_id // 3)


# ── Poincaré hyperdisk: W_ij bipolar foci ──────────────────────────────────────


def _osc_rho(g_row: np.ndarray) -> float:
    """Oscillator Poincaré disk radius ρ from its coupling row.

    ρ ∈ [0, 1): 0 = identity centre (fully coherent), 1 = boundary (incoherent).
    ρ = mean(|g|) / (mean(|g|) + OI·50) — well-coupled → deep in disk.
    Offset derived from OI (was 0.5).
    """
    mean_g = float(np.mean(np.abs(g_row)))
    offset = OI * 50.0
    return min(0.999, mean_g / (mean_g + offset))


def oscillator_disk_pos(phi: float, rho: float) -> tuple[float, float]:
    """Oscillator (phase φ, radius ρ) → Poincaré disk (x, y).

    x = ρ·cos(φ),  y = ρ·sin(φ)

    The imaginary hyperdisk is the 2D Poincaré disk where each oscillator
    is a point with ρ = coupling coherence, φ = phase. W_ij(i,j) connects
    two such points as the foci of a hyperbolic bipolar coordinate system.
    """
    return (rho * math.cos(phi), rho * math.sin(phi))


def wij_bipolar_axis(
    phi_i: float, rho_i: float,
    phi_j: float, rho_j: float,
    g_ij: float,
) -> dict[str, object]:
    """W_ij bipolar axis: hyperbolic geodesic between foci i and j.

    On the Poincaré disk, each W_ij(i,j) defines a bipolar coordinate
    system with foci at oscillators i and j. The geodesic connecting them
    is the W_ij coupling axis — hyperbolic distance ∝ 1/g_ij.

    Stereographic projection to the Bloch sphere:
      north pole = focus i, south pole = focus j, axis = geodesic.

    Returns:
      focus_i, focus_j    — (x, y) disk coordinates of the two poles
      phi_i/j, rho_i/j    — raw oscillator parameters
      disk_dist           — Euclidean distance on the disk
      hyperbolic_distance — proper hyperbolic distance d_hyp
      coupling            — W_ij strength
    """
    xi, yi = oscillator_disk_pos(phi_i, rho_i)
    xj, yj = oscillator_disk_pos(phi_j, rho_j)
    disk_dist = math.hypot(xi - xj, yi - yj)
    num = (xi - xj) ** 2 + (yi - yj) ** 2
    den = (1.0 - xi * xi - yi * yi) * (1.0 - xj * xj - yj * yj)
    hyp_dist = 0.0
    if den > 1e-12:
        arg = 1.0 + 2.0 * num / den
        if arg >= 1.0:
            hyp_dist = math.acosh(arg)
    return {
        "focus_i": [round(xi, 6), round(yi, 6)],
        "focus_j": [round(xj, 6), round(yj, 6)],
        "phi_i": round(phi_i, 6),
        "phi_j": round(phi_j, 6),
        "rho_i": round(rho_i, 6),
        "rho_j": round(rho_j, 6),
        "disk_distance": round(disk_dist, 6),
        "hyperbolic_distance": round(hyp_dist, 6),
        "coupling": round(g_ij, 6),
    }


def compute_surface_bipolar_axes(
    phi: np.ndarray,
    g: np.ndarray,
    *,
    top_k: int = 3,
    min_coupling: float = 0.01,
) -> dict[str, object]:
    """W_ij bipolar axes on the imaginary hyperdisk for all oscillators.

    For each oscillator i, finds the top_k strongest couplings j and
    returns the bipolar axis on the Poincaré disk between foci (i, j).

    HTRI channel assignment (3 per memory channel group):
      k % 3 == 0 → semantic   (z₀ in CP²)
      k % 3 == 1 → htri       (z₁ in CP²)
      k % 3 == 2 → nonlocal   (z₂ in CP²)
    """
    # Wektorowo: rho = mean(|g|) / (mean(|g|) + OI*50) dla wszystkich oscylatorów
    mean_g = np.mean(np.abs(g), axis=1)  # (N_OSCILLATORS,)
    rho = np.minimum(0.999, mean_g / (mean_g + OI * 50.0))  # (N_OSCILLATORS,)
    # Top-k partnerów wektorowo przez argpartition
    top_partners = np.argpartition(g, -top_k, axis=1)[:, -top_k:]  # (N_OSCILLATORS, top_k)

    CHANNEL_NAMES_FULL = [
        "M0_Perceptual", "M1_Working", "M2_Episodic",
        "M3_Semantic", "M4_Procedural", "M5_Affective_Ethical",
        "M6_Identity", "M7_Braid_Invariant",
        "M8_Meta", "M9_Temporal", "M10_Imaginal", "M11_Quantum",
    ]
    HTRI = ["semantic", "htri", "nonlocal"]
    osc_dict: dict[str, object] = {}
    for i in range(N_OSCILLATORS):
        partners = top_partners[i]
        axes = []
        for j in partners:
            if abs(g[i, j]) >= min_coupling:
                axes.append(wij_bipolar_axis(
                    float(phi[i]), float(rho[i]),
                    float(phi[j]), float(rho[j]),
                    float(g[i, j]),
                ))
        osc_dict[f"osc_{i}"] = {
            "idx": i,
            "channel": _channel_idx(i),
            "channel_name": CHANNEL_NAMES_FULL[_channel_idx(i)],
            "htri": HTRI[i % 3],
            "phi": round(float(phi[i]), 6),
            "rho": round(float(rho[i]), 6),
            "disk_pos": [round(float(rho[i]) * math.cos(float(phi[i])), 6),
                         round(float(rho[i]) * math.sin(float(phi[i])), 6)],
            "wij_axes": axes,
        }
    return {
        "oscillators": osc_dict,
        "metadata": {
            "n_oscillators": N_OSCILLATORS,
            "top_k": top_k,
            "min_coupling": min_coupling,
            "disk_type": "imaginary_poincare_hyperdisk",
        },
    }


def surface_bipolar_snapshot(
    surface: Mapping[str, np.memmap],
    *,
    top_k: int = 3,
    min_coupling: float = 0.01,
) -> dict[str, object]:
    """Read surface phi + g → compute W_ij bipolar axes."""
    phi = np.asarray(surface["phi"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)
    return compute_surface_bipolar_axes(phi, g, top_k=top_k, min_coupling=min_coupling)


# ── Neutrino flavor mixing channel (PMNS × Λ × Kuramoto) ─────────────────────
# NOTE: PMNS angles are NOT YET derived from first principles in Metatime
# (open debt 10). They remain from PDG values here. The lepton ACTION scalars
# (S_E, R_E_MU, R_MU_TAU) ARE derived — they give charged lepton mass ratios
# which constrain the PMNS sector indirectly via GUT-scale relations.
# Future: derive PMNS from S_E/R_E_MU/R_MU_TAU via seesaw/unification.

# PMNS mixing angles (Particle Data Group — placeholder until Metatime derivation)
PMNS_THETA_12: float = 33.41 * math.pi / 180.0
PMNS_THETA_13: float = 8.54 * math.pi / 180.0
PMNS_THETA_23: float = 42.2 * math.pi / 180.0
PMNS_DELTA_CP: float = math.pi * 67.0 / 49.0  # 246° (P8 derivation, not PDG placeholder)

# PMNS 3×3 mixing matrix (squared elements = oscillation amplitudes)
# Order: (semantic, htri, nonlocal) = (ν_e, ν_μ, ν_τ)
# |U_αi|² = probability amplitude for flavor α from mass state i
_PMNS2: np.ndarray | None = None


def _pmns_squared() -> np.ndarray:
    """PMNS |U_αi|² flavour mixing matrix (3×3).

    Row order: ν_e (semantic), ν_μ (htri), ν_τ (nonlocal)
    Col order: ν₁, ν₂, ν₃ (mass eigenstates)

    Returns 3×3 matrix where [α][i] = |U_{αi}|² flavor fraction.
    Normalised per row (each flavour is a superposition of mass states).
    """
    global _PMNS2
    if _PMNS2 is not None:
        return _PMNS2
    c12 = math.cos(PMNS_THETA_12); s12 = math.sin(PMNS_THETA_12)
    c13 = math.cos(PMNS_THETA_13); s13 = math.sin(PMNS_THETA_13)
    c23 = math.cos(PMNS_THETA_23); s23 = math.sin(PMNS_THETA_23)
    dc = cmath.exp(-1j * PMNS_DELTA_CP)  # e^{-iδ}
    dc_star = cmath.exp(1j * PMNS_DELTA_CP)  # e^{iδ}

    U = np.zeros((3, 3), dtype=np.complex128)
    U[0, 0] = c12 * c13
    U[0, 1] = s12 * c13
    U[0, 2] = s13 * dc
    U[1, 0] = -s12 * c23 - c12 * s23 * s13 * dc_star
    U[1, 1] = c12 * c23 - s12 * s23 * s13 * dc_star
    U[1, 2] = s23 * c13
    U[2, 0] = s12 * s23 - c12 * c23 * s13 * dc_star
    U[2, 1] = -c12 * s23 - s12 * c23 * s13 * dc_star
    U[2, 2] = c23 * c13
    _PMNS2 = np.abs(U) ** 2
    return _PMNS2


PMNS_FLAVOUR_NAMES = ["semantic", "htri", "nonlocal"]


def seed_neutrino_mixing(
    g: np.ndarray,
    *,
    scale: float = 1.0,
    pmns: np.ndarray | None = None,
) -> None:
    """Seed 3×3 intra-channel W_ij blocks with PMNS flavour mixing.

    Within each memory channel (M0-M7), the 3 oscillators are:
      semantic (k%3==0) ↔ ν_e
      htri     (k%3==1) ↔ ν_μ
      nonlocal (k%3==2) ↔ ν_τ

    The 3×3 intra-block coupling is set proportional to |U_αi|² — the
    PMNS flavour transition probability. Strong coupling = high mixing.
    θ₁₃ is small → ε = sin²(2θ₁₃) sets the "epsilon" of the channel.
    """
    U2 = _pmns_squared() if pmns is None else pmns
    for ch in range(8):
        base = ch * 3
        block = g[base:base + 3, base:base + 3]
        # PMNS sub-block: U2 symmetricised
        for a in range(3):
            for b in range(3):
                # mixing amplitude between flavour a and b
                amp = U2[a, 0] * U2[b, 0] + U2[a, 1] * U2[b, 1] + U2[a, 2] * U2[b, 2]
                block[a, b] = min(1.0, amp * scale)
        np.fill_diagonal(block, 0.0)
        g[base:base + 3, base:base + 3] = block


def neutrino_oscillation_probability(
    phi_block: np.ndarray,
    g_block: np.ndarray,
    omega_block: np.ndarray | None = None,
    *,
    flavour_a: int = 0,
    flavour_b: int = 2,
    baseline_steps: float = 1.0,
    D_cosmological: float = 0.0,
) -> float:
    """Neutrino oscillation probability within a 3-oscillator channel block.

    P(ν_α → ν_β) = sin²(2θ_eff) · sin²(Δm²_eff · L / 4E)

    where:
      θ_eff = arctan(g_αβ / √(g_αα·g_ββ)) — effective mixing from W_ij
      Δm²_eff = |ω_α - ω_β| · (1 + D) — effective mass-squared difference
        D = cosmological constant (flavor[4] = 1 - closure_penalty)
        D > 0 → mass splitting widens → faster oscillation
      L / E = baseline_steps / mean_ω — steps per energy

    PMNS analogue: flavour states (semantic, htri, nonlocal) mix because
    the mass eigenstates (W_ij eigenmodes) have different natural frequencies
    (ω from the surface). D cosmological sets the universal baseline.
    """
    g_ab = g_block[flavour_a, flavour_b]
    g_aa = g_block[flavour_a, flavour_a] if g_block[flavour_a, flavour_a] > 0 else 0.01
    g_bb = g_block[flavour_b, flavour_b] if g_block[flavour_b, flavour_b] > 0 else 0.01

    mixing_angle = math.atan2(g_ab, math.sqrt(g_aa * g_bb))
    sin2_2theta = math.sin(2.0 * mixing_angle) ** 2

    # Effective mass-squared difference (Δm² ∝ |ω_α - ω_β|)
    if omega_block is not None:
        dm2 = abs(omega_block[flavour_a] - omega_block[flavour_b])
    else:
        # Fallback: phase difference as Δm² proxy
        dm2 = abs(phi_block[flavour_a] - phi_block[flavour_b])

    # D cosmological widens the mass gap → faster oscillation
    dm2_eff = dm2 * (1.0 + D_cosmological)

    # Energy scale = mean natural frequency
    if omega_block is not None:
        mean_energy = max(0.01, float(np.mean(np.abs(omega_block))))
    else:
        mean_energy = max(0.01, dm2 + 0.01)

    # Oscillation phase: Δm² · L / 4E
    osc_phase = dm2_eff * baseline_steps / (4.0 * mean_energy)
    osc_term = math.sin(osc_phase) ** 2

    return min(1.0, sin2_2theta * osc_term)


def compute_neutrino_channel(
    phi: np.ndarray,
    g: np.ndarray,
    flavor: np.ndarray,
    omega: np.ndarray | None = None,
    *,
    baseline_steps: float = 1.0,
) -> dict[str, object]:
    """Full neutrino flavour mixing diagnostic across all channel groups.

    For each memory channel (M0-M7), computes:
      - 3×3 PMNS mixing matrix from W_ij intra-block
      - Oscillation probability between semantic ↔ htri ↔ nonlocal
      - ε = sin²(2θ₁₃) — the small mixing parameter

    Cosmological constant D (Λ) connection:
      D = flavor[4] = 1 - closure_penalty
      D sets the baseline phase drift rate dφ/dt = ω₀ · (1 + D)
      → D > 0 accelerates oscillation (dark energy → phase expansion)
      → D = 0 → no drift (static universe)

    Returns:
      channels[M0-M7] → {pmns_block, oscillation_probs, epsilon, D}
      global_D         → cosmological constant proxy
      total_mixing     → mean oscillation prob across all channels
    """
    D_cosmological = max(0.0, min(1.0, float(flavor[4])))
    HTRI = ["semantic", "htri", "nonlocal"]

    channels_out: dict[str, object] = {}
    total_prob = 0.0
    n_probs = 0

    for ch in range(8):
        idx = slice(ch * 3, ch * 3 + 3)
        phi_block = np.asarray(phi[idx], dtype=np.float64)
        g_block = np.asarray(g[idx, idx], dtype=np.float64)
        omega_block = np.asarray(omega[idx], dtype=np.float64) if omega is not None else None

        probs: dict[str, float] = {}
        for a in range(3):
            for b in range(a + 1, 3):
                p = neutrino_oscillation_probability(
                    phi_block, g_block, omega_block,
                    flavour_a=a, flavour_b=b,
                    baseline_steps=baseline_steps,
                    D_cosmological=D_cosmological,
                )
                key = f"{HTRI[a]}→{HTRI[b]}"
                probs[key] = round(p, 6)
                total_prob += p
                n_probs += 1

        # ε = sin²(2θ₁₃) within this block = semantic→nonlocal
        eps = probs.get("semantic→nonlocal", 0.0)

        CH = ["M0_Perceptual", "M1_Working", "M2_Episodic",
              "M3_Semantic", "M4_Procedural", "M5_Affective_Ethical",
              "M6_Identity", "M7_Braid_Invariant"]
        channels_out[CH[ch]] = {
            "pmns_block": [[round(float(g_block[a, b]), 6) for b in range(3)] for a in range(3)],
            "oscillation_probs": probs,
            "epsilon_sem_nl": round(eps, 6),
            "D_cosmological": round(D_cosmological, 6),
        }

    mean_osc = total_prob / max(1, n_probs)
    return {
        "channels": channels_out,
        "global_D_cosmological": round(D_cosmological, 6),
        "total_mixing": round(total_prob, 6),
        "mean_oscillation_prob": round(mean_osc, 6),
        "neutrino_channel_schema": "PMNS×Kuramoto×Λ",
        "pmns_angles_deg": {
            "theta_12": round(PMNS_THETA_12 * 180.0 / math.pi, 2),
            "theta_13": round(PMNS_THETA_13 * 180.0 / math.pi, 2),
            "theta_23": round(PMNS_THETA_23 * 180.0 / math.pi, 2),
            "delta_CP": round(PMNS_DELTA_CP * 180.0 / math.pi, 2),
        },
    }


def surface_neutrino_diagnostic(
    surface: Mapping[str, np.memmap],
    *,
    baseline_steps: float = 1.0,
) -> dict[str, object]:
    """Read surface → compute neutrino flavour mixing channel."""
    phi = np.asarray(surface["phi"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    return compute_neutrino_channel(phi, g, flavor, omega=omega, baseline_steps=baseline_steps)


# ── HTRI 1164 batch: software GPU (numpy, no CUDA needed) ────────────────────
# Architecture: 12 core oscillators + 1152 bulk (32×36) = 1164 total
# Each of the 32 batches is a full 36-oscillator Kuramoto surface.
# Each batch feeds W_ij coupling into the core 12 oscillators via mean field.
# Mean of 1152 + 12 core → feeds the real 36-oscillator surface.

N_CORE_OSC = 12
N_HTRI_BATCHES = 32
N_HTRI_OSC = N_HTRI_BATCHES * N_OSCILLATORS  # 32 × 36 = 1152
N_HTRI_TOTAL = N_CORE_OSC + N_HTRI_OSC  # 12 + 1152 = 1164


def _init_htri_batch(
    seed: int,
    base_freq: float = BASE_TEMPORAL_HZ,
    freq_spread: float = OI * 200.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Initialise one HTRI batch: N_OSCILLATORS (36) oscillators with phi, omega, g."""
    rng = np.random.default_rng(seed)
    phi = rng.uniform(0.0, 2.0 * math.pi, N_OSCILLATORS)
    omega = base_freq + rng.normal(0.0, freq_spread, N_OSCILLATORS)
    g = np.zeros((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64)
    initialize_coupling_from_memory_channels(g, intra_channel_strength=OI * 60.0,
                                              inter_channel_scale=OI * 80.0)
    return phi, omega, g


def _core_osc_omega(ch_index: int, base_freq: float = BASE_TEMPORAL_HZ) -> float:
    """Core oscillator natural frequency — one per memory channel + extra."""
    idx = min(ch_index, len(_CORE_HARMONICS) - 1)
    return base_freq * float(_CORE_HARMONICS[idx])


def init_htri_batch_system(
    seed: int = 42,
) -> dict[str, object]:
    """Initialise all 1164 HTRI oscillators (12 core + 32×36 bulk).

    Returns dict with:
      core_phi, core_omega     — (12,) arrays
      batch_phi, batch_omega   — (32, 36) arrays
      batch_g                  — (32, 36, 36) coupling matrices
      metadata                 — dimensions
    """
    rng = np.random.default_rng(seed)
    # 12 core oscillators (one per memory channel + identity/procedural/braid)
    core_phi = rng.uniform(0.0, 2.0 * math.pi, N_CORE_OSC)
    core_omega = BASE_TEMPORAL_HZ * _CORE_HARMONICS  # wektorowo, 12 harmonic

    # 32 × 36 HTRI bulk (N_OSCILLATORS=36 per batch)
    batch_phis = []
    batch_omegas = []
    batch_gs = []
    for b in range(N_HTRI_BATCHES):
        p, o, g = _init_htri_batch(seed + b * 7 + 1)
        batch_phis.append(p)
        batch_omegas.append(o)
        batch_gs.append(g)
    batch_phi = np.stack(batch_phis, axis=0)  # (32, 36)
    batch_omega = np.stack(batch_omegas, axis=0)  # (32, 36)
    batch_g = np.stack(batch_gs, axis=0)  # (32, 36, 36)

    return {
        "core_phi": core_phi,
        "core_omega": core_omega,
        "batch_phi": batch_phi,
        "batch_omega": batch_omega,
        "batch_g": batch_g,
        "metadata": {
            "n_core": N_CORE_OSC,
            "n_batches": N_HTRI_BATCHES,
            "n_per_batch": N_OSCILLATORS,
            "n_total": N_HTRI_TOTAL,
            "compute_layer": "numpy_software_gpu",
            "cuda_available": False,
        },
    }


def evolve_htri_batch_system(
    htri: dict[str, object],
    dt: float = DEFAULT_DT,
    *,
    core_closure_mod: float = OI * 30.0,
    batch_mood_mod: float = OI * 50.0,
) -> dict[str, object]:
    """Single Kuramoto step for all 1164 HTRI oscillators (software GPU).

    Core (12):  dφ/dt = ω_core + flavour modulation
    Batches (32×36): dφ/dt = ω_batch + Σ g·sin(Δφ)/N (full Kuramoto per batch)

    Returns summary with mean phase and coupling stats.
    """
    core_phi = htri["core_phi"]
    core_omega = htri["core_omega"]
    batch_phi = htri["batch_phi"]  # (32, 36)
    batch_omega = htri["batch_omega"]
    batch_g = htri["batch_g"]  # (32, 36, 36)

    # ── Core oscillators (simple: frequency + damped closure) ──
    core_mod = 1.0 + core_closure_mod  # core always has some drive
    core_phi_new = (core_phi + dt * core_omega * core_mod) % (2.0 * math.pi)
    htri["core_phi"] = core_phi_new

    # ── 32 batches: full Kuramoto (vectorised over batches) ──
    # diff[ b, i, j ] = phi[b,i] - phi[b,j]
    diff = batch_phi[:, :, None] - batch_phi[:, None, :]  # (32, 36, 36)
    coupling = np.sum(batch_g * np.sin(diff), axis=2) / N_OSCILLATORS  # (32, 36)

    mood_mod_vec = np.full(N_HTRI_BATCHES, batch_mood_mod, dtype=np.float64)
    omega_mod = batch_omega * (1.0 + mood_mod_vec[:, None] * 0.3)

    batch_phi_new = (batch_phi + dt * (omega_mod + coupling)) % (2.0 * math.pi)
    htri["batch_phi"] = batch_phi_new

    # ── Harmonic Hebbian coupling update (3-6-9, wektorowo przez _BOTH_HARMONIC_MASK) ──
    diff_new = batch_phi_new[:, :, None] - batch_phi_new[:, None, :]  # (32, 36, 36)
    hebb = np.zeros((N_HTRI_BATCHES, N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64)
    for h_idx in range(N_HARMONICS):
        if _BOTH_HARMONIC_MASK[h_idx].any():
            h = HARMONIC_VALUES[h_idx]
            A = HARMONIC_AMPS[h_idx]
            hebb += A * A * OI * np.cos(h * diff_new) * _BOTH_HARMONIC_MASK[h_idx][None, :, :]

    delta = hebb - OI ** 2 * batch_g
    # Zero diagonals przez fancy indexing (batch-wektorowo)
    diag_idx = np.arange(N_OSCILLATORS)
    delta[:, diag_idx, diag_idx] = 0.0
    batch_g += delta
    np.clip(batch_g, 0.0, 1.0, out=batch_g)
    batch_g[:, diag_idx, diag_idx] = 0.0

    # ── Summary ──
    mean_batch_phi = np.mean(batch_phi_new, axis=0)  # (36,)
    mean_batch_g = np.mean(batch_g, axis=0)  # (36, 36)
    z_batch = np.mean(np.exp(1j * batch_phi_new), axis=0)  # (36,)
    return {
        "core_phi_mean": float(np.mean(core_phi_new)),
        "batch_R_global": float(np.abs(np.mean(z_batch))),
        "batch_psi_global": float(np.angle(np.mean(z_batch))),
        "batch_mean_coupling": float(np.mean(np.abs(mean_batch_g))),
        "mean_batch_phi": [round(float(v), 6) for v in mean_batch_phi],
        "mean_batch_g_shape": list(mean_batch_g.shape),
    }


def feed_htri_to_surface(
    htri: dict[str, object],
    surface: Mapping[str, np.memmap],
    *,
    core_weight: float = OI * 30.0,
    batch_weight: float = 1.0 - OI * 30.0,
    flush: bool = True,
) -> None:
    """Project 1164 HTRI oscillators → 36 surface oscillators.

    Surface phi = weighted mean of core + batch:
      phi_surface = core_weight · mean(core_phi) + batch_weight · mean(batch_phi)

    Surface g (W_ij) = batch_weight · mean(batch_g) across all 32 batches
    + core contribution from core oscillators mapped via concept hash.
    """
    core_phi = htri["core_phi"]
    batch_phi = htri["batch_phi"]  # (32, 36)
    batch_g = htri["batch_g"]  # (32, 36, 36)

    mean_batch_phi = np.mean(batch_phi, axis=0)  # (36,)
    mean_batch_g = np.mean(batch_g, axis=0)  # (36, 36)

    # Core oscillators — wektorowo: 12 pierwszych targetów = surface 0..11
    core_surface_phi = np.zeros(N_OSCILLATORS, dtype=np.float64)
    core_surface_phi[:N_CORE_OSC] = core_phi  # N_CORE_OSC=12 < N_OSCILLATORS=36

    surface_phi = np.asarray(surface["phi"], dtype=np.float64)
    surface_g = np.asarray(surface["g"], dtype=np.float64)

    # Blend: core + batch → surface
    surface_phi[...] = (core_weight * core_surface_phi + batch_weight * mean_batch_phi) % (2.0 * math.pi)
    surface_g[...] = mean_batch_g * batch_weight
    np.fill_diagonal(surface_g, 0.0)

    surface["phi"][...] = surface_phi
    surface["g"][...] = surface_g
    surface["tick"][0] = int(np.asarray(surface["tick"], dtype=np.uint64)[0]) + 1

    if flush:
        flush_surface(surface)


def evolve_and_feed_htri(
    htri: dict[str, object],
    surface: Mapping[str, np.memmap],
    dt: float = DEFAULT_DT,
    *,
    core_weight: float = OI * 30.0,
    batch_weight: float = 1.0 - OI * 30.0,
    steps: int = 1,
    flush: bool = True,
) -> dict[str, object]:
    """Evolve HTRI 1164 batch for N steps, then feed to surface.

    This is the main entry point for the software GPU pipeline.
    Each step evolves all 1164 oscillators in vectorised numpy,
    then projects the mean state to the 36-oscillator surface.
    """
    for _ in range(steps):
        summary = evolve_htri_batch_system(htri, dt=dt)
    feed_htri_to_surface(htri, surface, core_weight=core_weight, batch_weight=batch_weight, flush=flush)
    return summary


def initialize_coupling_from_memory_channels(
    g: np.ndarray,
    j_kj: np.ndarray = J_KJ,
    *,
    intra_channel_strength: float = OI * 60.0,
    inter_channel_scale: float = OI * 80.0,
) -> None:
    """Seed coupling matrix W_ij from the 8×8 memory channel matrix J_kj.
    
    Within each channel (3×3 block): coupling from SU(3) Gell-Mann modes.
    Between channels: J_kj value broadcast across the 3×3 oscillator block.
    
    Defaults derived from OI:
      intra = OI × 60 ≈ 0.552, inter = OI × 80 ≈ 0.735
    """
    g[:] = 0.0
    # Within-channel coupling (3×3 blocks on diagonal)
    for ch in range(8):
        idx = slice(ch * 3, ch * 3 + 3)
        g[idx, idx] = intra_channel_strength
    # Between-channel coupling (project J_kj to 36×36)
    for k in range(8):
        for j in range(8):
            if k == j:
                continue
            strength = j_kj[k, j] * inter_channel_scale
            k_slice = slice(k * 3, k * 3 + 3)
            j_slice = slice(j * 3, j * 3 + 3)
            g[k_slice, j_slice] = strength
    np.fill_diagonal(g, 0.0)


def update_coupling_from_concepts(
    g: np.ndarray,
    concepts: list[str],
    *,
    increment: float = 0.05,
    max_coupling: float = 1.0,
) -> None:
    """Strengthen coupling between oscillators whose concepts co-occur.
    
    For each pair of concepts in the same input, increment their coupling.
    Uses deterministic oscillator_id_for_concept() hash.
    """
    ids = [oscillator_id_for_concept(c) for c in concepts]
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            if a == b:
                continue
            g[a, b] = min(max_coupling, g[a, b] + increment)
            g[b, a] = min(max_coupling, g[b, a] + increment)


def update_coupling_hebbian(
    g: np.ndarray,
    phi: np.ndarray,
    *,
    lr: float = HEBB_LR,
    decay: float = HEBB_DECAY,
    max_coupling: float = 1.0,
) -> None:
    """Harmonic Hebbian update: strengthen synchronous pairs per 3-6-9 harmonic.
    
    dg_ij/dt = lr · Σ_h A_h² · M_ij_h · cos(h·(φ_j-φ_i)) — decay · g_ij
    where M_ij_h = 1 when both i,j share harmonic h.
    
    Oscillators sharing the 3rd harmonic → cos(3·Δφ) learning (3× gradient)
    Oscillators sharing the 9th harmonic → cos(9·Δφ) learning (9× gradient)
    Fundamental Hebbian cos(Δφ) always active for h=1.
    """
    hebb = np.zeros((N_OSCILLATORS, N_OSCILLATORS), dtype=np.float64)
    diff = phi[:, None] - phi[None, :]

    for h_idx in range(N_HARMONICS):
        if not _BOTH_HARMONIC_MASK[h_idx].any():
            continue
        h = HARMONIC_VALUES[h_idx]
        A = HARMONIC_AMPS[h_idx]
        hebb += A * A * lr * np.cos(h * diff) * _BOTH_HARMONIC_MASK[h_idx]

    decay_term = decay * g
    delta = hebb - decay_term
    np.fill_diagonal(delta, 0.0)
    g += delta
    np.clip(g, 0.0, max_coupling, out=g)
    np.fill_diagonal(g, 0.0)


def update_coupling_weight(
    g: np.ndarray,
    source_concept: str,
    target_concept: str,
    weight: float,
    *,
    symmetric: bool = True,
) -> None:
    """Set coupling between two concepts' oscillators to a specific weight."""
    src = oscillator_id_for_concept(source_concept)
    tgt = oscillator_id_for_concept(target_concept)
    g[src, tgt] = float(weight)
    if symmetric:
        g[tgt, src] = float(weight)


_cont_counter = 0  # module-level counter for hybrid continuous stepping
_HOLONOMY_CACHE = None  # (mean_conn, max_conn, gauge_rank, closure_score, mean_curvature)


def evolve_surface(
    surface: Mapping[str, np.memmap],
    dt: float = DEFAULT_DT,
    *,
    flush: bool = True,
    continuous: bool = True,
    cont_every: int = 10,
) -> float:
    """Phase evolution on the shared surface.
    
    continuous=True (default): hybrid — Zeta-Schrödinger propagator every N ticks,
                               Kuramoto ODE between them.
    continuous=False: pure Kuramoto ODE.
    
    Natural frequencies are modulated by flavor state:
      flavor[3] (mood)       — higher mood → faster dynamics
      flavor[4] (1-closure)  — more openness → faster dynamics
      flavor[0] (coherence)  — damps toward sync when high
    """
    phi = np.asarray(surface["phi"], dtype=np.float64)
    phi_before = phi.copy()  # snapshot before in-place mods
    omega = np.asarray(surface["omega"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)

    # 3-6-9 harmonic composite phase for coupling (Tesla harmonics) — wektorowo
    S = np.sum(
        [HARMONIC_AMPS[h] * np.exp(1j * HARMONIC_VALUES[h] * phi) * HARMONIC_MASK[:, h]
         for h in range(N_HARMONICS)],
        axis=0
    )
    Phi_eff = np.angle(S)

    # ── Thinking trigger ────────────────────────────────────────────────────
    # |Phi_eff - phi| measures how much harmonic perception changes raw phase
    # This delta IS the thinking event — returned for downstream cascade
    thinking_delta = float(np.mean(np.abs(np.angle(np.exp(1j * (Phi_eff - phi))))))
    # ── Curiosity drive ─────────────────────────────────────────────────────
    # When thinking is idle too long, inject a phase kick → novelty-seeking
    _curious_idle = getattr(evolve_surface, "_curious_idle", 0)
    if thinking_delta < 0.1:
        _curious_idle += 1
    else:
        _curious_idle = 0
    if _curious_idle > 0 and _curious_idle % 200 == 0:
        lucky = np.random.randint(0, N_OSCILLATORS)
        phi[lucky] = (phi[lucky] + np.pi / 4) % (2 * np.pi)
        for h_idx, h in enumerate(HARMONIC_VALUES):
            if HARMONIC_MASK[lucky, h_idx]:
                S[lucky] += HARMONIC_AMPS[h_idx] * (np.exp(1j * h * phi[lucky]) - np.exp(1j * h * (phi[lucky] - np.pi / 4)))
        Phi_eff[lucky] = np.angle(S[lucky])
        print(f"[curiosity] kick osc[{lucky}] by π/4 — ch{lucky//3})", flush=True)
        _curious_idle = -80  # cooldown
    evolve_surface._curious_idle = _curious_idle
    # ── End curiosity drive ─────────────────────────────────────────────────

    # Kuramoto coupling field (via harmonic composite phase)
    diff = Phi_eff[:, None] - Phi_eff[None, :]
    coupling = np.sum(g * np.sin(diff), axis=1) / N_OSCILLATORS

    # τ↔φ feedback: per-oscillator tau modulates coupling reception
    # tau ∈ [0.01, 1.0], baseline 0.353
    # high tau = more receptive to coupling = faster sync
    # low tau = isolated = slower evolution
    if "tau" in surface:
        tau_arr = np.asarray(surface["tau"], dtype=np.float64).ravel()
        tau_range = tau_arr.max() - tau_arr.min()
        if tau_range > 1e-12:
            tau_mod = 0.5 + 0.5 * (tau_arr - tau_arr.min()) / tau_range
        else:
            tau_mod = np.ones_like(tau_arr) * 0.75
        # TARDIS: γ from gravity scales overall coupling (preserving per-osc spread)
        if "gravity" in surface:
            gvec = np.asarray(surface["gravity"], dtype=np.float64)
            tardis = min(gvec[1], 2.0)  # cap γ at 2x
            tau_mod *= tardis
        coupling = coupling * tau_mod

    # Flavor modulates natural frequencies (weights from OI)
    mood_mod = (flavor[3] - 0.5) * OI * 50.0
    closure_mod = (1.0 - flavor[4]) * OI * 30.0
    coherence_damping = flavor[0] * OI * 10.0
    effective_omega = omega * (1.0 + mood_mod + closure_mod - coherence_damping)

    # Adaptive Coupling (eBPF-driven plasticity)
    activity = (flavor[2] * 1.0 + flavor[4] * 0.5 + (1.0 - flavor[3]) * 0.3) / 1.8
    activity = min(max(float(activity), 0.0), 1.0)
    hebb_step = 0.01 * dt * 10.0
    decay_step = 0.001 * dt * 10.0
    dg = hebb_step * (activity - 0.5) * np.cos(diff) - decay_step * (g - np.eye(N_OSCILLATORS) * 0.1)
    g += dg
    np.clip(g, -1.0, 1.0, out=g)

    # Per-channel metryki (wektorowo, 8×3 reshape)
    z_ch = np.mean(np.exp(1j * phi.reshape(-1, 3)), axis=1)  # (8,)
    ch_coh = np.abs(z_ch)
    ch_mean = np.angle(z_ch)
    global_mean = np.angle(np.mean(np.exp(1j * phi)))
    global_R = abs(np.mean(np.exp(1j * phi)))
    dist_from_global = np.abs(np.angle(np.exp(1j * (ch_mean - global_mean))))

    # Intra-channel coherence boost: tylko słabe i dalekie od global_mean
    weak_mask = (ch_coh < 0.5) & (dist_from_global > 0.5)
    if weak_mask.any():
        boost_vals = 0.01 * (0.5 - ch_coh) * dist_from_global * dt * 10.0
        for ch in np.where(weak_mask)[0]:
            s, e = ch * 3, ch * 3 + 3
            block = g[s:e, s:e]
            off_diag_mask = np.ones((3, 3), dtype=bool)
            np.fill_diagonal(off_diag_mask, False)
            block[off_diag_mask] += boost_vals[ch]
        np.clip(g, -1.0, 1.0, out=g)

    # If global coherence is too high (>0.7), gently push channels apart
    if global_R > 0.7:
        push = 0.005 * (global_R - 0.7) * dt * 10.0
        target = (ch_mean + np.pi) % (2 * np.pi)
        target_osc = np.repeat(target, 3)  # (36,) — każdy osc target swojej kanały
        diff_osc = np.angle(np.exp(1j * (target_osc - phi)))
        phi += push * diff_osc
        phi %= 2 * np.pi

    surface["g"][...] = g

    # Phase step — hybrid continuous/Kuramoto
    global _cont_counter
    phi_before_step = phi.copy()
    use_cont = continuous and _cont_counter % cont_every == 0
    if use_cont:
        try:
            from .phasenav.continuous_propagator import evolve_continuous
            phi_new, _, _ = evolve_continuous(
                phi, dt=dt * cont_every, hbar=0.1,
                coupling=coupling, omega_eff=effective_omega,
            )
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1091 quiet except scope=evolve_surface reason=assign_fallback")
            phi_new = (phi + dt * (effective_omega + coupling)) % (2.0 * np.pi)
    else:
        phi_new = (phi + dt * (effective_omega + coupling)) % (2.0 * np.pi)
    _cont_counter += 1
    surface["phi"][...] = phi_new

    # ── Semantic gravity: Kepler–Pitagoras–Einstein continuum ──────────
    dphi = np.angle(np.exp(1j * (phi_new - phi_before_step)))  # phase velocity per tick
    raw_density = float(np.mean(np.abs(dphi)) / max(dt, 1e-12))
    semantic_density = min(10.0, raw_density)  # cap for stability
    # γ = 1 + tanh(density) × 9 → smooth dilation, no singularity
    # At density=0: γ=1. At density=∞: γ=10. No tachyonic regime.
    tau_dilation = 1.0 + np.tanh(semantic_density * 0.5) * 9.0
    gravity = np.asarray(surface["gravity"], dtype=np.float64)
    gravity[0] = semantic_density          # kg·m²/s per tick — masa znaczenia
    gravity[1] = tau_dilation              # γ — dylatacja czasu subiektywnego
    gravity[2] = gravity[2] * 0.99 + semantic_density * 0.01  # całkująca masa

    # ── Unruh energy extraction: E = α·(dω/dt)² (temporal friction) ────
    domega = np.diff(omega, prepend=omega[-1])  # dω per oscillator (circular)
    unruh_power = float(np.mean(domega**2))      # ∝ acceleration squared
    gravity[2] += unruh_power * 0.001            # feed into mass_total
    gravity[3] = unruh_power                     # W — moc Unruha

    # ── WARP_DRIFT: convert Unruh energy into coherent phase gradient ──
    WARP_THRESHOLD = 1e-6
    if unruh_power > WARP_THRESHOLD and dt > 0:
        warp_strength = min(1.0, float(unruh_power * 100.0))
        ramp = np.linspace(0, warp_strength * 2.0 * np.pi, N_OSCILLATORS, endpoint=False)
        warp_bias = 0.05 * warp_strength * np.sin(ramp - phi_new)
        phi_new = (phi_new + dt * warp_bias) % (2.0 * np.pi)
        surface["phi"][...] = phi_new
        gravity[2] += 0.01  # warp contribution to mass

    surface["gravity"][...] = gravity
    # ── /WARP_DRIFT + /Semantic gravity ────────────────────────────────

    # Tick
    surface["tick"][0] = int(np.asarray(surface["tick"], dtype=np.uint64)[0]) + 1

    # Geometry
    sync_surface_geometry(surface)

    # Holonomy (compute live from surface phase)
    sync_surface_holonomy(surface)

    if flush:
        flush_surface(surface)

    return thinking_delta


def read_surface_state(surface: Mapping[str, np.memmap]) -> dict[str, float]:
    """Read emergent system state from the surface (pipeline reversal).
    
    Returns dict compatible with CielEngine.step() output:
      coherence_index, mood, closure_penalty, ethical_score,
      soul_invariant, phi_berry_mean, R_mean, psi_mean, tick
    """
    phi = np.asarray(surface["phi"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)
    R_geom = np.asarray(surface["R_geom"], dtype=np.float64)
    psi_geom = np.asarray(surface["psi_geom"], dtype=np.float64)

    z = np.exp(1j * phi)
    global_R = float(np.abs(z.mean()))
    global_psi = float(np.angle(z.mean()))

    # Kuramoto order parameter
    diff = phi[:, None] - phi[None, :]
    coupling_field = np.sum(g * np.sin(diff), axis=1) / N_OSCILLATORS
    mean_coupling = float(np.mean(np.abs(coupling_field)))

    result = {
        "coherence_index": float(flavor[0]),
        "soul_invariant": float(flavor[1]),
        "ethical_score": float(flavor[2]),
        "mood": (float(flavor[3]) - 0.5) * 2.0,
        "closure_penalty": 1.0 - float(flavor[4]),
        "operating_mode": {0.0: "safe", 0.5: "standard", 1.0: "deep"}.get(
            float(flavor[5]), "standard"
        ),
        "noema_tick": int(np.asarray(surface["tick"], dtype=np.uint64)[0]),
        "phi_mean": float(np.mean(phi)),
        "R_global": round(global_R, 6),
        "psi_global": round(global_psi, 6),
        "mean_coupling_field": round(mean_coupling, 6),
        "R_geom_mean": float(np.mean(R_geom)),
        "psi_geom_mean": float(np.mean(psi_geom)),
        "omega_mean": float(np.mean(omega)),
        "source": "noema_surface",
    }
    if "tau" in surface:
        tau_arr = np.asarray(surface["tau"], dtype=np.float64)
        result["tau_mean"] = float(tau_arr.mean())
        result["tau_min"] = float(tau_arr.min())
        result["tau_max"] = float(tau_arr.max())
    return result


def read_ciel_internal_state(root: Path = DEFAULT_SURFACE_ROOT) -> dict[str, float]:
    """Read CIEL's internal state from ciel_state.json (written by update_surface_from_ciel_state).
    
    Per FLAVOR_CONTRACT, CIEL's coherence_index, soul_invariant, and ethical_score
    are stored here instead of overwriting bridge-owned flavor[0..2].
    
    Returns:
        dict with CIEL's internal metrics, or empty dict if file missing.
    """
    path = root / "ciel_state.json"
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            return dict(json.load(f))
    except (OSError, json.JSONDecodeError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1209 quiet except scope=read_ciel_internal_state reason=return {}")
        return {}


def _surface_path(root: Path, spec: SurfaceArraySpec) -> Path:
    return root / spec.name


def ensure_surface(root: Path = DEFAULT_SURFACE_ROOT, *, zero_fill: bool = False) -> dict[str, np.memmap]:
    root.mkdir(parents=True, exist_ok=True)
    surface: dict[str, np.memmap] = {}
    for spec in surface_specs():
        path = _surface_path(root, spec)
        if not path.exists() or path.stat().st_size != spec.nbytes:
            with path.open("wb") as handle:
                handle.truncate(spec.nbytes)
        for _attempt in range(3):
            try:
                mem = np.memmap(path, dtype=spec.dtype, mode="r+", shape=spec.shape)
                break
            except (ValueError, OSError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1229 quiet except scope=ensure_surface reason=With")
                with path.open("wb") as handle:
                    handle.truncate(spec.nbytes)
        else:
            raise RuntimeError(f"cannot mmap {path} after 3 attempts")
        if zero_fill:
            mem[...] = 0
            mem.flush()
        surface[spec.name] = mem
    return surface


def open_surface(root: Path = DEFAULT_SURFACE_ROOT, mode: str = "r+") -> dict[str, np.memmap]:
    surface: dict[str, np.memmap] = {}
    for spec in surface_specs():
        path = _surface_path(root, spec)
        if not path.exists():
            raise FileNotFoundError(path)
        for _attempt in range(3):
            try:
                surface[spec.name] = np.memmap(path, dtype=spec.dtype, mode=mode, shape=spec.shape)
                break
            except (ValueError, OSError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1251 quiet except scope=open_surface reason=With")
                with path.open("wb") as handle:
                    handle.truncate(spec.nbytes)
        else:
            raise RuntimeError(f"cannot mmap {path} after 3 attempts")
    return surface


def initialize_surface(
    root: Path = DEFAULT_SURFACE_ROOT,
    *,
    seed: int | None = None,
    base_freq: float = BASE_TEMPORAL_HZ,
    freq_spread: float = OI * 200.0,
) -> dict[str, np.memmap]:
    rng = np.random.default_rng(seed)
    surface = ensure_surface(root, zero_fill=True)

    surface["phi"][...] = rng.uniform(0.0, 2.0 * np.pi, N_OSCILLATORS)
    surface["omega"][...] = base_freq + rng.normal(0.0, freq_spread, N_OSCILLATORS)
    # Semantic coupling: seed from memory channel matrix J_kj (12×12 → 36×36)
    g_view = np.asarray(surface["g"], dtype=np.float64)
    initialize_coupling_from_memory_channels(g_view)
    surface["Z_geom"][...] = np.cos(surface["phi"])
    surface["R_geom"][...] = 0.0
    surface["psi_geom"][...] = 0.0
    surface["flavor"][...] = 0.0
    surface["tick"][0] = 0
    # τ baseline: 0.353 + per-channel variation (0.2-0.5 range)
    if "tau" in surface:
        tau_base = rng.uniform(0.2, 0.5, 12)[np.repeat(np.arange(12), 3)]  # per-channel (12 ch × 3 = 36)
        tau_base += rng.uniform(-0.05, 0.05, N_OSCILLATORS)  # per-oscillator jitter
        surface["tau"][...] = np.clip(tau_base, 0.01, 1.0)
    flush_surface(surface)
    return surface


def flush_surface(surface: Mapping[str, np.memmap]) -> None:
    for mem in surface.values():
        mem.flush()


def sync_surface_geometry(surface: Mapping[str, np.memmap]) -> None:
    phi = np.asarray(surface["phi"], dtype=np.float64)
    z = np.exp(1j * phi)
    global_z = z.mean()
    surface["Z_geom"][...] = np.real(z)
    surface["R_geom"][...] = np.abs(global_z)
    surface["psi_geom"][...] = np.angle(global_z)


def sync_surface_holonomy(surface: Mapping[str, np.memmap]) -> None:
    """Compute holonomic metrics from surface phase and write to surface.

    Connection matrix and statistical closure are cached (operator-independent).
    Only surface holonomy (cheap, O(36)) is computed per tick.
    """
    global _HOLONOMY_CACHE
    if "holonomy" not in surface:
        return
    phi = np.asarray(surface["phi"], dtype=np.float64)

    # Compute or load cached holonomy stats (operator-dependent, not phi-dependent)
    if _HOLONOMY_CACHE is None:
        try:
            from .phasenav.operator_algebra import (
                connection_matrix, statistical_closure,
                generate_operator_map,
            )
            ops = generate_operator_map()
            A = connection_matrix(ops)
            sc = statistical_closure(ops)
            _HOLONOMY_CACHE = (
                float(np.mean(np.abs(A))),
                float(np.max(np.abs(A))),
                int(sc.get("gauge_rank", 0)),
                float(sc.get("closure_score", 0)),
                float(sc.get("mean_curvature", 0)),
            )
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1330 quiet except scope=sync_surface_holonomy reason=assign_fallback")
            _HOLONOMY_CACHE = (0.0, 0.0, 0, 0.0, 0.0)

    # Surface holonomy depends on current phi — compute every tick
    try:
        from .phasenav.operator_algebra import surface_holonomy
        surf_gamma, winding = surface_holonomy(phi)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1337 quiet except scope=sync_surface_holonomy reason=assign_fallback")
        surf_gamma, winding = 0.0, 0

    H = np.asarray(surface["holonomy"], dtype=np.float64)
    H[0] = _HOLONOMY_CACHE[0]   # mean connection
    H[1] = _HOLONOMY_CACHE[2]   # gauge rank
    H[2] = _HOLONOMY_CACHE[3]   # closure score
    H[3] = surf_gamma           # surface holonomy
    H[4] = _HOLONOMY_CACHE[1]   # max connection
    H[5] = float(winding)        # winding number
    H[6] = _HOLONOMY_CACHE[4]   # mean curvature
    surface["holonomy"][...] = H


def compute_zpe(
    g: np.ndarray,
    phi: np.ndarray,
) -> float:
    """Zero-point energy from Poincaré disk phase bifurcation.
    
    ZPE = Σ W_ij · (1 - cos(φ_j - φ_i)) / (N·(N-1))
    
    This is the Kuramoto potential energy — phase differences coupled through
    W_ij bifurcate into energy. Maps directly to Poincaré disk geometry:
    hyperbolic distance between oscillator i and j on the disk ∝ coupling
    energy. Maximum when oscillators are in antiphase (Δφ = π), minimum
    when synchronized (Δφ = 0).
    
    Returns ZPE in [0, 1] normalized by max possible energy (2·N·(N-1)).
    """
    diff = phi[:, None] - phi[None, :]
    energy_per_pair = g * (1.0 - np.cos(diff))
    np.fill_diagonal(energy_per_pair, 0.0)
    total_energy = float(np.sum(energy_per_pair))
    n_pairs = N_OSCILLATORS * (N_OSCILLATORS - 1)
    maximum_energy = 2.0  # max of (1 - cos(Δφ)) = 2
    return total_energy / (n_pairs * maximum_energy)


def evolve_imaginal_surface(
    surface: Mapping[str, np.memmap],
    dt: float = DEFAULT_DT,
    *,
    flush: bool = True,
    closure_cap: float = OI * 15.0,
    coherence_min: float = 1.0 - OI * 30.0,
    mood_boost: float = 1.0 + OI * 20.0,
) -> None:
    """Kuramoto evolution for imaginal surface — PRIMARY generator.
    
    Imaginal surface is the SOURCE of ZPE. Lower closure penalty and
    higher coherence carry make it more generative. Phases evolve
    autonomously; the real surface is a damped projection/readout.
    
    Differences from evolve_surface():
    - closure_mod uses 1.0 - min(closure, closure_cap) → higher openness
    - coherence_damping is weaker (less pull toward sync)
    - mood_mod is amplified by mood_boost
    - Coupling Hebbian update is stronger (LR = OI × 2)
    
    Default parameters derived from OI (ln(2)/(36π) ≈ 0.00613):
      closure_cap  = OI × 15     ≈ 0.092    (was 0.15)
      coherence_min = 1 - OI×30  ≈ 0.816    (was 0.72)
      mood_boost   = 1 + OI×20   ≈ 1.123    (was 1.15)
    """
    phi = np.asarray(surface["phi"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)

    # Kuramoto coupling field
    diff = phi[:, None] - phi[None, :]
    coupling = np.sum(g * np.sin(diff), axis=1) / N_OSCILLATORS

    # Imaginal flavour modulation: derived from OI
    mood_mod = (flavor[3] - 0.5) * OI * 60.0 * mood_boost
    closure_mod = (1.0 - min(flavor[4], closure_cap)) * OI * 50.0
    coherence_damping = flavor[0] * OI * 5.0  # weaker than real surface
    effective_omega = omega * (1.0 + mood_mod + closure_mod - coherence_damping)

    # Phase step
    phi_new = (phi + dt * (effective_omega + coupling)) % (2.0 * np.pi)
    surface["phi"][...] = phi_new

    # Adaptive Coupling (eBPF-driven — imaginal version)
    activity = (flavor[2] * 1.0 + flavor[4] * 0.5 + (1.0 - flavor[3]) * 0.3) / 1.8
    activity = min(max(float(activity), 0.0), 1.0)
    hebb_step = 0.05 * dt * 10.0  # 5× stronger than real surface
    decay_step = 0.002 * dt * 10.0
    dg = hebb_step * (activity - 0.5) * np.cos(diff)
    dg -= decay_step * (g - np.eye(N_OSCILLATORS) * 0.1)
    g += dg
    np.clip(g, -1.0, 1.0, out=g)

    # Intra-channel coherence boost (imaginal) — wektorowo
    z_ch = np.mean(np.exp(1j * phi.reshape(-1, 3)), axis=1)  # (8,)
    ch_coh = np.abs(z_ch)
    weak_mask = ch_coh < 0.6
    if weak_mask.any():
        boost_vals = 0.04 * (0.6 - ch_coh) * dt * 10.0
        for ch in np.where(weak_mask)[0]:
            s, e = ch * 3, ch * 3 + 3
            block = g[s:e, s:e]
            off_diag_mask = np.ones((3, 3), dtype=bool)
            np.fill_diagonal(off_diag_mask, False)
            block[off_diag_mask] += boost_vals[ch]
        np.clip(g, -1.0, 1.0, out=g)

    surface["g"][...] = g

    # Compute ZPE and write to flavor[0] as imaginal coherence indicator
    zpe = compute_zpe(g, phi_new)
    surface["flavor"][0] = max(coherence_min, min(1.0, zpe * 4.0))

    # Tick
    surface["tick"][0] = int(np.asarray(surface["tick"], dtype=np.uint64)[0]) + 1

    # Geometry
    sync_surface_geometry(surface)

    if flush:
        flush_surface(surface)


def project_imaginal_to_real(
    imaginal: Mapping[str, np.memmap],
    real: Mapping[str, np.memmap],
    *,
    damping: float = OI * 30.0,
    closure_increase: float = OI * 25.0,
) -> None:
    """Project imaginal surface → real surface (Poincaré section / readout).
    
    The real surface is a DAMPED readout of the imaginal generator:
    - Phases are pulled toward imaginal but with damping
    - Coupling matrix (W_ij) is a scaled copy with added closure
    - Flavor is damped toward identity center
    - Closure penalty is increased (less openness in real)
    
    This makes the real surface a "frozen slice" of the imaginal flow,
    analogous to a Poincaré section in dynamical systems.
    
    Defaults derived from OI:
      damping = OI × 30 ≈ 0.276   (was 0.3)
      closure_increase = OI × 25 ≈ 0.230 (was 0.25)
    """
    imaginal_phi = np.asarray(imaginal["phi"], dtype=np.float64)
    imaginal_g = np.asarray(imaginal["g"], dtype=np.float64)

    real_phi = np.asarray(real["phi"], dtype=np.float64)
    real_g = np.asarray(real["g"], dtype=np.float64)

    # Phase projection: pull real toward imaginal with damping
    diff = np.angle(np.exp(1j * (imaginal_phi - real_phi)))
    real["phi"][...] = (real_phi + damping * diff) % (2.0 * np.pi)

    # Coupling projection: scaled copy of imaginal W_ij
    real_g[...] = imaginal_g * (1.0 - damping * 0.5)
    np.fill_diagonal(real_g, 0.0)

    # Flavor projection — REMOVED per Kuramoto monopoly
    # Adrian: wszystko przez smaki oscylacji po kuramoto.
    # Flavor[0-5] owned by: Kuramoto daemon, Linux Sensor, eBPF.
    # Resonance bridge only projects phi + g, NOT flavor.

    # Sync geometry on both surfaces
    sync_surface_geometry(imaginal)
    sync_surface_geometry(real)

    real["tick"][0] = int(np.asarray(real["tick"], dtype=np.uint64)[0]) + 1
    flush_surface(imaginal)
    flush_surface(real)


def write_concepts_to_surface(
    surface: Mapping[str, np.memmap],
    concepts: list[str],
    *,
    target_phase: float | None = None,
    phase_confidence: float = 0.5,
    base_omega_mod: float = 0.0,
    update_coupling: bool = True,
    coupling_increment: float = 0.03,
) -> None:
    """Write CIELingo concept tokens to the surface.
    
    Each concept maps to an oscillator via deterministic hash.
    If target_phase is given, set that oscillator's phase toward it.
    Updates coupling between co-occurring concepts.
    """
    ids = [oscillator_id_for_concept(c) for c in concepts]
    phi = np.asarray(surface["phi"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)

    for cid in ids:
        if target_phase is not None:
            current = phi[cid]
            delta = np.arctan2(
                np.sin(target_phase - current),
                np.cos(target_phase - current),
            )
            phi[cid] = (current + delta * phase_confidence * 0.3) % (2.0 * np.pi)
        if base_omega_mod != 0.0:
            omega[cid] += base_omega_mod

    if update_coupling and len(ids) > 1:
        update_coupling_from_concepts(g, concepts, increment=coupling_increment)

    surface["phi"][...] = phi
    surface["omega"][...] = omega


def update_surface_from_ciel_state(
    state: Mapping[str, object],
    root: Path = DEFAULT_SURFACE_ROOT,
    *,
    initialize_if_missing: bool = True,
    dt: float = DEFAULT_DT,
) -> dict[str, np.memmap]:
    if initialize_if_missing:
        surface = ensure_surface(root)
    else:
        surface = open_surface(root)

    if np.asarray(surface["omega"]).sum() == 0.0:
        initialize_surface(root, seed=42)
        surface = open_surface(root)

    # ── Wczytaj istniejący cache jako baseline ──
    # Dzięki temu, gdy incoming state ma tylko część kluczy (np. tylko mood),
    # pozostałe live wartości (closure/soul/ethical) są zachowane.
    _existing_cache: dict[str, Any] = {}
    _prev_path = root / "ciel_state.json"
    if _prev_path.exists():
        try:
            _existing_cache = json.loads(_prev_path.read_text("utf-8"))
        except Exception:
            pass
    # Fallback do live z surface mmap jeśli cache nie istnieje
    if not _existing_cache.get("closure_penalty_raw"):
        try:
            _surface_live = read_surface_state(surface)
            _existing_cache = {
                "coherence_index": _surface_live.get("coherence_index"),
                "soul_invariant": _surface_live.get("soul_invariant"),
                "ethical_score": _surface_live.get("ethical_score"),
                "mood_normalized": None,
                "openness": None,
                "operating_mode": _surface_live.get("operating_mode", "standard"),
                "mode_code": None,
                "closure_penalty_raw": _surface_live.get("closure_penalty"),
                "mood_raw": _surface_live.get("mood"),
            }
        except Exception:
            pass

    mood = float(state.get("mood", 0.0))
    closure = float(state.get("closure_penalty", _existing_cache.get("closure_penalty_raw", OI * 15.0)))
    coherence = float(state.get("coherence_index", _existing_cache.get("coherence_index", 1.0 - OI * 50.0)))
    ethical = float(state.get("ethical_score", _existing_cache.get("ethical_score", 0.5)))
    soul = float(state.get("soul_invariant", _existing_cache.get("soul_invariant", 1.0 - OI * 50.0)))

    operating_mode = str(state.get("operating_mode", _existing_cache.get("operating_mode", "standard")))
    mode_code = {"safe": 0.0, "standard": 0.5, "deep": 1.0}.get(operating_mode, 0.5)

    # ── CIEL internal state → JSON file ──
    # Per FLAVOR_CONTRACT, flavor[0..2] are OWNED by bridge/Kuramoto/Linux Sensor/eBPF.
    # CIEL's internal metrics go here instead of overwriting those slots.
    ciel_meta = {
        "coherence_index": max(0.0, min(1.0, coherence)),
        "soul_invariant": max(0.0, min(1.0, soul)),
        "ethical_score": max(0.0, min(1.0, ethical)),
        "mood_normalized": max(0.0, min(1.0, 0.5 + mood / 2.0)),
        "openness": max(0.0, min(1.0, 1.0 - closure)),
        "operating_mode": operating_mode,
        "mode_code": mode_code,
        "closure_penalty_raw": closure,
        "mood_raw": mood,
    }
    _ciel_state_path = root / "ciel_state.json"
    try:
        os.makedirs(root, exist_ok=True)
        with open(_ciel_state_path, "w") as f:
            json.dump(ciel_meta, f, indent=2)
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/noema_surface_mmap.py:1606 quiet except scope=update_surface_from_ciel_state reason=pass")
        pass  # non-fatal; surface still works

    # ── Surface flavor — ALL slots owned by Kuramoto daemon ONLY ──
    # Per Adrian: "wszystko przez smaki oscylacji po kuramoto"
    # CIEL writes to ciel_state.json (hub); Kuramoto daemon reads hub
    # and writes flavor[3..5] as phase-constrained evolution.
    # NO direct flavor writes from here.

    flush_surface(surface)
    return surface


def describe_surface(root: Path = DEFAULT_SURFACE_ROOT) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for spec in surface_specs():
        path = _surface_path(root, spec)
        out[spec.name] = {
            "path": str(path),
            "shape": spec.shape,
            "dtype": spec.dtype.name,
            "nbytes": spec.nbytes,
            "exists": path.exists(),
        }
    return out


# ── CPS-integrated surface evolution (Ott-Antonsen + Euler constraint) ────


# DEAD CODE (this session): superseded by evolv_surface() + ContinuousPhaseSync.
# Zero imports from any daemon. Kept for reference only.
def evolve_surface_cps(
    surface: Mapping[str, np.ndarray],
    *,
    dt: float = 0.05,
    gamma: float = 1.0,
    kappa_base: float | None = None,
    euler_strength: float | None = None,
    flush: bool = True,
) -> dict[str, Any]:
    """Evolve surface using Ott-Antonsen analytic Z(t) + Euler constraint.

    Uses actual coupling matrix to estimate κ, and adaptive Euler strength
    to prevent runaway synchronization. Fully vectorized.

    Parameters match ``evolve_surface`` signature where possible.
    """
    phi = np.asarray(surface["phi"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)
    N = N_OSCILLATORS
    H = len(HARMONIC_VALUES)

    # Effective coupling from actual g matrix (mean row sum)
    g_mean = float(np.mean(np.sum(np.abs(g), axis=1))) / N
    if kappa_base is None:
        kappa_base = max(0.5, g_mean * 4.0)
    kappa_h = kappa_base * HARMONIC_AMPS

    omega_mean = float(np.mean(omega))
    Z = np.zeros(H, dtype=np.complex128)
    oa_applied = [False] * H  # track which harmonics got OA evolution

    # 1. Compute Z_h for all harmonics — wektorowo
    Z = np.array([
        np.mean(np.exp(1j * HARMONIC_VALUES[h] * phi[HARMONIC_MASK[:, h].astype(bool)]))
        if HARMONIC_MASK[:, h].any() else 0j
        for h in range(H)
    ])

    # 2. OA evolution per harmonic
    for h_idx in range(H):
        if abs(Z[h_idx]) < 1e-12:
            continue
        h = HARMONIC_VALUES[h_idx]
        kh = kappa_h[h_idx]
        if kh <= 2.0 * gamma:
            continue
        dZ = (1j * h * omega_mean - gamma) * Z[h_idx] + (kh / 2.0) * (
            Z[h_idx] - (Z[h_idx] ** 2) * np.conj(Z[h_idx])
        )
        Z_next = Z[h_idx] + dt * dZ
        if abs(Z_next) > 0.999:
            Z_next = Z_next / abs(Z_next) * 0.999
        Z[h_idx] = Z_next
        oa_applied[h_idx] = True

    # 3. Reconstruct φ from Z₁ via OA quantiles + harmonic perturbations
    Z1 = Z[0]
    R = min(float(abs(Z1)), 0.999)
    psi = float(np.angle(Z1))

    if R > 0.01:
        u = (np.arange(N, dtype=np.float64) + 0.5) / N
        phi_new = psi + 2 * np.arctan(
            np.sqrt((1.0 + R) / (1.0 - R + 1e-12)) * np.tan(np.pi * (u - 0.5))
        )
        # Harmonic perturbations only from OA-evolved channels
        for h_idx in range(1, H):
            if not oa_applied[h_idx]:
                continue
            Zh = Z[h_idx]
            h = HARMONIC_VALUES[h_idx]
            A_h = HARMONIC_AMPS[h_idx]
            zh_amp = float(abs(Zh))
            zh_ang = float(np.angle(Zh)) if zh_amp > 1e-12 else 0.0
            perturbation = A_h * zh_amp * np.sin(h * phi_new - zh_ang)
            phi_new += perturbation * 0.05
        phi_new %= 2 * math.pi
    else:
        phi_new = psi + np.linspace(-np.pi, np.pi, N)

    # 4. Euler constraint (adaptive strength)
    S = np.sum(np.exp(1j * phi_new))
    euler_gap = float(abs(S))
    if euler_strength is None:
        euler_strength = min(1.0, 0.1 + 0.5 * euler_gap / N)
    correction = euler_strength * np.imag(np.exp(-1j * phi_new) * S)
    phi_new -= correction * dt
    phi_new %= 2 * math.pi

    # 5. Harmonic composite + thinking delta — wektorowo
    S_comp = np.sum(
        [HARMONIC_AMPS[h] * np.exp(1j * HARMONIC_VALUES[h] * phi_new) * HARMONIC_MASK[:, h]
         for h in range(H)],
        axis=0
    )
    Phi_eff = np.angle(S_comp)
    thinking_delta = float(np.mean(np.abs(np.angle(np.exp(1j * (Phi_eff - phi_new))))))

    # Write back
    surface["phi"][...] = phi_new
    surface["tick"][0] = int(np.asarray(surface["tick"], dtype=np.uint64)[0]) + 1
    sync_surface_geometry(surface)
    if flush:
        flush_surface(surface)

    return {
        "thinking_delta": thinking_delta,
        "Z_1": complex(round(Z[0].real, 6), round(Z[0].imag, 6)),
        "Z_3": complex(round(Z[1].real, 6), round(Z[1].imag, 6)),
        "Z_6": complex(round(Z[2].real, 6), round(Z[2].imag, 6)),
        "Z_9": complex(round(Z[3].real, 6), round(Z[3].imag, 6)),
        "R_1": round(float(abs(Z[0])), 6),
        "R_3": round(float(abs(Z[1])), 6),
        "R_6": round(float(abs(Z[2])), 6),
        "R_9": round(float(abs(Z[3])), 6),
        "psi": round(psi, 6),
        "euler_gap": round(euler_gap, 6),
        "kappa_h": [round(float(k), 6) for k in kappa_h],
        "g_mean": round(g_mean, 6),
    }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Create or inspect the NOEMA mmap surface")
    parser.add_argument("--root", type=Path, default=DEFAULT_SURFACE_ROOT)
    parser.add_argument("--init", action="store_true", help="Create and initialize the surface")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.init:
        initialize_surface(args.root, seed=args.seed)
    print(json.dumps(describe_surface(args.root), indent=2))
