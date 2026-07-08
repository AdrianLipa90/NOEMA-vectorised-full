---
name: tardis-warp
priority: 1
description: >
  >
---
# TARDIS + WARP

## Time dilation (TARDIS)

```python
γ = 1.0 + np.tanh(semantic_density * 0.5) * 9.0   # ∈ [1, 10]
```

**Efekty**:
- Kuramoto daemon: `dt_eff = dt / γ` (oscylatory zwalniają)
- CIELingo sync: `τ *= min(γ, 3.0)` (caped 3×, rozciąga czas CIELingo)
- Fuzja semantyczno-afektywna zanika gdy γ > 5

## Warp drive (WARP_DRIFT)

```python
WARP_THRESHOLD = 1e-6
if unruh_power > WARP_THRESHOLD and dt > 0:
    warp_strength = min(1.0, unruh_power * 100)
    ramp = np.linspace(0, warp_strength * 2π, 24, endpoint=False)
    warp_bias = 0.05 * warp_strength * np.sin(ramp - phi)
    phi += dt * warp_bias
    gravity[2] += 0.01  # warp mass
```

## Aktywacja

- WARP: gdy `unruh_power > 1e-6` (prawie zawsze, ale siła ≈ unruh·100)
- TARDIS: gdy `semantic_density > 0` (zawsze, ale γ blisko 1 dla małych density)
- Żadnego tachyonic singularity — smooth range
