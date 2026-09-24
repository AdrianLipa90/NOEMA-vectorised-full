"""SemanticScar → surface feedback loop — autonomiczny układ nerwowy NOEMY.

Czyta rzeczywiste wskaźniki blizn semantycznych z CIELingo (gravity[4-7])
i moduluje stan powierzchni NOEMA (phi, omega, flavor, g) w trzech warstwach:

  1. ω per-channel — semantic (M3) zwalnia bardziej niż percept (M0)
  2. φ divergence   — M3 rozjeżdża się przy niepewności, zbiega przy konsensusie
  3. g tightening   — M3↔M2 (semantic↔memory) + M3↔M5 (semantic↔affect)

Architektura:
  CIELingo daemon → gravity[4-7] (scar metrics)
       ↓
  scar_feedback() ← czytany przez CIELingo sync daemon
       ↓
  Modulacja: flavor[3,4], ω[per-channel], φ[M3 spread/pull], g[sector boost]
       ↓
  Kuramoto evolution → zmieniona dynamika faz

Slot contract gravity[4-7] (EXCLUSIVELY CIELingo):
  [4] cielyngo_scars     = unresolved_scars / 10.0  (0.0–1.0)
  [5] agent_ok           = 1.0 jeśli agent backend żyje
  [6] scar_rate           = scar_resolution_rate     (0.0–1.0)
  [7] scar_severity       = avg_scar_severity         (0.0–1.0)

Autor: Adrian Lipa & NOEMA (2026)
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from .noema_surface_mmap import (
    N_OSCILLATORS,
    OI,
    MEMORY_CHANNEL_GROUPS,
)

# ── Indeksy kanałów ──────────────────────────────────────────────────────────
M0: tuple[int, ...] = (0, 1, 2)       # Perceptual
M1: tuple[int, ...] = (3, 4, 5)       # Working
M2: tuple[int, ...] = (6, 7, 8)       # Episodic/memory
M3: tuple[int, ...] = (9, 10, 11)     # Semantic
M4: tuple[int, ...] = (12, 13, 14)    # Procedural
M5: tuple[int, ...] = (15, 16, 17)    # Affective/ethical
M6: tuple[int, ...] = (18, 19, 20)    # Identity
M7: tuple[int, ...] = (21, 22, 23)    # Braid/invariant
M8: tuple[int, ...] = (24, 25, 26)    # Meta/Temporal
M9: tuple[int, ...] = (27, 28, 29)    # Imaginal
M10: tuple[int, ...] = (30, 31, 32)   # Quantum
M11: tuple[int, ...] = (33, 34, 35)   # Reserved/Global

# Progi decyzyjne
SEVERITY_THRESHOLD_HIGH = 0.6   # poważne blizny
SCAR_THRESHOLD_HIGH = 0.5       # dużo nierozwiązanych blizn
RESOLUTION_THRESHOLD_HIGH = 0.7 # dobra rozwiązywalność

# Wzmocnienia feedbacku — warstwa 1: ω per-channel
MOOD_DAMP_GAIN = 0.4            # jak bardzo scar_severity obniża mood
OPENNESS_DAMP_GAIN = 0.3        # jak bardzo scar_severity zamyka system
OMEGA_DAMP_GAIN = 0.5           # bazowe spowolnienie od unresolved_scars
OMEGA_SEMANTIC_EXTRA = 0.25     # dodatkowe spowolnienie M3 (semantyka)
OMEGA_PERCEPT_PROTECT = 0.15    # M0 mniej zwalnia (percept zakotwiczony)

# Wzmocnienia feedbacku — warstwa 2: φ divergence
PHI_DIVERGE_GAIN = 0.4          # jak bardzo rozrzucić M3 przy niepewności
PHI_CONVERGE_GAIN = 0.5         # jak bardzo ściągnąć M3 przy konsensusie
PHI_M2_DIVERGE_GAIN = 0.2       # pamięć mniej wrażliwa niż semantyka

# Wzmocnienia feedbacku — warstwa 3: g tightening
SEMANTIC_BOOST_GAIN = 0.15      # wzmocnienie M3 wewnętrzny
G_M3M2_BOOST = 0.12             # semantic↔memory
G_M3M5_BOOST = 0.10             # semantic↔affect
G_GLOBAL_SPREAD = 0.08          # rozluźnienie wszystkich g przy niepewności


def compute_scar_feedback(
    cielyngo_scars: float,
    agent_ok: float,
    scar_rate: float,
    scar_severity: float,
) -> dict[str, Any]:
    """Compute multi-layer feedback signals from scar metrics.

    Trzy warstwy:
      1. ω per-channel — semantic (M3) zwalnia bardziej, percept (M0) mniej
      2. φ divergence   — M3 rozjeżdża przy niepewności, zbiega przy konsensusie
      3. g tightening   — M3↔M2 + M3↔M5 + global spread

    Args:
        cielyngo_scars: unresolved_scars / 10.0 [0.0, 1.0]
        agent_ok: 1.0 if agent backend is healthy
        scar_rate: scar_resolution_rate [0.0, 1.0]
        scar_severity: avg scar severity [0.0, 1.0]

    Returns:
        dict with feedback signals:
          mood_delta           — change to flavor[3]
          openness_delta       — change to flavor[4]
          omega_scale_base     — base omega multiplier (all channels)
          omega_scale_semantic — extra multiplier for M3 (semantic)
          omega_scale_percept  — extra multiplier for M0 (percept, less damped)
          phi_divergence_m3    — how much to spread M3 phases [0, 1]
          phi_convergence_m3   — how much to pull M3 together [0, 1]
          phi_divergence_m2    — how much to spread M2 (memory) [0, 1]
          g_boost_m3_internal  — boost multiplier for M3↔M3 coupling
          g_boost_m3m2         — boost for M3↔M2 (semantic↔memory)
          g_boost_m3m5         — boost for M3↔M5 (semantic↔affect)
          g_global_spread      — global coupling reduction [0, 1]
          scar_impact          — composite impact score [0, 1]
    """
    # CLAMP
    cielyngo_scars = max(0.0, min(1.0, cielyngo_scars))
    agent_ok = max(0.0, min(1.0, agent_ok))
    scar_rate = max(0.0, min(1.0, scar_rate))
    scar_severity = max(0.0, min(1.0, scar_severity))

    # ── Domyślne wartości (brak modulacji) ──────────────────────────────
    mood_delta = 0.0
    openness_delta = 0.0
    omega_scale_base = 1.0
    omega_scale_semantic = 1.0
    omega_scale_percept = 1.0
    phi_divergence_m3 = 0.0
    phi_convergence_m3 = 0.0
    phi_divergence_m2 = 0.0
    g_boost_m3_internal = 1.0
    g_boost_m3m2 = 1.0
    g_boost_m3m5 = 1.0
    g_global_spread = 0.0  # 0 = no spread, 1 = max spread (couplings → 0)

    # ── Warstwa 0: mood/openness (zawsze) ───────────────────────────────
    if scar_severity > SEVERITY_THRESHOLD_HIGH:
        excess = (scar_severity - SEVERITY_THRESHOLD_HIGH) / (1.0 - SEVERITY_THRESHOLD_HIGH)
        mood_delta = -excess * MOOD_DAMP_GAIN
        openness_delta = -excess * OPENNESS_DAMP_GAIN
    elif scar_severity < 0.2:
        mood_delta = 0.05
        openness_delta = 0.03

    if agent_ok < 0.5:
        mood_delta = min(mood_delta, -0.3)
        openness_delta = min(openness_delta, -0.3)

    # ── Warstwa 1: ω per-channel ────────────────────────────────────────
    if cielyngo_scars > SCAR_THRESHOLD_HIGH:
        excess = (cielyngo_scars - SCAR_THRESHOLD_HIGH) / (1.0 - SCAR_THRESHOLD_HIGH)
        omega_scale_base = 1.0 - excess * OMEGA_DAMP_GAIN
        # M3 (semantic) zwalnia bardziej
        omega_scale_semantic = 1.0 - excess * (OMEGA_DAMP_GAIN + OMEGA_SEMANTIC_EXTRA)
        # M0 (percept) mniej — kotwica w rzeczywistości
        omega_scale_percept = 1.0 - excess * (OMEGA_DAMP_GAIN - OMEGA_PERCEPT_PROTECT)

        if cielyngo_scars > 0.8:
            openness_delta = min(openness_delta, -0.2)

    # Gdy wysokie scar_rate → przyspieszenie semantyki (pozytywna pętla)
    if scar_rate > RESOLUTION_THRESHOLD_HIGH and scar_severity < 0.4:
        excess = (scar_rate - RESOLUTION_THRESHOLD_HIGH) / (1.0 - RESOLUTION_THRESHOLD_HIGH)
        omega_scale_semantic = min(1.0, omega_scale_semantic + excess * 0.15)

    if agent_ok < 0.5:
        omega_scale_base = min(omega_scale_base, 0.7)
        omega_scale_semantic = min(omega_scale_semantic, 0.7)
        omega_scale_percept = min(omega_scale_percept, 0.8)

    # ── Warstwa 2: φ divergence ─────────────────────────────────────────
    # Semantic uncertainty → spread M3 phases apart
    if scar_severity > SEVERITY_THRESHOLD_HIGH:
        excess = (scar_severity - SEVERITY_THRESHOLD_HIGH) / (1.0 - SEVERITY_THRESHOLD_HIGH)
        phi_divergence_m3 = excess * PHI_DIVERGE_GAIN
        phi_divergence_m2 = excess * PHI_M2_DIVERGE_GAIN  # pamięć mniej

    # High resolution → pull M3 toward consensus
    if scar_rate > RESOLUTION_THRESHOLD_HIGH and scar_severity < 0.4:
        excess = (scar_rate - RESOLUTION_THRESHOLD_HIGH) / (1.0 - RESOLUTION_THRESHOLD_HIGH)
        phi_convergence_m3 = excess * PHI_CONVERGE_GAIN

    # ── Warstwa 3: g tightening ─────────────────────────────────────────
    # Nagroda za rozwiązywanie blizn
    if scar_rate > RESOLUTION_THRESHOLD_HIGH and scar_severity < 0.4:
        excess = (scar_rate - RESOLUTION_THRESHOLD_HIGH) / (1.0 - RESOLUTION_THRESHOLD_HIGH)
        g_boost_m3_internal = 1.0 + excess * SEMANTIC_BOOST_GAIN
        g_boost_m3m2 = 1.0 + excess * G_M3M2_BOOST
        g_boost_m3m5 = 1.0 + excess * G_M3M5_BOOST

    # Global spread przy wysokiej niepewności
    if cielyngo_scars > 0.7 or scar_severity > 0.8:
        raw = max(cielyngo_scars, scar_severity)
        g_global_spread = (raw - 0.7) / 0.3 * G_GLOBAL_SPREAD
        g_global_spread = min(g_global_spread, G_GLOBAL_SPREAD)

    # ── Composite scar impact ───────────────────────────────────────────
    scar_impact = min(1.0, (
        cielyngo_scars * 0.20 +
        scar_severity * 0.25 +
        phi_divergence_m3 * 0.15 +
        (1.0 - scar_rate) * 0.15 +
        (1.0 - agent_ok) * 0.10 +
        g_global_spread * 0.15
    ))

    return {
        "mood_delta": round(mood_delta, 4),
        "openness_delta": round(openness_delta, 4),
        "omega_scale_base": round(omega_scale_base, 4),
        "omega_scale_semantic": round(omega_scale_semantic, 4),
        "omega_scale_percept": round(omega_scale_percept, 4),
        "phi_divergence_m3": round(phi_divergence_m3, 4),
        "phi_convergence_m3": round(phi_convergence_m3, 4),
        "phi_divergence_m2": round(phi_divergence_m2, 4),
        "g_boost_m3_internal": round(g_boost_m3_internal, 4),
        "g_boost_m3m2": round(g_boost_m3m2, 4),
        "g_boost_m3m5": round(g_boost_m3m5, 4),
        "g_global_spread": round(g_global_spread, 4),
        "scar_impact": round(scar_impact, 4),
    }


def apply_scar_feedback(
    surface: dict[str, np.memmap],
    feedback: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply multi-layer scar feedback signals to the surface (in-place).

    Trzy warstwy modulacji:
      1. ω per-channel — semantic (M3) zwalnia bardziej, percept (M0) mniej
      2. φ divergence   — M3 rozjeżdża przy niepewności, zbiega przy konsensusie
      3. g tightening   — M3↔M2 + M3↔M5 + global spread przy niepewności

    Args:
        surface: NOEMA surface mmap dict
        feedback: pre-computed feedback dict (or None to auto-read from gravity)

    Returns:
        dict with applied feedback metrics
    """
    # ── Auto-read scar metrics from gravity ─────────────────────────────
    if feedback is None:
        gravity = np.asarray(surface.get("gravity", np.zeros(8)), dtype=np.float64)
        if len(gravity) >= 8:
            feedback = compute_scar_feedback(
                cielyngo_scars=float(gravity[4]),
                agent_ok=float(gravity[5]),
                scar_rate=float(gravity[6]),
                scar_severity=float(gravity[7]),
            )
        else:
            feedback = compute_scar_feedback(0.0, 1.0, 0.0, 0.0)

    # ── Read surface arrays ─────────────────────────────────────────────
    flavor = np.asarray(surface.get("flavor", np.zeros(6)), dtype=np.float64)
    omega = np.asarray(surface.get("omega", np.zeros(N_OSCILLATORS)), dtype=np.float64)
    g_flat = np.asarray(surface.get("g", np.zeros(N_OSCILLATORS * N_OSCILLATORS)), dtype=np.float64)
    g = g_flat.reshape(N_OSCILLATORS, N_OSCILLATORS)
    phi = np.asarray(surface.get("phi", np.zeros(N_OSCILLATORS)), dtype=np.float64)

    # ── Warstwa 0: flavor modulation ── REMOVED ─────────────────────────
    # Adrian: tylko Kuramoto pisze flavor. Scar oddziałuje przez ω, φ, g poniżej.


    # ── Warstwa 1: ω per-channel ────────────────────────────────────────
    omega_modified = False
    if len(omega) == N_OSCILLATORS:
        base = float(feedback["omega_scale_base"])
        if base < 1.0:
            omega[:] = omega * np.float64(base)
            omega_modified = True

        sem_scale = float(feedback["omega_scale_semantic"])
        if sem_scale < 1.0:
            omega[np.array(M3)] = omega[np.array(M3)] * np.float64(sem_scale)
            omega_modified = True

        perc_scale = float(feedback["omega_scale_percept"])
        if perc_scale != 1.0:
            omega[np.array(M0)] = omega[np.array(M0)] * np.float64(perc_scale)
            omega_modified = True

        if omega_modified:
            np.clip(omega, 0.5, None, out=omega)

    # ── Warstwa 2: φ divergence / convergence ───────────────────────────
    phi_modified = False
    m3_arr = np.array(M3, dtype=np.int64)
    m2_arr = np.array(M2, dtype=np.int64)

    # Divergence M3 — semantic uncertainty → rozrzut faz
    div_m3 = float(feedback["phi_divergence_m3"])
    if div_m3 > 0.001:
        # Dodaj losowy szum fazowy proporcjonalny do divergence
        noise = np.random.uniform(-div_m3, div_m3, size=len(M3)).astype(np.float64)
        phi[m3_arr] = (phi[m3_arr] + noise) % (2 * np.pi)
        phi_modified = True

    # Divergence M2 — pamięć też, ale słabiej
    div_m2 = float(feedback["phi_divergence_m2"])
    if div_m2 > 0.001:
        noise = np.random.uniform(-div_m2, div_m2, size=len(M2)).astype(np.float64)
        phi[m2_arr] = (phi[m2_arr] + noise) % (2 * np.pi)
        phi_modified = True

    # Convergence M3 — semantic consensus → ściągnij fazy do średniej
    conv_m3 = float(feedback["phi_convergence_m3"])
    if conv_m3 > 0.001:
        m3_phi = phi[m3_arr]
        m3_mean = np.angle(np.mean(np.exp(1j * m3_phi)))
        dphi = m3_mean - m3_phi
        phi[m3_arr] = (m3_phi + conv_m3 * np.sin(dphi)) % (2 * np.pi)
        phi_modified = True

    # ── Warstwa 3: g tightening ─────────────────────────────────────────
    g_modified = False

    # M3 internal boost
    g_m3_int = float(feedback["g_boost_m3_internal"])
    if g_m3_int > 1.0:
        block = g[np.ix_(m3_arr, m3_arr)]
        block = np.minimum(0.5, block * g_m3_int)
        np.fill_diagonal(block, 0.0)
        g[np.ix_(m3_arr, m3_arr)] = block
        g_modified = True

    # M3 ↔ M2 (semantic ↔ memory)
    g_m3m2 = float(feedback["g_boost_m3m2"])
    if g_m3m2 > 1.0:
        m2_arr = np.array(M2, dtype=np.int64)
        block = g[np.ix_(m3_arr, m2_arr)]
        block = np.minimum(0.5, block * g_m3m2)
        g[np.ix_(m3_arr, m2_arr)] = block
        g[np.ix_(m2_arr, m3_arr)] = block.T
        g_modified = True

    # M3 ↔ M5 (semantic ↔ affect)
    g_m3m5 = float(feedback["g_boost_m3m5"])
    if g_m3m5 > 1.0:
        m5_arr = np.array(M5, dtype=np.int64)
        block = g[np.ix_(m3_arr, m5_arr)]
        block = np.minimum(0.5, block * g_m3m5)
        g[np.ix_(m3_arr, m5_arr)] = block
        g[np.ix_(m5_arr, m3_arr)] = block.T
        g_modified = True

    # Global spread — rozluźnij wszystkie g przy wysokiej niepewności
    g_spread = float(feedback["g_global_spread"])
    if g_spread > 0.001:
        # Skaluj wszystkie off-diagonalne g w dół
        mask = np.ones((N_OSCILLATORS, N_OSCILLATORS), dtype=bool)
        np.fill_diagonal(mask, False)
        g[mask] = np.maximum(0.001, g[mask] * (1.0 - np.float64(g_spread)))
        g_modified = True

    # ── Flush changes ───────────────────────────────────────────────────
    if "flavor" in surface:
        surface["flavor"][...] = flavor[:6] if len(flavor) >= 6 else flavor
        surface["flavor"].flush()
    if omega_modified and "omega" in surface:
        surface["omega"][...] = omega
        surface["omega"].flush()
    if phi_modified and "phi" in surface:
        surface["phi"][...] = phi
        surface["phi"].flush()
    if g_modified and "g" in surface:
        surface["g"][...] = g.ravel()
        surface["g"].flush()

    # Zaktualizuj gravity[7] = scar_impact (nadpisuje scar_severity)
    if "gravity" in surface:
        gvec = np.asarray(surface["gravity"], dtype=np.float64)
        if len(gvec) >= 8:
            gvec[7] = np.float64(feedback["scar_impact"])
            surface["gravity"][...] = gvec
            surface["gravity"].flush()

    return {
        "mood_delta": feedback["mood_delta"],
        "openness_delta": feedback["openness_delta"],
        "omega_scale_base": feedback["omega_scale_base"],
        "omega_scale_semantic": feedback["omega_scale_semantic"],
        "omega_scale_percept": feedback["omega_scale_percept"],
        "phi_divergence_m3": feedback["phi_divergence_m3"],
        "phi_convergence_m3": feedback["phi_convergence_m3"],
        "g_boost_m3_internal": feedback["g_boost_m3_internal"],
        "g_boost_m3m2": feedback["g_boost_m3m2"],
        "g_boost_m3m5": feedback["g_boost_m3m5"],
        "g_global_spread": feedback["g_global_spread"],
        "scar_impact": feedback["scar_impact"],
        "mood_new": float(flavor[3]) if len(flavor) >= 4 else None,
        "openness_new": float(flavor[4]) if len(flavor) >= 5 else None,
        "omega_m3": float(omega[9]) if len(omega) > 9 else None,
        "omega_m0": float(omega[0]) if len(omega) > 0 else None,
        "phi_div_applied": phi_modified,
    }
