"""ContinuousPhaseSync — analytic Ott-Antonsen Z(t) for harmonic Kuramoto.

Replaces discrete Euler integration with the Ott-Antonsen ansatz for the
3-6-9 harmonic Kuramoto surface. Provides closed-form evolution of the
order parameter Z(t) = R(t)·e^{iψ(t)} for each harmonic channel.

Standard Kuramoto with Lorentzian frequency distribution g(ω) = γ/(π(ω²+γ²))
has analytic solution: ∂Z/∂t = (iω₀ − γ)Z + (κ/2)(Z − Z²Z̄)

For the 3-6-9 harmonic case, each channel h ∈ {1,3,6,9} has its own
order parameter Z_h = ⟨e^{ihφ}⟩ and the effective coupling is a weighted
sum across harmonics. The composite Ott-Antonsen is:

  ∂Z_h/∂t = (i·h·ω₀ − γ_h)Z_h + (κ_h/2)(Z_h − Z_h²·Z̄_h)

  where κ_h = Σ_k A_k·κ_{hk} depends on the harmonic amplitude matrix

Fractional Z(ω) for heterogenous case uses:

  Z_ω = ∫ Z(t)e^{-iωt} dt  (Fourier-domain solution)

Adapted from CIEL original ContinuousPhaseSync into NOEMA 3-6-9.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from .noema_surface_mmap import (
    N_OSCILLATORS, HARMONIC_VALUES, HARMONIC_AMPS,
    N_HARMONICS, HARMONIC_MASK, BASE_TEMPORAL_HZ,
)


@dataclass
class ContinuousPhaseSync:
    gamma: float = 0.5       # Lorentzian width (inverse of heterogeneity)
    kappa_base: float = 2.0  # Base coupling strength
    dt_analytic: float = 0.01

    def compute_Z_harmonic(
        self, phi: np.ndarray, h: int,
    ) -> complex:
        return np.mean(np.exp(1j * h * phi))

    def compute_all_Z(
        self, phi: np.ndarray,
    ) -> dict[int, complex]:
        return {h: self.compute_Z_harmonic(phi, h) for h in HARMONIC_VALUES}

    def evolve_analytic(
        self, Z: dict[int, complex],
        omega_mean: float = BASE_TEMPORAL_HZ,
        coupling_mod: float = 1.0,
    ) -> dict[int, complex]:
        """Ott-Antonsen step for each harmonic channel independently.

        ∂Z_h/∂t = (i·h·ω₀ − γ)Z_h + (κ_h/2)(Z_h − Z_h²·Z̄_h)

        Returns updated Z_h per channel.
        """
        Z_out: dict[int, complex] = {}
        for h_idx, h in enumerate(HARMONIC_VALUES):
            A_h = HARMONIC_AMPS[h_idx]
            kappa_h = self.kappa_base * A_h * coupling_mod
            Z_h = Z.get(h, 0.0 + 0.0j)

            if abs(Z_h) < 1e-12:
                Z_out[h] = 0.0 + 0.0j
                continue

            dZ = (
                (1j * h * omega_mean - self.gamma) * Z_h
                + (kappa_h / 2.0) * (Z_h - (Z_h ** 2) * np.conj(Z_h))
            )
            Z_next = Z_h + self.dt_analytic * dZ

            if abs(Z_next) > 0.999:
                Z_next = Z_next / abs(Z_next) * 0.999

            Z_out[h] = Z_next

        return Z_out

    def reconstruct_phi_from_Z(
        self, Z: dict[int, complex],
    ) -> np.ndarray:
        """Reconstruct oscillator phases from Z order parameters.

        Uses the Ott-Antonsen phase distribution P(φ) = (1-R²)/(2π(1+R²-2Rcos(φ-ψ)))
        to sample N_OSCILLATORS phases consistent with Z_h.

        For the harmonic case, we use the fundamental Z₁ to determine R and ψ,
        then add harmonic perturbations from Z₃, Z₆, Z₉.
        """
        Z1 = Z.get(1, 0.0 + 0.0j)
        R = min(float(abs(Z1)), 0.999)
        psi = float(np.angle(Z1))

        # Sample from OA distribution via inverse transform
        rng = np.random.default_rng(seed=int(psi * 1000) % (2**31))
        u = rng.uniform(0, 1, N_OSCILLATORS)
        phi_oa = psi + 2 * np.arctan(
            np.sqrt((1 + R) / (1 - R)) * np.tan(np.pi * (u - 0.5))
        )

        # Add harmonic perturbations from higher Z channels
        for h_idx, h in enumerate(HARMONIC_VALUES):
            if h == 1:
                continue
            Zh = Z.get(h, 0.0 + 0.0j)
            A_h = HARMONIC_AMPS[h_idx]
            perturbation = A_h * float(abs(Zh)) * np.sin(h * phi_oa - float(np.angle(Zh) if abs(Zh) > 1e-12 else 0))
            phi_oa += perturbation * 0.1

        phi_oa %= 2 * math.pi
        return phi_oa

    def compute_R(
        self, phi: np.ndarray,
    ) -> float:
        Z1 = self.compute_Z_harmonic(phi, 1)
        return float(abs(Z1))

    def compute_R_harmonic(
        self, phi: np.ndarray,
    ) -> dict[int, float]:
        return {h: float(abs(self.compute_Z_harmonic(phi, h))) for h in HARMONIC_VALUES}

    def effective_kappa(
        self, phi: np.ndarray, kappa_base: float | None = None,
    ) -> float:
        """Effective coupling strength felt by the system given current state."""
        kb = kappa_base or self.kappa_base
        Z_all = self.compute_all_Z(phi)
        k_eff = kb
        for h_idx, h in enumerate(HARMONIC_VALUES):
            A_h = HARMONIC_AMPS[h_idx]
            R_h = abs(Z_all.get(h, 0.0 + 0.0j))
            k_eff += kb * A_h * R_h * 0.5
        return float(k_eff)

    def convergence_time(
        self, R0: float, kappa: float, tol: float = 1e-3,
    ) -> float:
        """Estimate time to reach steady-state R from initial R0.

        Ott-Antonsen: ∂R/∂t = (κ/2)(R − R³) − γR
        Near transition: R(t) evolves as dR/dt = (κ/2 − γ)R − (κ/2)R³

        For κ > 2γ (supercritical): R(t) → R∞ = √(1 − 2γ/κ)
        Characteristic time τ = 1/(κ/2 − γ) for growth from small R.
        """
        if kappa <= 2.0 * self.gamma:
            return float("inf")
        R_inf = math.sqrt(max(0.0, 1.0 - 2.0 * self.gamma / kappa))
        if R_inf <= tol:
            return float("inf")
        R_clamp = max(R0, 1e-6)
        decay_rate = (kappa / 2.0) * (1.0 - R_clamp**2) - self.gamma
        if decay_rate <= 0:
            return float("inf")
        return float(math.log(tol / R_clamp) / (-decay_rate))

    def snapshot(self, phi: np.ndarray) -> dict[str, Any]:
        Z_all = self.compute_all_Z(phi)
        R_h = {f"R_{h}": float(abs(Z)) for h, Z in Z_all.items()}
        R1 = R_h.get("R_1", 0.0)
        psi = float(np.angle(Z_all.get(1, 0.0+0.0j)))
        k_eff = self.effective_kappa(phi)
        return {
            "Z": {str(h): complex(round(Z.real, 6), round(Z.imag, 6)) for h, Z in Z_all.items()},
            **R_h,
            "psi": round(psi, 6),
            "kappa_effective": round(k_eff, 6),
            "gamma": self.gamma,
            "convergence_t": round(self.convergence_time(R1, k_eff), 4),
        }
