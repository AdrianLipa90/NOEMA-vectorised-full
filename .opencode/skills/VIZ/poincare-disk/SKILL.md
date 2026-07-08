---
name: poincare-disk
priority: 1
description: >
  >
---
# Poincaré Disk

## Mapping

```python
θ ∈ [0, π/2) → ρ = tanh(tan(θ/2)) ∈ [0, 1)     # poincare_radius
(coupling, phase) → (ρ·cos(phase), ρ·sin(phase))  # entity_to_disk
```

## Hyperbolic distance

```
d(a,b) = acosh(1 + 2·(r_a² + r_b² - 2·r_a·r_b·cos(Δφ)) / ((1-r_a²)·(1-r_b²)))
```

## Orbital bridge

OrchOrbital: entity_count=21, mean_coupling=0.8514
- Adrian_Lipa: coupling=0.97 (konstytutywny)
- relational_contract: coupling=1.0 (nienaruszalny)
- Berry_holonomy: coupling=0.93 (geometryczna tożsamość)

## Plik

`src/ciel_geometry/disk.py`
