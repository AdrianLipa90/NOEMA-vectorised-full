"""NOEMA Kuramoto surface daemon — continuous phase evolution on /dev/shm/ciel_noema.

Hosts the Kuramoto phase synchronization on the shared memory surface,
evolving 36 oscillators at ~10Hz with flavor-modulated frequencies.

Usage:
    python scripts/ciel_noema_kuramoto_daemon.py [--interval SEC] [--dt STEP]
"""

from __future__ import annotations
# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import argparse
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np

# ── Soft clamping: NaN → Heisenberg uncertainty, boundaries → tanh ─────────
def soft_clip(x, lo=0.0, hi=1.0, tau=0.15):
    """Sigmoid-like soft clamp. NaN propagates as uncertainty (Heisenberg).
    
    Args:
        x: input array
        lo: lower bound
        hi: upper bound  
        tau: softness (0=hard, 0.15=default, >0.3 = very soft)
    Returns:
        Soft-clamped values, NaN preserved as np.nan
    """
    if tau <= 0:
        return np.clip(x, lo, hi)
    mid = (lo + hi) / 2.0
    half_range = (hi - lo) / 2.0
    # tanh creates smooth S-curve, NaN flows through as NaN
    return mid + half_range * np.tanh((x - mid) / (tau * half_range + 1e-12))

def zeta_div(x, y, zeta=1e-9):
    """Division with ζ-regularization. Avoids division-by-zero singularities.
    
    Instead of x / max(y, eps) which creates a hard floor,
    uses x / (y + ζ·exp(-y/ζ)) — smooth regularization that 
    preserves sign and asymptotics.
    
    Args:
        x: numerator
        y: denominator  
        zeta: regularization scale (default 1e-9)
    Returns:
        x / (y + ζ·exp(-y/ζ))
    """
    return x / (y + zeta * np.exp(-np.abs(y) / zeta))

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.agent_attractor import apply_agent_attractor, agent_attractor_state
from ciel_geometry.neutrino_phase_channel import tau_phi_coupling
from ciel_geometry.noema_registry import registry
from ciel_geometry.scar_feedback import apply_scar_feedback
from ciel_geometry.noema_surface_mmap import (
    open_surface,
    ensure_surface,
    evolve_surface,
    read_surface_state,
    flush_surface,
)

