---
name: continuous-propagator
priority: 1
description: >
  >
---
# Continuous Propagator

## Signatura

```python
def evolve_continuous(
    phi_knots: np.ndarray,       # 24 control points (radians)
    dt: float = 0.01,
    hbar: float = 0.1,
    coupling: np.ndarray | None = None,   # 24 — Kuramoto drive
    omega_eff: np.ndarray | None = None,  # 24 — effective frequencies
) -> tuple[np.ndarray, float, float]:
```

## Pipeline

```
φ_knots (24)
  ↓ C² spline (periodic BC)
φ(θ) on [0, 2π)
  ↓ evaluate 512-point dense grid
φ_dense, d²φ/dθ²
  ↓
H_kinetic = -ħ/2 · d²φ/dθ²          # kinetic energy
V_zeta = Σ_{n=1}^{32} cos(n·φ)/n^{1.5}  # Riemann ζ potential
H_drive = ω + g·sin(φ(θ)-φ(θ+δθ))  # Kuramoto drive
  ↓
φ_new = φ + dt · (H_kinetic + V_zeta + H_drive)
  ↓ project back to 24 knots
φ_knots_new
```

## Use

Wywoływany z evolve_surface() co cont_every=10 ticków.
Jeśli import/call fail → cichy fallback do Euler.

## Riemann ζ potential

```python
V(φ) = cos(φ)/1^1.5 + cos(2φ)/2^1.5 + cos(3φ)/3^1.5 + ... + cos(32φ)/32^1.5
```

Tworzy potencjał z seria harmonicznych o ζ(1.5) wagach — preferuje niskie częstotliwości.

## Plik

`src/ciel_geometry/phasenav/continuous_propagator.py`
