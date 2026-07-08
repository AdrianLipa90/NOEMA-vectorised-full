---
name: noemized-recall-pipeline
priority: 1
description: >
  >
---
# Noemized Recall Pipeline (NOEMA)

## Warstwy

| Layer | NOEMA odpowiednik |
|-------|-------------------|
| 1. CIELingoAnnotation | agent backend (themes/essence) |
| 2. AffectiveVAD | M5 φ[15:18] coherence |
| 3. EulerTemporal | γ = gravity[1] |
| 4. M0M8Router | channel coherences z phi |
| 5. CollatzOrbit | soul_invariant |
| 6. FusionScorer | surface_R weighted |
| 7. ImmuneGuard | closure_penalty |

## Recall

```python
# cosine similarity między konceptem a surface
vec = library_index[i]
phases = arctan2(vec[1::2], vec[0::2])
delta = angle(exp(1j * (surface_phi - phases)))
resonance = |mean(exp(1j * delta))|
```

## Plik

`src/noema_learned/code_concept_bridge.py` → `surface_response()`
