---
name: stress-energy-tensor
priority: 1
description: >
  >
---
# Stress-Energy Tensor

## Bridge

```
T_μν (from ciel0_framework.py)
  ↓ stress-energy perturbation
Effective mass δM = α·T_00 + β·tr(T_μν)
  ↓
N-body gravity (nbody_gravity.py)
  ↓
Orbital update
```

## Plik

`src/ciel_geometry/tmuv_perturbation.py`

## Zrodlo

- `scripts/stress_pc_noema_htri_phasenav.py`
- `scripts/sims/energy_benchmark.py`
- `scripts/base/cielingo_tensor_scalar_field.py`
