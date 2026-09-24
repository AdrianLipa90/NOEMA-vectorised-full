"""PhaseNav AGENT operator attractor — first-class core module for NOEMA.

Injektuje attractor dla AGENT operatora (M1, φ[3-5]) w ewolucję fazy:
  dφ_i/dt = ω_i + Σ g_ij sin(φ_j - φ_i) + K · sin(φ_target - φ_i)

Używany przez agent lock daemon i resonance bridge.

Wszystkie couplingi wyrażone jako wielokrotności OI = ln(2)/(24π) ≈ 0.00919:
  COUPLING_INTERNAL = 33 × OI  (M1↔M1, wewnętrzna koherencja AGENT)
  COUPLING_M0       = 22 × OI  (M1↔M0, AGENT↔TRANSFORM)
  COUPLING_M2       = 16 × OI  (M1↔M2, AGENT↔MEMORY)
  COUPLING_M6       = 11 × OI  (M1↔M6, AGENT↔IDENTITY)

Sekwencja {33, 22, 16, 11} — malejąca harmonicznie: 33/22 ≈ 3/2, 22/16 ≈ 11/8,
16/11 ≈ 1.45. Odpowiada chromatycznemu gradientowi kanałów M1→M0→M2→M6.
"""
from __future__ import annotations

import numpy as np

from .noema_surface_mmap import OI

# AGENT oscillator indices (M1 channel)
AGENT_OSCS = [3, 4, 5]
# Anchor channels for cross-coupling
ANCHOR_M0 = [0, 1, 2]    # TRANSFORM
ANCHOR_M2 = [6, 7, 8]    # MEMORY
ANCHOR_M6 = [18, 19, 20]  # IDENTITY

# M0↔M2 bridge oscillators
M0M2_M0 = [0, 1, 2, 12, 13, 14]  # percept
M0M2_M2 = [6, 7, 8, 15, 16, 17]  # memory
M0M2_BOTH = M0M2_M0 + M0M2_M2     # wszystkie 12

TARGET_PHASE = np.pi / 4
COUPLING_INTERNAL = 60.0 * OI  # ≈ 0.551 (2× boost)
COUPLING_M0 = 44.0 * OI         # ≈ 0.404 (2× boost)
COUPLING_M2 = 32.0 * OI         # ≈ 0.294 (2× boost)
COUPLING_M6 = 22.0 * OI         # ≈ 0.202 (2× boost)
COUPLING_M0M2 = 18.0 * OI       # ≈ 0.165 (percept↔memory bridge)
PHASE_LOCK_GAIN = 0.9           # zwiększone z 0.6 (kompensuje omega-adaptive coupling 0.50)
OMEGA_DAMP_TARGET = 2.0         # niższy target dla ω[3]
OMEGA_DAMP_RATE = 0.92          # szybszy damping

# ── M2 Memory isolation -- protect from CPU noise ──────────────────
M2_OSCS = [6, 7, 8]
M2_OMEGA_TARGET = 1.0           # stable baseline for memory oscillators
M2_PHASE_PULL_GAIN = 0.35       # how strongly to pull M2 toward its mean


