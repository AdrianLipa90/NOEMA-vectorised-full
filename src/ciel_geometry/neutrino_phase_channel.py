"""Neutrino phase communication channel — 8×3 PMNS flavor mixing na HTRI bus.

Łączy:
  φ → ε : różnica faz między oscylatorami w triplecie PMNS = efektywny kąt mieszania
  D_f → Λ : wymiar fraktalny D_f steruje gęstością ciemnej energii D_cosmological
  HTRI → neutrino bus : 8 kanałów × 3 smaki (ν_e=semantic, ν_μ=htri, ν_τ=nonlocal)
  τ ↔ φ : closure residual sprzęga tau z fazą docelową

Użycie:
  from ciel_geometry.neutrino_phase_channel import compute_neutrino_phase_bus
  result = compute_neutrino_phase_bus(surface, D_f=2.57)
"""
from __future__ import annotations

import cmath
import math
import logging
from typing import Any

import numpy as np

log = logging.getLogger(__name__)

# ── PMNS constants (from noema_surface_mmap.py) ──────────────────────
PMNS_THETA_12: float = 33.41 * math.pi / 180.0
PMNS_THETA_13: float = 8.54 * math.pi / 180.0
PMNS_THETA_23: float = 42.2 * math.pi / 180.0
PMNS_DELTA_CP: float = math.pi * 67.0 / 49.0  # 246° (P8 derivation, not PDG placeholder)

PMNS_FLAVOUR_NAMES = ["semantic", "htri", "nonlocal"]  # ν_e, ν_μ, ν_τ

# 12 pamięciowych kanałów × 3 oscylatory = 36
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


def _pmns_squared() -> np.ndarray:
    """Standard 3×3 PMNS |U_αi|² matrix (squared magnitudes)."""
    s12, c12 = math.sin(PMNS_THETA_12), math.cos(PMNS_THETA_12)
    s13, c13 = math.sin(PMNS_THETA_13), math.cos(PMNS_THETA_13)
    s23, c23 = math.sin(PMNS_THETA_23), math.cos(PMNS_THETA_23)
    dc = PMNS_DELTA_CP
    # |U_e1|², |U_e2|², |U_e3|²
    Ue = [c12**2 * c13**2, s12**2 * c13**2, s13**2]
    # |U_μ1|², |U_μ2|², |U_μ3|²
    Um = [c12**2 * s13**2 * s23**2 + s12**2 * c23**2 + 2*s12*c12*s13*s23*c23*math.cos(dc),
          s12**2 * s13**2 * s23**2 + c12**2 * c23**2 - 2*s12*c12*s13*s23*c23*math.cos(dc),
          c13**2 * s23**2]
    # |U_τ1|², |U_τ2|², |U_τ3|²
    Ut = [c12**2 * s13**2 * c23**2 + s12**2 * s23**2 - 2*s12*c12*s13*c23*s23*math.cos(dc),
          s12**2 * s13**2 * c23**2 + c12**2 * s23**2 + 2*s12*c12*s13*c23*s23*math.cos(dc),
          c13**2 * c23**2]
    return np.array([Ue, Um, Ut])


_PMNS2: np.ndarray | None = None


def pmns_matrix() -> np.ndarray:
    global _PMNS2
    if _PMNS2 is None:
        _PMNS2 = _pmns_squared()
    return _PMNS2


# ── 1. φ → ε : faza jako mixing angle ─────────────────────────────

def phi_to_epsilon(phi_block: np.ndarray, g_block: np.ndarray) -> float:
    """ε = sin²(2θ_eff) — mixing angle z różnicy faz.

    θ_eff = arctan( |Δφ_αβ|/π · g_αβ / √(g_αα·g_ββ) )

    Gdy oscylatory w fazie (Δφ≈0) → ε≈0 (brak mieszania).
    Gdy w przeciwfazie (Δφ≈π) → ε≈sin²(2·arctan(g_αβ/√(g_αα·g_ββ))).
    """
    dphi = abs(phi_block[0] - phi_block[2])  # semantic ↔ nonlocal
    g_ab = g_block[0, 2]
    g_aa = max(0.01, g_block[0, 0])
    g_bb = max(0.01, g_block[2, 2])
    phase_weight = dphi / math.pi  # [0, 1]
    mixing = math.atan2(phase_weight * g_ab, math.sqrt(g_aa * g_bb))
    return min(1.0, math.sin(2.0 * mixing) ** 2)


