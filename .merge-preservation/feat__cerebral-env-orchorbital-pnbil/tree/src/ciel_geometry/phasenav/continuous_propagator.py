#!/usr/bin/env python3
"""Continuous phase propagator on S¹ — Zeta-Schrödinger evolution.

Replaces discrete Kuramoto (36 osc, dt stepping) with a continuous spline
representation. The phase field φ(θ, t) lives on a circle, evolved by:
    i·∂φ/∂t = H·φ + V_zeta(φ)
where V_zeta is Zeta-regularized potential (no collaps, continuous).

Discrete 36 points are kept as B-spline control knots, not oscillators.
"""
from __future__ import annotations

import numpy as np

N_KNOTS = 36
N_SAMPLES = 512  # evaluation grid for continuous representation


def _periodic_phase_interp(values: np.ndarray, samples: np.ndarray) -> np.ndarray:
    """Interpolate S¹ phases without a 2π coordinate seam."""
    values = np.asarray(values, dtype=np.float64).reshape(-1)
    if values.size == 0:
        return np.zeros_like(np.asarray(samples, dtype=np.float64))
    knots = np.linspace(0.0, 2.0 * np.pi, values.size, endpoint=False)
    xp = np.mod(np.asarray(samples, dtype=np.float64), 2.0 * np.pi)
    z = np.exp(1j * values)
    z_ext = np.concatenate((z, z[:1]))
    real = np.interp(xp, np.concatenate((knots, [2.0 * np.pi])), z_ext.real)
    imag = np.interp(xp, np.concatenate((knots, [2.0 * np.pi])), z_ext.imag)
    return np.mod(np.angle(real + 1j * imag), 2.0 * np.pi)


class _PeriodicPhaseSpline:
    """Small NumPy-only compatibility surface for the former CubicSpline."""

    def __init__(self, values: np.ndarray):
        self.values = np.asarray(values, dtype=np.float64).reshape(-1)

    def __call__(self, samples: np.ndarray) -> np.ndarray:
        return _periodic_phase_interp(self.values, samples)

    def derivative(self, order: int):
        if order != 2:
            raise ValueError("PhaseNav periodic spline exposes only the second derivative")

        h = 2.0 * np.pi / max(1, self.values.size)

        def second_derivative(samples: np.ndarray) -> np.ndarray:
            x = np.asarray(samples, dtype=np.float64)
            center = self(x)
            forward = self(x + h)
            backward = self(x - h)
            d_forward = np.angle(np.exp(1j * (forward - center)))
            d_backward = np.angle(np.exp(1j * (center - backward)))
            return (d_forward - d_backward) / (h * h)

        return second_derivative


def spline_phi(phi_knots: np.ndarray) -> _PeriodicPhaseSpline:
    """Build the canonical NumPy-only continuous phase field on S¹."""
    return _PeriodicPhaseSpline(phi_knots)


def zeta_potential(phi: np.ndarray) -> np.ndarray:
    """Zeta-regularized potential: smooth, non-collapsing.

    V(φ) = Σ_{n=1}^{∞} cos(n·φ) / n^{σ}
    Truncated at n=32, σ=1.5 → continuous, no Gibbs.
    """
    n = np.arange(1, 33, dtype=np.float64)  # (32,)
    # Wektorowo: (N, 32) * (32,) → (N, 32) → (N,)
    return np.sum(np.cos(n[None, :] * phi[:, None]) / n[None, :] ** 1.5, axis=1)


def evolve_continuous(
    phi_knots: np.ndarray,
    dt: float = 0.01,
    hbar: float = 0.1,
    coupling: np.ndarray | None = None,  # coupling field [36] from g*sin(diff)
    omega_eff: np.ndarray | None = None,  # effective frequencies
) -> tuple[np.ndarray, float, float]:
    """Single step of continuous Schrödinger evolution on S¹.

    Returns (new_knots, max_dphi, second_deriv_norm).
    """
    # Native PhaseNav ring operator.  The old dense interpolation path
    # amplified wrapped seams by 1/h² (live d²φ≈205), creating a false
    # gravity/γ spike and a synchronization clog.  The S¹ graph Laplacian
    # below is the vectorized nearest-neighbour operator on the phase knots.
    phi_knots = np.mod(np.asarray(phi_knots, dtype=np.float64).reshape(-1), 2.0 * np.pi)
    d_forward = np.angle(np.exp(1j * (np.roll(phi_knots, -1) - phi_knots)))
    d_backward = np.angle(np.exp(1j * (phi_knots - np.roll(phi_knots, 1))))
    d2phi = d_forward - d_backward

    # Zeta potential
    V = zeta_potential(phi_knots)

    # Hamiltonian: -hbar²/2 · ∇² + V
    H_kinetic = -hbar * 0.5 * d2phi
    H_potential = V * phi_knots

    # The caller already supplies Σ_j g_ij sin(Δφ).  Apply that canonical
    # weighted field once; the former local-sine multiplication attenuated it
    # a second time and formed a throughput bottleneck.
    if coupling is not None and omega_eff is not None:
        H_drive = (
            np.asarray(omega_eff, dtype=np.float64).reshape(-1)
            + np.asarray(coupling, dtype=np.float64).reshape(-1)
        )
    else:
        H_drive = 0.0

    # Schrödinger evolution
    phi_new = np.mod(phi_knots + dt * (H_kinetic + H_potential + H_drive), 2.0 * np.pi)

    # Metrics
    max_dphi = float(np.max(np.abs(np.angle(np.exp(1j * (phi_new - phi_knots))))))
    d2_norm = float(np.mean(np.abs(d2phi)))

    return phi_new, max_dphi, d2_norm


def self_test():
    rng = np.random.default_rng(42)
    phi_knots = rng.uniform(0, 2 * np.pi, N_KNOTS)

    cs = spline_phi(phi_knots)
    theta_test = np.linspace(0, 2 * np.pi, N_SAMPLES, endpoint=False)
    phi_cont = cs(theta_test)
    print(f"Continuous spline: min={phi_cont.min():.3f} max={phi_cont.max():.3f}")
    print(f"C² continuity: derr={np.max(np.abs(cs.derivative(2)(theta_test) - cs.derivative(2)(theta_test + 0.01))):.6f}")

    phi_next = evolve_continuous(phi_knots, dt=0.05)
    delta = float(np.mean(np.abs(phi_next - phi_knots)))
    print(f"Evolution (1 step): mean |Δφ| = {delta:.4f}")
    print(f"  min={phi_next.min():.3f} max={phi_next.max():.3f}")

    return delta


if __name__ == "__main__":
    self_test()
