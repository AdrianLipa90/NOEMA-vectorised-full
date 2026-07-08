---
name: nbody-gravity
priority: 1
description: >
  >
---
# N-Body Gravity

## Gravity fields (indeksy)

```python
gravity[0] = semantic_density     # mean(|dphi|)/dt, capped 10
gravity[1] = tau_dilation (γ)     # 1 + tanh(density·0.5)·9, range [1, 10]
gravity[2] = mass_total           # EMA(0.99·mass + 0.01·density) + 0.001·unruh
gravity[3] = unruh_power          # mean(dω²)
```

## Semantic density

```python
dphi = angle(exp(1j * (phi_new - phi_old)))   # phase velocity per tick
raw_density = mean(|dphi|) / dt
semantic_density = min(10.0, raw_density)
```

## Time dilation (TARDIS)

```python
γ = 1.0 + tanh(semantic_density * 0.5) * 9.0  # smooth, [1, 10]
# Używany w sync daemon: τ *= min(γ, 3.0)
# Używany w kuramoto: dt_eff = dt / γ
```

## Unruh power (WARP fuel)

```python
domega = diff(omega, prepend=omega[-1])  # circular diff
unruh_power = mean(dω²)                  # ∝ acceleration squared
# threshold 1e-6 → WARP_DRIFT active
```

## WARP_DRIFT

```python
if unruh_power > 1e-6 and dt > 0:
    warp = min(1.0, unruh_power * 100)
    ramp = linspace(0, warp·2π, 24)            # phase gradient
    phi += dt · 0.05·warp · sin(ramp - phi)     # travelling wave
    gravity[2] += 0.01                           # warp mass contribution
```