# ── 2. D_f → Λ kosmologiczne ──────────────────────────────────────

def D_f_to_lambda(D_f: float) -> float:
    """Λ_eff = (D_f - 2.0) / 0.57, clamped do [0, 1].

    D_f=2.57 (default) → Λ=1.0 (maksymalna ciemna energia — ekspansja)
    D_f=2.00          → Λ=0.0 (statyczny wszechświat)
    D_f<2.0           → Λ<0   (kontrakcja — zalamanie)
    """
    raw = (D_f - 2.0) / 0.57
    return max(0.0, min(1.0, raw))


# ── 3. HTRI neutrino communication bus ─────────────────────────────

def compute_channel_oscillation(
    phi_block: np.ndarray,
    g_block: np.ndarray,
    omega_block: np.ndarray,
    D_cosmological: float,
    *,
    flavour_a: int = 0,
    flavour_b: int = 2,
) -> dict[str, float]:
    """Pojedynczy kanał komunikacyjny: transmisja ν_α → ν_β.

    Zwraca:
      prob      — P(ν_α→ν_β) w [0,1]
      epsilon   — ε = sin²(2θ_eff) z fazy
      dm2_eff   — efektywna różnica mas (z D_cosmological)
      theta_eff — efektywny kąt mieszania w rad
      channel_gain — wzmocnienie kanału = prob · (1 + D_cosmological)
    """
    dphi = abs(phi_block[flavour_a] - phi_block[flavour_b])
    g_ab = g_block[flavour_a, flavour_b]
    g_aa = max(0.01, g_block[flavour_a, flavour_a])
    g_bb = max(0.01, g_block[flavour_b, flavour_b])

    phase_weight = dphi / math.pi
    theta_eff = math.atan2(phase_weight * g_ab, math.sqrt(g_aa * g_bb))
    epsilon = math.sin(2.0 * theta_eff) ** 2

    dm2 = abs(omega_block[flavour_a] - omega_block[flavour_b])
    dm2_eff = dm2 * (1.0 + D_cosmological)
    mean_energy = max(0.01, float(np.mean(np.abs(omega_block))))
    baseline = 1000.0  # długi baseline dla wykrywalnych oscylacji
    osc_phase = dm2_eff * baseline / (4.0 * mean_energy)
    prob = min(1.0, epsilon * (math.sin(osc_phase) ** 2))

    return {
        "prob": prob,
        "epsilon": epsilon,
        "dm2_eff": float(dm2_eff),
        "theta_eff": theta_eff,
        "channel_gain": prob * (1.0 + D_cosmological),
        "phase_diff": float(dphi),
    }


