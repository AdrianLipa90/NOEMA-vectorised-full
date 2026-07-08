---
name: semantic-affective-fusion
priority: 1
description: >
  >
---
# Semantic-Affective Fusion (NOEMA)

## Surface mapping

| Komponent | Lokalizacja | Zakres |
|-----------|-------------|--------|
| semantic_density | gravity[0] | [0, ~1.5] |
| tau_dilation (γ) | gravity[1] | [1, 10] |
| M5 coherence | |M5(exp(iφ))| | [0, 1] |
| M6 coherence | |M6(exp(iφ))| | [0, 1] |

## Fusion

```
F_sa = 0.4 · gravity[0] + 0.3 · coh(M5) + 0.3 · gravity[0] · coh(M5)
```

Zanika gdy γ > 5 (TARDIS time dilation rozrzedza fuzję).
