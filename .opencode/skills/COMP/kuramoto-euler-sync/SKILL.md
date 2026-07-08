---
name: kuramoto-euler-sync
priority: 1
description: >
  >
---
# Kuramoto Euler Sync

## Euler constraint

```python
R = |Σ e^{iφ_i}|
target: R = 0 → Σ e^{iφ_i} = 0
φ_target_i = angle(-Σ_{j≠i} e^{iφ_j})
```

## Live system

| Parametr | Wartość |
|----------|---------|
| Daemon | `ciel_noema_kuramoto_daemon.py` |
| Interval | 10Hz (0.1s) |
| N | 24 (HTRI) |
| harmonics | {1, 3, 6, 9} per oscillator |
| Euler residual R | 3-4 (target: 0) |
| τ̄ | 0.35-0.55 |

Euler feedback: `τ_i += 0.05 * R * cos(φ_target - φ_i) - 0.02 * (τ - 0.353)`