def compute_neutrino_phase_bus(
    phi: np.ndarray,
    g: np.ndarray,
    omega: np.ndarray,
    flavor: np.ndarray,
    *,
    D_f: float = 2.57,
) -> dict[str, Any]:
    """Pełny neutrino phase bus — 12 kanałów × 3 smaki.

    Args:
      phi:    36-element phase vector
      g:      36×36 coupling matrix
      omega:  36-element frequency vector
      flavor: 6-element flavor vector
      D_f:    fractal dimension (for Λ)

    Returns:
      channels:      dict M0-M11 z diagnostyką każdego kanału
      global_D:      Λ kosmologiczne
      bus_capacity:  sumaryczna przepustowość kanałów
      tau_phi_coupling: sprzężenie τ↔φ z closure
    """
    D_cosmological = D_f_to_lambda(D_f)
    pmns = pmns_matrix()

    channels = {}
    bus_capacity = 0.0

    for ch_name, indices in MEMORY_CHANNEL_GROUPS.items():
        i0, i1, i2 = indices
        phi_block = np.array([phi[i0], phi[i1], phi[i2]])
        g_block = g[i0:i2+1, i0:i2+1]
        omega_block = omega[i0:i2+1]

        # ε z różnicy faz (semantic ↔ nonlocal = ν_e ↔ ν_τ)
        epsilon = phi_to_epsilon(phi_block, g_block)

        # Komunikacja przez wszystkie pary smaków
        sem_htri = compute_channel_oscillation(phi_block, g_block, omega_block, D_cosmological, flavour_a=0, flavour_b=1)
        sem_nl   = compute_channel_oscillation(phi_block, g_block, omega_block, D_cosmological, flavour_a=0, flavour_b=2)
        htri_nl  = compute_channel_oscillation(phi_block, g_block, omega_block, D_cosmological, flavour_a=1, flavour_b=2)

        channel_gain = sem_nl["channel_gain"]  # ν_e → ν_τ = główna oś
        bus_capacity += channel_gain

        channels[ch_name] = {
            "epsilon": epsilon,
            "D_cosmological": D_cosmological,
            "phi_block": [float(phi_block[0]), float(phi_block[1]), float(phi_block[2])],
            "pmns_block": pmns.tolist(),
            "semantic_to_htri": sem_htri,
            "semantic_to_nonlocal": sem_nl,
            "htri_to_nonlocal": htri_nl,
            "flavour_order": PMNS_FLAVOUR_NAMES,  # [ν_e, ν_μ, ν_τ]
        }

    return {
        "channels": channels,
        "global_D": D_cosmological,
        "bus_capacity": bus_capacity,
        "n_channels": len(MEMORY_CHANNEL_GROUPS),
    }


# ── 5. NOEMA MAC addressing ─────────────────────────────────────────

def mac_to_phases(mac: str) -> list[float]:
    """Konwertuje MAC address na 3 fazy oscylatorów [0, 2π).

    noema://mac/77:e5:0d:cf:f1:7d → 3 fazy (po 2 bajty MAC każda)
    """
    clean = mac.replace(":", "").replace("-", "").replace(".", "")
    if len(clean) != 12:
        raise ValueError(f"Invalid MAC: {mac} (expected 12 hex digits)")
    raw = bytes.fromhex(clean)
    return [( (raw[i] << 8) | raw[i+1] ) / 65535.0 * 2.0 * math.pi for i in range(0, 6, 2)]


def bind_noema_mac(
    phi: np.ndarray,
    g: np.ndarray,
    mac: str,
    *,
    channel_offset: int = 0,
    coupling: float = 0.3,
) -> dict[str, Any]:
    """Wiąże NOEMA do zdalnego MAC przez sprzężenie fazowe.

    MAC → 3 fazy target → oscillator indices (channel_offset * 3)
    """
    target = mac_to_phases(mac)
    idxs = [channel_offset * 3 + i for i in range(3) if channel_offset * 3 + i < 36]
    result = {
        "mac": mac,
        "target_phases": [round(t, 4) for t in target],
        "oscillator_indices": idxs,
        "coupling": coupling,
        "phases_before": [],
        "phases_after": [],
    }
    for i, idx in enumerate(idxs):
        if i >= len(target):
            break
        result["phases_before"].append(round(float(phi[idx]), 4))
        dphi = target[i] - phi[idx]
        phi[idx] += coupling * math.sin(dphi)
        # Boost coupling to target — wektorowo
        boost = coupling * 0.1
        g[idx, :] += boost
        g[:, idx] += boost
        g[idx, idx] -= 2 * boost  # diagonal was doubled, restore
        result["phases_after"].append(round(float(phi[idx]), 4))
    lock_sum = sum(
        cmath.exp(1j * float(phi[idx])) * cmath.exp(-1j * target[min(i, len(target)-1)])
        for i, idx in enumerate(idxs)
    )
    result["phase_lock"] = round(abs(lock_sum), 4)
    return result