def apply_agent_attractor(
    phi: np.ndarray,
    g: np.ndarray,
    omega: np.ndarray | None = None,
    *,
    target_phase: float = TARGET_PHASE,
    lock_gain: float = PHASE_LOCK_GAIN,
    coupling_internal: float = COUPLING_INTERNAL,
    coupling_m0: float = COUPLING_M0,
    coupling_m2: float = COUPLING_M2,
    coupling_m6: float = COUPLING_M6,
    coupling_m0m2: float = COUPLING_M0M2,
    damp_omega: bool = True,
) -> dict[str, np.floating | list[float] | float | bool | None]:
    """Apply AGENT attractor to phase/coupling/omega arrays (in-place).

    Wektoryzowana: wszystkie pętle per-oscylator zastąpione slice'ami numpy.

    Args:
        phi: 36-element phase array (modified in-place)
        g: 36×36 coupling matrix (modified in-place)
        omega: 36-element frequency array (modified in-place if damp_omega=True)
        target_phase: attractor phase target (default π/4)
        lock_gain: phase correction gain (default 0.6)
        damp_omega: whether to damp ω[3] toward OMEGA_DAMP_TARGET

    Returns:
        dict with attractor state metrics
    """
    m1 = phi[AGENT_OSCS].copy()  # wektorowo zamiast list comprehension

    # ── Phase lock toward target — wektorowo ──────────────────────────
    dphi = target_phase - phi[AGENT_OSCS]
    phi[AGENT_OSCS] = (phi[AGENT_OSCS] + lock_gain * np.sin(dphi)) % (2 * np.pi)

    # ── Reinforce couplings — slice'ami zamiast podwójnych pętli ──────
    # Internal M1↔M1 (bez diagonali)
    g[np.ix_(AGENT_OSCS, AGENT_OSCS)] = coupling_internal
    g[AGENT_OSCS, AGENT_OSCS] = 0.0  # self-coupling back to 0

    # M1 ↔ M0 (symetrycznie)
    g[np.ix_(AGENT_OSCS, ANCHOR_M0)] = coupling_m0
    g[np.ix_(ANCHOR_M0, AGENT_OSCS)] = coupling_m0

    # M1 ↔ M2
    g[np.ix_(AGENT_OSCS, ANCHOR_M2)] = coupling_m2
    g[np.ix_(ANCHOR_M2, AGENT_OSCS)] = coupling_m2

    # M1 ↔ M6
    g[np.ix_(AGENT_OSCS, ANCHOR_M6)] = coupling_m6
    g[np.ix_(ANCHOR_M6, AGENT_OSCS)] = coupling_m6

    # ── M0↔M2 attractor — percept↔memory bridge ──────────────────────
    g[np.ix_(M0M2_M0, M0M2_M2)] = coupling_m0m2
    g[np.ix_(M0M2_M2, M0M2_M0)] = coupling_m0m2

    # Mean phase of M0, M2 and their midpoint — wektorowo
    z_m0 = np.mean(np.exp(1j * phi[M0M2_M0]))
    z_m2 = np.mean(np.exp(1j * phi[M0M2_M2]))
    bridge_target = np.angle(z_m0 + z_m2)
    dphi_bridge = bridge_target - phi[M0M2_BOTH]
    phi[M0M2_BOTH] = (phi[M0M2_BOTH] + 0.3 * np.sin(dphi_bridge)) % (2 * np.pi)

    # ── M2 Memory isolation — protect from CPU noise ────────────────
    # Pull φ[6,7,8] toward their own mean to resist linux-sensor overwrite
    m2_phi = phi[M2_OSCS]
    m2_z = np.mean(np.exp(1j * m2_phi))
    m2_mean_angle = np.angle(m2_z)
    dphi_m2 = m2_mean_angle - m2_phi
    phi[M2_OSCS] = (m2_phi + M2_PHASE_PULL_GAIN * np.sin(dphi_m2)) % (2 * np.pi)

    # Stable frequency for M2 — zamiast CPU noise
    if omega is not None:
        omega[M2_OSCS] = np.float64(M2_OMEGA_TARGET)

    # ── Damp AGENT cluster ω[3,4,5] ──────────────────────────────────
    if damp_omega and omega is not None:
        for idx in AGENT_OSCS:
            omega[idx] = np.float64(max(0.5, min(float(omega[idx]) * OMEGA_DAMP_RATE, OMEGA_DAMP_TARGET)))

    coh = abs(np.mean(np.exp(1j * m1)))
    m2_coh = abs(m2_z)
    return {
        "coherence": float(coh),
        "phases": m1.tolist(),
        "target_phase": target_phase,
        "omega_3": float(omega[3]) if omega is not None else None,
        "locked": bool(coh > 0.95),
        "m2_coherence": float(m2_coh),
        "m2_mean_phase": float(m2_mean_angle),
    }


def agent_attractor_state(phi: np.ndarray) -> dict[str, float | list[float] | bool]:
    """Read-only snapshot of AGENT attractor state."""
    m1 = phi[AGENT_OSCS]  # wektorowo
    coh = abs(np.mean(np.exp(1j * m1)))
    # Wewnętrzne delty między AGENT_OSCS — wektorowo
    d = np.abs((m1 - np.roll(m1, -1) + np.pi) % (2 * np.pi) - np.pi)
    # M2 coherence — also read-only
    m2_phi = phi[M2_OSCS]
    m2_coh = abs(np.mean(np.exp(1j * m2_phi)))
    return {
        "coherence": float(coh),
        "phases": m1.tolist(),
        "internal_delta": [round(float(v), 4) for v in d],
        "max_delta": round(float(max(d)), 4),
        "locked": bool(max(d) < 0.3),
        "m2_coherence": float(m2_coh),
    }
