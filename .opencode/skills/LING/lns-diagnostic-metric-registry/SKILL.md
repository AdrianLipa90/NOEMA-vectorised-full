---
name: diagnostic-metric-registry
priority: 3
description: >
  >
---
# 40. Diagnostic Metric Registry

## Contents

- **language_panel_coverage**: Observed language panels divided by expected `concepts × 5` panels. A value below 1 means at least o
- **operator_coverage**: Fraction of concepts with at least one operator hook. Low coverage means the library may contain sem
- **relation_density**: Directed relation count divided by `N × (N - 1)`. This is a graph sparsity signal, not a quality sco
- **case_reconstruction_cost_mean**: Average cost for reconstructing case-gauge information in languages that express roles through word 
- **Review principle**: Metrics must generate review actions: add missing panels, add operator hooks, mark unresolved, split

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/40_DIAGNOSTIC_METRIC_REGISTRY.md` (27 lines, 1084B)*