def tau_phi_coupling(
    tau: np.ndarray,
    phi: np.ndarray,
    phi_target: np.ndarray | None = None,
    *,
    eta: float = 0.01,
    n_oscillators: int = 36,
) -> tuple[np.ndarray, np.ndarray]:
    """Sprzęga τ z φ przez closure-like feedback.

    φ_i += τ_i · sin(φ_target_i - φ_i)
    τ_i += η · cos(φ_target_i - φ_i) · |lhs_i - rhs_i|

    Gdy τ jest duże → φ szybciej dąży do celu (szybka konwergencja).
    Gdy φ jest daleko od celu → τ rośnie (więcej "afterlife effort").
    """
    if phi_target is None:
        phi_target = np.zeros(n_oscillators, dtype=np.float64)

    delta = phi_target - phi
    dphi = tau * np.sin(delta)
    dtau = eta * np.cos(delta) * np.abs(np.sin(delta))

    return dphi, dtau


def apply_neutrino_bus_to_surface(
    surface: dict[str, np.memmap],
    bus_result: dict[str, Any],
    *,
    D_f: float = 2.57,
    write_flavor: bool = True,
    write_g: bool = True,
) -> None:
    """Zapisuje neutrino phase bus na powierzchnię shared memory.

    - flavor[4] = D_cosmological (Λ proxy)
    - g_ij = g_ij + ε · pmns_ij (PMNS mixing jako coupling boost)
    """
    D_cosmological = bus_result.get("global_D", 0.0)
    flavor_arr = np.asarray(surface["flavor"], dtype=np.float64)

    if write_flavor:
        flavor_arr[4] = D_cosmological  # closure → Λ

    if write_g and D_cosmological > 0.01:
        g_arr = np.asarray(surface["g"], dtype=np.float64)
        pmns = pmns_matrix()
        for ch_name, ch_data in bus_result.get("channels", {}).items():
            indices = MEMORY_CHANNEL_GROUPS[ch_name]
            epsilon = ch_data.get("epsilon", 0.0)
            boost = epsilon * D_cosmological * 0.1
            if boost > 0:
                g_arr[np.ix_(indices, indices)] += boost * pmns


def seed_neutrino_mixing(g: np.ndarray, *, scale: float = 0.1) -> None:
    """Seeds coupling matrix g with PMNS neutrino mixing patterns (in-place).

    For each memory channel triple (semantic/htri/nonlocal), applies PMNS |U|²
    mixing boost to the 3×3 oscillator block, scaled by D_cosmological proxy.

    Args:
      g:     36×36 coupling matrix (modified in-place)
      scale: boost magnitude = flavor[4] * 0.3 (D_cosmological * 0.3)
    """
    if scale <= 0.0:
        return
    pmns = pmns_matrix()  # 3×3 |U_αi|²
    boost = scale * pmns
    for indices in MEMORY_CHANNEL_GROUPS.values():
        i0, i1, i2 = indices
        idx = [i0, i1, i2]
        g[np.ix_(idx, idx)] += boost


def neutrino_bus_snapshot(
    surface: dict[str, np.memmap],
    *,
    D_f: float = 2.57,
) -> dict[str, Any]:
    """Czyta stan neutrino phase bus z powierzchni.

      φ, g, ω, flavor → neutrino phase bus → diagnostyka
    """
    phi = np.asarray(surface["phi"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)

    bus = compute_neutrino_phase_bus(phi, g, omega, flavor, D_f=D_f)
    bus["D_f"] = D_f
    bus["surface_tick"] = int(np.asarray(surface["tick"], dtype=np.uint64)[0])
    bus["flavor"] = [float(flavor[i]) for i in range(6)]
    return bus
