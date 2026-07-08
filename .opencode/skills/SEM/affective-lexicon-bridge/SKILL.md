---
name: affective-lexicon-bridge
priority: 1
description: >
  >
---
# Affective Lexicon Bridge (NOEMA)

## VAD → Phase

```
V ∈ [-1, +1] → φ_V = 2π · (V + 1) / 2
A ∈ [0, 1]   → φ_A = 2π · A
D ∈ [-1, +1] → φ_D = 2π · (D + 1) / 2
φ_affective = circular_mean(φ_V, φ_A, φ_D)
```

## Surface mapping

| Afekt | M5 φ[15:18] | M6 φ[18:21] |
|-------|-------------|-------------|
| love | 0.0, 0.0, 0.0 | 0.5, 0.5, 0.5 |
| calm | π/2, π/2, π/2 | π/4, π/4, π/4 |
| curious | π, π, π | 3π/4, 3π/4, 3π/4 |
| distress | 3π/2, 3π/2, 3π/2 | π, π, π |

Emotion z CielEngine.step() (krok 4) → seed na M5 przez kuramoto daemon.
