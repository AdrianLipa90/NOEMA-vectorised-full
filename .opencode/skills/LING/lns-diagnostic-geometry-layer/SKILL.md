---
name: diagnostic-geometry-layer
priority: 3
description: >
  >
---
# 39. Diagnostic Geometry Layer

## Contents

- **Purpose**: The layer adds diagnostics for: - cross-language grammar-gauge reconstruction cost, - operator incidence and operator de
- **Principle**: ```text Diagnostics do not prove semantic correctness. Diagnostics expose where semantic correctness must be checked. ``
- **Main artifacts**: ```text data/diagnostics/global_diagnostic_summary_v2_0.json data/diagnostics/cross_language_reconstruction_costs.csv da
- **Interpretation**: A high grammar-gauge distance does not mean translation failure. It means more structure must be rec A dense operator pr

## Key Points

- cross-language grammar-gauge reconstruction cost,
- operator incidence and operator density,
- relation-type density by domain,
- global concept/operator graph growth,
- conflict, ambiguity, and unresolved-state tracking.

## Code

```
The diagnostics are intentionally conservative. Warnings are preserved rather than smoothed away. Missing or unresolved states are valid seed states when explicitly reported.

## Main artifacts
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/39_DIAGNOSTIC_GEOMETRY_LAYER.md` (43 lines, 1776B)*