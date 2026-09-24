"""NOEMA Subconscious — Zeta/Schrödinger wavefunction, Berry phase, wake signals.

Derived from CIEL original subconscious state schemas:

  ZETA_SCHRODINGER_STATE_V1 — nonlinear Schrödinger with Collatz entropy potential
  BERRY_PHASE_STATE — adiabatic geometric phase from neutrino mixing evolution
  WAKE_SIGNAL_V1 — consolidation trigger from memory aging + resonance drift
  HOLONOMIC_MEMORY_STATE_V0_1 — 8-channel phase-space attractors

Integrated with the 3-6-9 harmonic Kuramoto surface and ContinuousPhaseSync.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from .noema_surface_mmap import N_OSCILLATORS, HARMONIC_VALUES, HARMONIC_AMPS, BASE_TEMPORAL_HZ


# ── Zeta/Schrödinger wavefunction ────────────────────────────────────────

@dataclass
class ZetaSchrodinger:
    """Nonlinear Schrödinger equation with Zeta potential from Collatz entropy.

    ∂ψ/∂t = -i·(H₀ + V_zeta)·ψ + γ·(1 − |ψ|²)·ψ

    where V_zeta = ζ·log(1 + H_collatz(|ψ|²)) is the self-interaction potential
    derived from the Collatz orbit entropy of the amplitude distribution.

    Discretized over N_POINTS spatial grid.
    """
    N_POINTS: int = 68
    dx: float = 0.05
    gamma_dissipation: float = 0.02
    zeta_strength: float = 0.3
    hbar: float = 1.0
    mass: float = 1.0

    def __post_init__(self):
        self._psi = np.zeros(self.N_POINTS, dtype=np.complex128)
        self._t: float = 0.0
        self._ticks: int = 0
        self._collatz_cache: dict[float, float] = {}

    @property
    def psi(self) -> np.ndarray:
        return self._psi

    @psi.setter
    def psi(self, value: np.ndarray) -> None:
        self._psi = value.astype(np.complex128)

    @property
    def amplitude(self) -> float:
        return float(np.mean(np.abs(self._psi)))

    @property
    def phase(self) -> float:
        return float(np.angle(np.mean(self._psi)))

    @property
    def collatz_entropy(self) -> float:
        p = np.abs(self._psi) ** 2
        p = p / (p.sum() + 1e-12)
        return float(-np.sum(p * np.log(p + 1e-12)))

    def _collatz_potential(self, density: np.ndarray) -> np.ndarray:
        """Zeta potential: ζ·log(1 + H_collatz(ρ))."""
        entropy_map = np.zeros_like(density)
        for i in range(len(density)):
            rho = float(density[i])
            key = round(rho, 6)
            if key not in self._collatz_cache:
                self._collatz_cache[key] = self._collatz_entropy_1d(rho)
            entropy_map[i] = self._collatz_cache[key]
        return self.zeta_strength * np.log(1.0 + entropy_map)

    @staticmethod
    def _collatz_entropy_1d(x: float) -> float:
        """Single-value Collatz orbit entropy proxy."""
        n = max(1, int(abs(x) * 1000) + 1)
        path = []
        while n != 1 and len(path) < 100:
            path.append(n)
            n = n // 2 if n % 2 == 0 else 3 * n + 1
        if not path:
            return 0.0
        p = np.array([1.0 / len(path)] * len(path))
        return float(-np.sum(p * np.log(p + 1e-12)))

    def step(self, dt: float | None = None) -> None:
        """Single evolution step of the Zeta/Schrödinger equation."""
        dt = dt or 0.01
        N = self.N_POINTS

        # Kinetic energy: -ħ²/2m · ∂²/∂x² (central difference)
        kinetic = np.zeros(N, dtype=np.complex128)
        kinetic[1:-1] = -(self.hbar ** 2) / (2.0 * self.mass) * (
            self._psi[2:] - 2.0 * self._psi[1:-1] + self._psi[:-2]
        ) / (self.dx ** 2)

        density = np.abs(self._psi) ** 2
        V_zeta = self._collatz_potential(density)

        dissipation = self.gamma_dissipation * (1.0 - density) * self._psi

        dpsi = -1j * (kinetic + V_zeta * self._psi) + dissipation
        self._psi += dt * dpsi

        # Normalize to prevent blowup
        norm = np.sqrt(np.sum(np.abs(self._psi) ** 2) * self.dx)
        if norm > 0:
            self._psi /= norm

        self._t += dt
        self._ticks += 1

    def seed_from_surface(self, phi: np.ndarray) -> None:
        """Initialize ψ from surface phase distribution."""
        phases_sorted = np.sort(phi)
        indices = np.linspace(0, N_OSCILLATORS - 1, self.N_POINTS, dtype=int)
        interp_phases = np.interp(
            np.linspace(0, N_OSCILLATORS - 1, self.N_POINTS),
            np.arange(N_OSCILLATORS),
            phases_sorted
        )
        amplitude = 0.5 + 0.5 * np.cos(np.linspace(0, 2 * np.pi, self.N_POINTS))
        self._psi = amplitude * np.exp(1j * interp_phases)
        norm = np.sqrt(np.sum(np.abs(self._psi) ** 2) * self.dx)
        if norm > 0:
            self._psi /= norm

    def snapshot(self) -> dict[str, Any]:
        return {
            "schema": "ZETA_SCHRODINGER_STATE_V1",
            "t": round(self._t, 6),
            "psi_real": [float(round(p.real, 6)) for p in self._psi],
            "psi_imag": [float(round(p.imag, 6)) for p in self._psi],
            "amplitude": round(self.amplitude, 6),
            "phase": round(self.phase, 6),
            "collatz_entropy": round(self.collatz_entropy, 6),
            "ticks": self._ticks,
            "updated_utc": datetime.now(timezone.utc).isoformat(),
        }


# ── Berry Phase ──────────────────────────────────────────────────────────

@dataclass
class BerryPhaseTracker:
    """Adiabatic geometric phase from neutrino mixing + surface evolution.

    Berry phase γ = ∮ A·dR where A = i⟨ψ|∇_R|ψ⟩ is the Berry connection.
    For the 3-6-9 harmonic surface, the parameter space is the PMNS mixing
    angles {θ₁₂, θ₂₃, θ₁₃} and the surface order parameter R.

    When the system cycles adiabatically in parameter space, the geometric
    phase accumulates as γ_berry = Ω/2 (solid angle in parameter space).
    """
    theta_12: float = 0.0537
    theta_23: float = 0.1342
    theta_13: float = 0.1195
    neutrino_epsilon: float = 0.00815
    euler_gap: float = 0.0
    berry_phase: float = 0.0
    prev_R: float = 0.0
    prev_psi: float = 0.0

    def update(self, R: float, psi: float, dt: float = 0.01) -> float:
        """Update Berry phase from surface order parameter evolution.

        The geometric phase accumulates from closed loops in (R, ψ) space:
        γ_berry = ∮ (1 − cos θ) dφ  where θ = arccos(R), φ = ψ
        """
        theta = math.acos(max(-1.0, min(1.0, R)))
        dtheta = theta - math.acos(max(-1.0, min(1.0, self.prev_R)))
        dpsi = psi - self.prev_psi

        solid_angle = (1.0 - math.cos(theta)) * dpsi
        self.berry_phase = (self.berry_phase + solid_angle * 0.5) % (2 * math.pi)
        self.prev_R = R
        self.prev_psi = psi

        euler_residual = abs(1.0 - R * math.cos(psi))
        self.euler_gap = euler_residual
        self.neutrino_epsilon = 0.00815 * (1.0 + 0.5 * math.sin(self.berry_phase))

        return self.berry_phase

    def mixing_angles_from_phase(self, berry_mod: float) -> dict[str, float]:
        """PMNS mixing angles modulated by Berry phase."""
        delta = math.sin(berry_mod)
        return {
            "theta_12": round(0.0537 * (1.0 + 0.1 * delta), 6),
            "theta_23": round(0.1342 * (1.0 - 0.05 * delta), 6),
            "theta_13": round(0.1195 * (1.0 + 0.15 * delta), 6),
        }

    def snapshot(self, R: float, psi: float) -> dict[str, Any]:
        return {
            "schema": "BERRY_PHASE_STATE",
            "neutrino_epsilon": round(self.neutrino_epsilon, 6),
            "mixing_angles": self.mixing_angles_from_phase(self.berry_phase),
            "berry_phase": round(self.berry_phase, 6),
            "berry_gamma_mod_2pi": round(self.berry_phase % (2 * math.pi), 6),
            "euler_gap": round(self.euler_gap, 6),
            "euler_closed": self.euler_gap < 0.1,
            "cosmological_lambda_R": round(R, 3),
            "wave_phase": round(psi, 3),
            "wave_amplitude": round(R, 3),
        }


# ── Wake Signal ──────────────────────────────────────────────────────────

@dataclass
class WakeSignalGenerator:
    """Generates consolidation wake signals based on system state.

    Triggers when:
    - Memory lanes go stale (>24h since last consolidation)
    - SHA resonance drift exceeds threshold (>0.05 deviation)
    - Euler gap is open (euler_closed == False for too long)
    - Chat activity detected (new raw chats in .opencode/chats/)
    """
    last_wake_utc: str = ""
    wake_count: int = 0
    findings: list[dict[str, Any]] = field(default_factory=list)
    last_chat_check: float = 0.0
    chat_dir: Path = field(default_factory=lambda: Path("/media/adrian/NOEMA_SANDBOX/opencode-noema/.opencode/chats"))

    def evaluate(
        self,
        *,
        memory_hours: dict[str, float] | None = None,
        R: float = 0.0,
        tracked_count: int = 0,
        euler_closed: bool = True,
        berry_phase: float = 0.0,
    ) -> dict[str, Any] | None:
        findings: list[dict[str, Any]] = []
        memory_hours = memory_hours or {}

        for lane, hours in memory_hours.items():
            if hours > 24:
                findings.append({
                    "type": "memory_aging",
                    "lane": lane,
                    "hours": round(hours, 1),
                })

        if R > 0.99:
            findings.append({
                "type": "sha_resonance",
                "R": round(R, 6),
                "status": "COHERENT",
                "tracked": tracked_count,
            })

        if not euler_closed:
            findings.append({
                "type": "euler_gap_open",
                "berry_phase": round(berry_phase, 4),
            })

        if not findings:
            return None

        reasons = ";".join(f["type"] for f in findings)
        self.wake_count += 1
        self.last_wake_utc = datetime.now(timezone.utc).isoformat()
        self.findings = findings

        return {
            "schema": "NOEMA_WAKE_SIGNAL_V1",
            "wake_utc": self.last_wake_utc,
            "reason": reasons,
            "context": {"findings": findings, "R": round(R, 6), "error_count": len(findings)},
        }


# ── Phase Lane Bank (8-channel) ────────────────────────────────────────────
# Renamed from HolonomicMemory to avoid collision with
# ciel_omega/memory/holonomic_memory.py (SQLite retrieval layer, 870 lines).

@dataclass
class PhaseLaneBank:
    """8-channel phase attractor system for M0-M7 memory lanes.

    Each channel maintains a complex phase z_k = r_k·e^{iφ_k} that evolves
    toward an attractor determined by the surface order parameter.
    """
    n_channels: int = 8
    dt: float = 0.01

    def __post_init__(self):
        self.phases: np.ndarray = np.random.uniform(0, 2 * math.pi, self.n_channels)
        self.velocities: np.ndarray = np.zeros(self.n_channels)
        self.identity_phase: float = 0.0
        self.attractor: np.ndarray = np.zeros(3)
        self._time: float = 0.0
        self._cycle: int = 0

    def step(self, surface_phi: np.ndarray) -> None:
        """Pull channel phases toward surface order parameter."""
        Z1 = np.mean(np.exp(1j * surface_phi))
        R = float(abs(Z1))
        psi = float(np.angle(Z1))

        target = np.linspace(0, 2 * math.pi, self.n_channels) + psi
        diff = np.angle(np.exp(1j * (target - self.phases)))
        self.velocities = 0.3 * R * diff - 0.1 * self.velocities
        self.phases += self.dt * self.velocities
        self.phases %= 2 * math.pi

        self.identity_phase = float(np.mean(self.phases))
        self.attractor = np.array([R, psi, self.identity_phase])
        self._time += self.dt
        self._cycle += 1

    def snapshot(self) -> dict[str, Any]:
        return {
            "schema": "HOLONOMIC_MEMORY_STATE_V0_1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "identity_phase": round(self.identity_phase, 6),
            "attractor_vector": [round(float(x), 6) for x in self.attractor],
            "anchors": [],
            "phases": [round(float(p), 6) for p in self.phases],
            "velocities": [round(float(v), 6) for v in self.velocities],
            "time": round(self._time, 6),
            "timestep": self._cycle,
            "cycle_index": self._cycle,
        }


# ── Top-Level Subconscious ────────────────────────────────────────────────

@dataclass
class Subconscious:
    """Aggregates all subconscious modules into one interface."""
    zeta: ZetaSchrodinger = field(default_factory=ZetaSchrodinger)
    berry: BerryPhaseTracker = field(default_factory=BerryPhaseTracker)
    wake: WakeSignalGenerator = field(default_factory=WakeSignalGenerator)
    holonomic: PhaseLaneBank = field(default_factory=PhaseLaneBank)

    def step_all(
        self,
        surface_phi: np.ndarray,
        dt: float = 0.01,
        memory_hours: dict[str, float] | None = None,
    ) -> dict[str, Any]:
        R = float(abs(np.mean(np.exp(1j * surface_phi))))
        psi = float(np.angle(np.mean(np.exp(1j * surface_phi))))

        if self.zeta.amplitude < 0.01:
            self.zeta.seed_from_surface(surface_phi)

        self.zeta.step(dt)
        self.berry.update(R, psi, dt)
        self.holonomic.step(surface_phi)
        wake_signal = self.wake.evaluate(
            memory_hours=memory_hours,
            R=R,
            tracked_count=8,
            euler_closed=self.berry.euler_gap < 0.1,
            berry_phase=self.berry.berry_phase,
        )

        result: dict[str, Any] = {
            "tick": self.holonomic._cycle,
            "R": round(R, 6),
            "psi": round(psi, 6),
            "zet_amplitude": round(self.zeta.amplitude, 6),
            "zet_collatz_entropy": round(self.zeta.collatz_entropy, 6),
            "berry_phase": round(self.berry.berry_phase, 6),
            "euler_gap": round(self.berry.euler_gap, 6),
            "euler_closed": self.berry.euler_gap < 0.1,
            "holonomic_identity_phase": round(self.holonomic.identity_phase, 6),
        }
        if wake_signal:
            result["wake"] = wake_signal

        return result

    def snapshot(self) -> dict[str, Any]:
        return {
            "zeta": self.zeta.snapshot(),
            "berry": {
                **self.berry.snapshot(0.0, 0.0),
                "history": [],
            },
            "holonomic": self.holonomic.snapshot(),
        }
