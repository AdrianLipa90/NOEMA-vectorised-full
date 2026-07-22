"""NOEMA Kuramoto surface daemon — real surface on /dev/shm and imaginal
generator on the dedicated New Volume catalog.

Hosts the Kuramoto phase synchronization on the shared memory surface,
evolving 36 oscillators at ~10Hz with flavor-modulated frequencies.

Usage:
    python scripts/ciel_noema_kuramoto_daemon.py [--interval SEC] [--dt STEP]

Consolidated: uses CielDaemon base (daemon_base.py).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.daemon_base import CielDaemon
from ciel_geometry.agent_attractor import apply_agent_attractor, agent_attractor_state
from ciel_geometry.neutrino_phase_channel import tau_phi_coupling
from ciel_geometry.scar_feedback import apply_scar_feedback
from ciel_geometry.noema_surface_mmap import (
    OI,
    open_surface,
    ensure_surface,
    evolve_surface,
    read_surface_state,
    flush_surface,
    initialize_coupling_from_memory_channels,
)
from ciel_geometry.resonance_bridge import DEFAULT_IMAGINAL_SURFACE_ROOT


# Static topology/index views.  These are derived from the 36-oscillator
# contract once at import time; rebuilding the same masks and Python tuples at
# 10 Hz only added interpreter overhead and did not alter the phase equations.
_TWO_PI = 2.0 * np.pi
_TAU_PROTECTED = np.zeros(36, dtype=bool)
_TAU_PROTECTED[3:9] = True
_TAU_PROTECTED[15:21] = True
_TAU_PROTECTED[24:30] = True
_TAU_PROTECTED[33:36] = True
_SENSOR_PROTECTED = _TAU_PROTECTED.copy()
_SENSOR_PROTECTED[33:36] = True
_SMT_A = np.array([0, 1, 2, 3, 4, 5], dtype=np.intp)
_SMT_B = _SMT_A + 6
_CPU_I, _CPU_J = np.where(~np.eye(12, dtype=bool))
_CPU_BASE = np.where((_CPU_I < 6) == (_CPU_J < 6), 0.15, 0.08)


def soft_clip(x, lo=0.0, hi=1.0, tau=0.15):
    if tau <= 0:
        return np.clip(x, lo, hi)
    mid = (lo + hi) / 2.0
    half_range = (hi - lo) / 2.0
    return mid + half_range * np.tanh((x - mid) / (tau * half_range + 1e-12))


def zeta_div(x, y, zeta=1e-9):
    return x / (y + zeta * np.exp(-np.abs(y) / zeta))


class KuramotoDaemon(CielDaemon):
    NAME = "kuramoto"
    INTERVAL = 0.1  # 10 Hz
    HEARTBEAT_INTERVAL = 5.0  # every 50 ticks

    def __init__(self, dt: float = 0.05):
        super().__init__()
        self.dt = dt
        self._prev_omega_held: np.ndarray | None = None
        self._imaginal_surface: dict[str, np.memmap] | None = None
        self._step = 0
        self._last_report = 0.0
        self._R_held: float = 0.57

    def setup(self) -> None:
        self._open_surface()
        # Restore the J_KJ/OI-derived topology at daemon start.  This is a
        # deterministic runtime reinitialisation of coupling only; phases,
        # memory channels, and sensor observations remain untouched.
        initialize_coupling_from_memory_channels(self._surface["g"])
        flush_surface(self._surface)
        # Open the resonance-owned imaginal surface once.  Recreating twelve
        # memmaps on every 100 ms tick was needless transport/I/O churn; the
        # writer keeps the underlying files stable for the daemon lifetime.
        if not DEFAULT_IMAGINAL_SURFACE_ROOT.exists():
            raise RuntimeError(
                f"imaginal surface unavailable: {DEFAULT_IMAGINAL_SURFACE_ROOT}"
            )
        self._imaginal_surface = open_surface(
            root=DEFAULT_IMAGINAL_SURFACE_ROOT, mode="r"
        )
        self._setup_registry()
        self.log.info(
            "Surface OK: tick=%s, phi_mean=%.4f",
            self._read_tick(), self._surface.get("phi", np.array([])).mean()
            if "phi" in self._surface else 0,
        )
        self._last_report = time.monotonic()

    def tick(self) -> None:
        surface = self._surface
        sensor_valid = False

        # ── Sensor blend ──────────────────────────────────────────
        if "sensor_raw" in surface:
            sensor_raw = np.asarray(surface["sensor_raw"], dtype=np.float64)
            sensor_valid = bool(
                np.all(np.isfinite(sensor_raw))
                and np.all(sensor_raw >= 0.0)
                and np.all(sensor_raw <= _TWO_PI)
            )
            if sensor_valid:
                sensor_phi = sensor_raw
                phi_view = np.asarray(surface["phi"], dtype=np.float64)
                unrest = ~_SENSOR_PROTECTED
                phi_view[unrest] = 0.85 * phi_view[unrest] + 0.15 * sensor_phi[unrest]
            if "omega" in surface and self._prev_omega_held is not None:
                omega_view = np.asarray(surface["omega"], dtype=np.float64)
                omega_view[3:9] = self._prev_omega_held

        # ── τ↔φ HOLONOMIC LOOP ───────────────────────────────────
        if "tau" in surface and sensor_valid:
            tau_arr = np.asarray(surface["tau"], dtype=np.float64)
            sr_arr = np.asarray(surface["sensor_raw"], dtype=np.float64)
            if np.any(np.isfinite(sr_arr)):
                sr_norm = soft_clip(sr_arr / _TWO_PI, 0.0, 1.0, tau=0.15)
                tau_from_sensor = 0.2 + 0.6 * (1.0 - sr_norm)
                safe = np.isfinite(tau_from_sensor)
                unrest = ~_TAU_PROTECTED & safe
                tau_arr[unrest] = 0.85 * tau_arr[unrest] + 0.15 * tau_from_sensor[unrest]
                tau_arr[_TAU_PROTECTED] = 0.353

        # ── SINGLE-WRITER RESONANCE INPUT ────────────────────────
        # The resonance daemon owns only the imaginal surface.  Kuramoto is
        # the sole writer of real phi and applies the existing bridge gain
        # scaled to its 10 Hz cadence (the old bridge wrote once per second).
        imaginal = self._imaginal_surface
        if imaginal is None:
            raise RuntimeError("imaginal surface handle was not initialized")
        imaginal_phi = np.asarray(imaginal["phi"], dtype=np.float64)
        resonance_delta = np.angle(
            np.exp(1j * (imaginal_phi - np.asarray(surface["phi"], dtype=np.float64)))
        )
        resonance_step = OI * 12.0 * self.INTERVAL
        surface["phi"][...] = np.mod(
            np.asarray(surface["phi"], dtype=np.float64)
            + resonance_step * resonance_delta,
            2.0 * np.pi,
        )

        # ── τ→ε→D cascade ────────────────────────────────────────
        if "tau" in surface and "flavor" in surface and "phi" in surface:
            tau_arr = np.asarray(surface["tau"], dtype=np.float64)
            phi_arr = np.asarray(surface["phi"], dtype=np.float64)
            flavor_arr = np.asarray(surface["flavor"], dtype=np.float64)
            z_global = np.mean(np.exp(1j * phi_arr))
            R = abs(z_global)
            self._R_held = float(R)
            std_tau = float(np.std(tau_arr))
            epsilon = float(zeta_div(std_tau, 0.353, zeta=0.01))
            epsilon = min(0.5, epsilon)
            R_gate = soft_clip((R - 0.4) / 0.3, 0.0, 1.0, tau=0.1)
            D_target = 0.3 + epsilon * R_gate * 0.2
            _d_blend = 0.75 * flavor_arr[4] + 0.25 * D_target
            flavor_arr[4] = max(0.15, min(0.6, _d_blend))

        # ── TARDIS: semantic gravity modulates dt ─────────────────
        dt_eff = self.dt
        if "gravity" in surface:
            gvec = np.asarray(surface["gravity"], dtype=np.float64)
            tau_dilation = float(gvec[1])
            if 1.01 < tau_dilation < 10.0:
                dt_eff = self.dt / tau_dilation

        thinking_delta = evolve_surface(surface, dt=dt_eff, flush=True, continuous=True)

        # ── AGENT attractor ──────────────────────────────────────
        _attractor_state = apply_agent_attractor(
            surface["phi"], surface["g"],
            omega=surface.get("omega"),
            coupling_m0=0.0, coupling_m2=0.0,
            coupling_m6=0.0, coupling_m0m2=0.0,
        )

        # ── Coupling matrix adjustments ──────────────────────────
        g_view = np.asarray(surface["g"], dtype=np.float64)
        # M2 boost
        g_view[6:9, 0:3] = 0.12
        g_view[6:9, 3:6] = 0.15
        g_view[6:9, 6:9] = 0.08
        np.fill_diagonal(g_view[6:9, 6:9], 0.0)
        # M5+M6, M8+M9 semantic channels
        g_view[15:21, 15:21] = 0.35
        np.fill_diagonal(g_view[15:21, 15:21], 0.0)
        g_view[24:30, 24:30] = 0.35
        np.fill_diagonal(g_view[24:30, 24:30], 0.0)
        # M11 quantum floor
        g_view[33:36, 33:36] = 0.08
        np.fill_diagonal(g_view[33:36, 33:36], 0.0)

        # ── OMEGA-ADAPTIVE coupling ──────────────────────────────
        omega_v = np.asarray(surface["omega"], dtype=np.float64).ravel()
        agent_mean_omega = float(omega_v[3:6].mean())
        omega_dev = np.abs(omega_v - agent_mean_omega)
        cpl_strength = np.clip(omega_dev * 0.01, 0.05, 0.50)
        for i in range(36):
            if 3 <= i < 6:
                continue
            g_view[i, 3:6] = cpl_strength[i]
            g_view[3:6, i] = cpl_strength[i]

        # ── CPU TOPOLOGY coupling ─────────────────────────────────
        g_view[_SMT_A, _SMT_B] = np.maximum(g_view[_SMT_A, _SMT_B], 0.35)
        g_view[_SMT_B, _SMT_A] = np.maximum(g_view[_SMT_B, _SMT_A], 0.35)
        g_view[_CPU_I, _CPU_J] = np.maximum(g_view[_CPU_I, _CPU_J], _CPU_BASE)

        # ── SCAR FEEDBACK ────────────────────────────────────────
        scar_result = apply_scar_feedback(surface)

        # ── Flavor blend from CIEL state ─────────────────────────
        _flavor_arr = np.asarray(surface.get("flavor", None), dtype=np.float64)
        _hub_path = Path("/dev/shm/ciel_noema/ciel_state.json")
        if _hub_path.exists() and _flavor_arr is not None and len(_flavor_arr) >= 6:
            try:
                _hub = json.loads(_hub_path.read_text())
                _fmood = float(_hub.get("mood_normalized", 0.5))
                _flavor_arr[3] = np.float64(max(0.05, min(1.0, _fmood)))
                _D_f = 2.0 + self._R_held
                _flavor_arr[5] = np.float64(max(2.0, min(3.0, _D_f)))
            except Exception as exc:
                self.log.debug("flavor read skipped: %s", exc)

        # Save ω[3:9]
        if "omega" in surface:
            self._prev_omega_held = np.asarray(surface["omega"], dtype=np.float64)[3:9].copy()

        # ── Status report ────────────────────────────────────────
        self._step += 1
        now = time.monotonic()
        if now - self._last_report >= 5.0:
            state = read_surface_state(surface)
            _agent = agent_attractor_state(surface["phi"])
            m2_coh_val = _attractor_state.get("m2_coherence", 0.0)
            self.log.info(
                "tick=%s  steps=%d  φ=%.4f  coh=%.3f  γ=%.3f  think=%.4f  AGENT=%.4f%s  M2=%.3f",
                surface["tick"][0], self._step,
                surface["phi"].mean(),
                state.get("coherence_index", 0),
                float(np.asarray(surface["gravity"], dtype=np.float64)[1])
                if "gravity" in surface else 1.0,
                thinking_delta,
                _agent["coherence"],
                "🔒" if _agent["locked"] else "",
                m2_coh_val,
            )
            if thinking_delta > 0.5:
                self.log.info("  >> THINKING TRIGGER: ΔΦ=%.4f", thinking_delta)
            self._last_report = now


def main() -> int:
    parser = argparse.ArgumentParser(description="NOEMA Kuramoto surface daemon")
    parser.add_argument("--interval", type=float, default=0.1)
    parser.add_argument("--dt", type=float, default=0.05)
    args = parser.parse_args()

    daemon = KuramotoDaemon(dt=args.dt)
    daemon.INTERVAL = args.interval
    daemon.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
