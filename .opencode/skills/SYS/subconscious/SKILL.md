---
name: subconscious
priority: 1
description: >
  >
---
# Subconscious

## ZetaSchrodinger

```python
@dataclass
class ZetaSchrodinger:
    N_POINTS: int = 68
    dx: float = 0.05
    gamma_dissipation: float = 0.02
    zeta_strength: float = 0.3
    hbar: float = 1.0
    mass: float = 1.0
```

Równanie:
```
∂ψ/∂t = -i·(H₀ + V_zeta)·ψ + γ·(1 − |ψ|²)·ψ
V_zeta = ζ·log(1 + H_collatz(|ψ|²))  — self-interaction z Collatz entropy
```

## WakeSignal

Sygnał konsolidacji z:
- memory aging (jak stara pamięć)
- resonance drift (dryf rezonansu)
- phase mismatch

## BerryPhase

Adiabatic geometric phase z neutrino mixing evolution.

## Lokacja

`src/ciel_geometry/subconscious.py`