logging.basicConfig(
    level=logging.INFO,
    format="[kuramoto] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Kuramoto surface daemon")
    parser.add_argument("--interval", type=float, default=0.1, help="Seconds between evolutions (default: 0.1 = 10Hz)")
    parser.add_argument("--dt", type=float, default=0.05, help="Kuramoto integration dt (default: 0.05)")
    args = parser.parse_args()

    log.info("Starting Kuramoto surface daemon (interval=%.3fs, dt=%.4f)", args.interval, args.dt)
    surface = ensure_surface()
    log.info("Surface OK: tick=%s, phi_mean=%.4f", surface["tick"][0], surface["phi"].mean())

    reg_token = registry.register("kuramoto")

    import signal
    _running = True
    def _stop(signum, frame):
        nonlocal _running
        _running = False
    def _bus(signum, frame):
        nonlocal surface
        log.warning("SIGBUS — mmap collision, re-opening surface")
        surface = ensure_surface()
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGBUS, _bus)

    step = 0
    last_report = time.monotonic()
    hb_step = 0
    base_dt = args.dt
    _prev_omega_held: np.ndarray | None = None  # ω[3:9] saved from attractor for sensor protection
    try:
        while _running:
            try:
                # ── Sensor blend: gentle drift from linux_sensor, protect AGENT/M2 ──
                if "sensor_raw" in surface:
                    sensor_phi = np.asarray(surface["sensor_raw"], dtype=np.float64)
                    if np.any(np.isfinite(sensor_phi)):
                        phi_view = np.asarray(surface["phi"], dtype=np.float64)
                        # Protected: AGENT(3-5) + M2(6-8) — ignore sensor completely
                        _n = len(phi_view)
                        unrest = np.ones(_n, dtype=bool)
                        unrest[3:9] = False
                        phi_view[unrest] = 0.85 * phi_view[unrest] + 0.15 * sensor_phi[unrest]
                    # Protect ω[3-8]: restore from last attractor correction
                    if "omega" in surface and _prev_omega_held is not None:
                        omega_view = np.asarray(surface["omega"], dtype=np.float64)
                        omega_view[3:9] = _prev_omega_held
                # ── /Sensor ────────────────────────────────────────────────

                # ── τ↔φ HOLONOMIC LOOP: sensor_raw → tau → coupling ──
                # sensor_raw (36 loads, φ values 0-2π) maps to tau per-oscillator.
                # High load → low tau (slow integration, conserve energy)
                # Low load → high tau (fast integration, explore)
                # PROTECTED: AGENT(3-5) + M2(6-8) — identity/semantic oscillators
                # hold fixed tau=0.353, unaffected by system load fluctuations
                _TWO_PI = 2.0 * np.pi
                _protected = np.zeros(36, dtype=bool)
                _protected[3:9] = True
                if "tau" in surface and "sensor_raw" in surface:
                    tau_arr = np.asarray(surface["tau"], dtype=np.float64)
                    sr_arr = np.asarray(surface["sensor_raw"], dtype=np.float64)
                    if np.any(np.isfinite(sr_arr)):
                        # Normalize φ/2π → [0,1] via soft_clip (tanh, Heisenberg-soft)
                        sr_norm = soft_clip(sr_arr / _TWO_PI, 0.0, 1.0, tau=0.15)
                        # Invert: high load → tau near 0.2, low load → tau near 0.8
                        tau_from_sensor = 0.2 + 0.6 * (1.0 - sr_norm)
                        safe = np.isfinite(tau_from_sensor)
                        unrest = ~_protected & safe
                        # Slow EMA (85/15) keeps tau continuous, prevents binary collapse
                        tau_arr[unrest] = 0.85 * tau_arr[unrest] + 0.15 * tau_from_sensor[unrest]
                        tau_arr[_protected] = 0.353
                        # NO relaxation term — it caused binary collapse
                        # NO soft_clip boundary — mapping naturally keeps [0.2, 0.8]

                # ── τ→ε→D cascade: tau spread drives Λ (flavor[4])
                # ε = σ_τ / τ₀ — rozrzut tau jako perturbacja (zeta-div)
                # R-gated: ε modulates D only when system is synchronized.
                #   When R < 0.4 → R_gate ≈ 0 → D returns to baseline
                #   When R > 0.7 → R_gate ≈ 1 → ε fully modulates D
                # This prevents positive feedback desync spiral.
                if "tau" in surface and "flavor" in surface and "phi" in surface:
                    tau_arr = np.asarray(surface["tau"], dtype=np.float64)
                    phi_arr = np.asarray(surface["phi"], dtype=np.float64)
                    flavor_arr = np.asarray(surface["flavor"], dtype=np.float64)
                    z_global = np.mean(np.exp(1j * phi_arr))
                    R = abs(z_global)
                    std_tau = float(np.std(tau_arr))
                    epsilon = float(zeta_div(std_tau, 0.353, zeta=0.01))
                    epsilon = min(0.5, epsilon)
                    R_gate = soft_clip((R - 0.4) / 0.3, 0.0, 1.0, tau=0.1)
                    D_target = 0.3 + epsilon * R_gate * 0.2       # [0.3, 0.4] when synced
                    flavor_arr[4] = soft_clip(
                        0.95 * flavor_arr[4] + 0.05 * D_target,
                        0.05, 0.6, tau=0.15
                    )
                # ── /τ↔φ ─────────────────────────────────────────────────

                # ── TARDIS: semantic gravity modulates integration step ──
                dt_eff = base_dt
                if "gravity" in surface:
                    gvec = np.asarray(surface["gravity"], dtype=np.float64)
                    tau_dilation = float(gvec[1])
                    if tau_dilation > 1.01 and tau_dilation < 10.0:
                        dt_eff = base_dt / tau_dilation  # slower evolution when meaning is dense
                # ── /TARDIS ──────────────────────────────────────────────
                thinking_delta = evolve_surface(surface, dt=dt_eff, flush=True, continuous=True)
                # ── AGENT attractor (phase lock + ω damping + M1 internal coupling) ──
                # Peripheral coupling (M0,M2,M6) handled by omega-adaptive below.
                # Set coupling_m0/m2/m6/m0m2=0 to avoid overwriting omega-adaptive.
                _attractor_state = apply_agent_attractor(
                    surface["phi"], surface["g"],
                    omega=surface.get("omega"),
                    coupling_m0=0.0, coupling_m2=0.0,
                    coupling_m6=0.0, coupling_m0m2=0.0,
                )
                # ── /AGENT ────────────────────────────────────────────────
                # ── MEMORY (M2) boost — wektorowo przez slicing ──
                g_view = np.asarray(surface["g"], dtype=np.float64)
                g_view[6:9, 0:3] = 0.12   # M2→M0
                g_view[6:9, 3:6] = 0.15   # M2→M1
                g_view[6:9, 6:9] = 0.08   # M2↔M2 (off-diag)
                np.fill_diagonal(g_view[6:9, 6:9], 0.0)  # diagonal bez zmian
                # ── /MEMORY ────────────────────────────────────────────────
                # ── OMEGA-ADAPTIVE COUPLING: pull high-ω osc toward AGENT ──
                # Każdy oscillator dostaje coupling do AGENT(M1,3:6)
                # proporcjonalny do ω deviation — im dalej, tym silniej
                omega_v = np.asarray(surface["omega"], dtype=np.float64).ravel()
                agent_mean_omega = float(omega_v[3:6].mean())  # ~0.5
                omega_dev = np.abs(omega_v - agent_mean_omega)
                cpl_strength = np.clip(omega_dev * 0.01, 0.05, 0.50)
                for i in range(36):
                    if 3 <= i < 6:
                        continue
                    g_view[i, 3:6] = cpl_strength[i]
                    g_view[3:6, i] = cpl_strength[i]
                # ── /OMEGA-ADAPTIVE ─────────────────────────────────────────

                # ── CPU TOPOLOGY COUPLING: linux hardware geometry → g matrix ──
                # 6 physical cores × 2 SMT threads → 12 oscillator block (0-11)
                # SMT pairs (sharing core): strong coupling 0.35
                # Same-group (physical/SMT): medium coupling 0.15
                # Cross SMT-core: weak coupling 0.08
                _smt_pairs = [(0,6), (1,7), (2,8), (3,9), (4,10), (5,11)]
                _phys = [0,1,2,3,4,5]
                _smt = [6,7,8,9,10,11]
                # SMT sibling pairs — strongest
                for a, b in _smt_pairs:
                    g_view[a, b] = max(g_view[a, b], 0.35)
                    g_view[b, a] = max(g_view[b, a], 0.35)
                # Within physical core group
                for i in _phys:
                    for j in _phys:
                        if i != j:
                            g_view[i, j] = max(g_view[i, j], 0.15)
                # Within SMT thread group
                for i in _smt:
                    for j in _smt:
                        if i != j:
                            g_view[i, j] = max(g_view[i, j], 0.15)
                # Cross: physical ↔ different SMT
                for a, _ in _smt_pairs:
                    for _, b in _smt_pairs:
                        if a != b:
                            g_view[a, b] = max(g_view[a, b], 0.08)
                            g_view[b, a] = max(g_view[b, a], 0.08)
                # ── /CPU TOPOLOGY ─────────────────────────────────────────────

                # ── SCAR FEEDBACK: semantic scar metrics → surface modulation
                scar_result = apply_scar_feedback(surface)
                # ── Kuramoto-owned flavor blend: read CIEL state + scar suggestions ──
                # CIEL writes to ciel_state.json; scar_feedback to scar_suggestions.json.
                # Kuramoto daemon is the SOLE writer of flavor[2..5], reading both.
                _flavor_arr = np.asarray(surface.get("flavor", None), dtype=np.float64)
                _hub_path = Path("/dev/shm/ciel_noema/ciel_state.json")
                if _hub_path.exists() and _flavor_arr is not None and len(_flavor_arr) >= 6:
                    try:
                        _hub = json.loads(_hub_path.read_text())
                        _fmood = float(_hub.get("mood_normalized", 0.5))
                        _fmode = float(_hub.get("mode_code", 0.5))
                        _flavor_arr[3] = np.float64(max(0.05, min(1.0, _fmood)))
                        _flavor_arr[5] = np.float64(max(0.0, min(1.0, _fmode)))
                    except Exception:
                        pass
                    # flavor[2] = R_M5: koherencja kanału etycznego φ[15,16,17]
                    # Zapobiega spłynięciu do 0 przez scar_feedback race condition.
                    _phi_local = np.asarray(surface.get("phi", np.zeros(36)), dtype=np.float64)
                    if len(_phi_local) >= 18:
                        _s = (np.sin(_phi_local[15]) + np.sin(_phi_local[16]) + np.sin(_phi_local[17])) / 3.0
                        _c = (np.cos(_phi_local[15]) + np.cos(_phi_local[16]) + np.cos(_phi_local[17])) / 3.0
                        _r_m5 = float(np.sqrt(_s*_s + _c*_c))
                        _flavor_arr[2] = np.float64(_r_m5)
                        # mode_code z R_M5 — zrywa pętlę stale hub (mode=safe gdy R_M5≥0.4)
                        if _r_m5 >= 0.4:
                            _flavor_arr[5] = np.float64(0.5)  # standard


                # Save ω[3:9] for sensor protection next cycle
                if "omega" in surface:
                    _prev_omega_held = np.asarray(surface["omega"], dtype=np.float64)[3:9].copy()
                step += 1
                hb_step += 1
                now = time.monotonic()
                if hb_step % 50 == 0:
                    registry.heartbeat(reg_token)
                if now - last_report >= 5.0:
                    state = read_surface_state(surface)
                    lr = getattr(evolve_surface, 'last_thinking_lr', 0.0)
                    tau_d = float(np.asarray(surface["gravity"], dtype=np.float64)[1]) if "gravity" in surface else 1.0
                    tau_mean = float(np.asarray(surface["tau"], dtype=np.float64).mean()) if "tau" in surface else 0.0
                    tau_std = float(np.asarray(surface["tau"], dtype=np.float64).std()) if "tau" in surface else 0.0
                    epsilon = float(zeta_div(tau_std, 0.353, zeta=0.01))
                    _agent = agent_attractor_state(surface["phi"])
                    m2_coh_val = _attractor_state.get("m2_coherence", 0.0)
                    log.info(
                        "tick=%s  steps=%d  φ=%.4f  τ̄=%.4f  ε=%.4f  coh=%.3f  γ=%.3f  think=%.4f  AGENT=%.4f%s  M2=%.3f",
                        surface["tick"][0], step,
                        surface["phi"].mean(),
                        tau_mean,
                        epsilon,
                        state.get("coherence_index", 0),
                        tau_d,
                        thinking_delta,
                        _agent["coherence"],
                        "🔒" if _agent["locked"] else "",
                        m2_coh_val,
                    )
                    if thinking_delta > 0.5:
                        log.info("  >> THINKING TRIGGER: ΔΦ=%.4f — harmonic insight cascade", thinking_delta)
                    last_report = now
            except Exception as e:
                log.error("Evolve error: %s", e)
                time.sleep(1)
            time.sleep(args.interval)
    finally:
        registry.unregister(reg_token)
        log.info("Unregistered from NOEMA registry")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
