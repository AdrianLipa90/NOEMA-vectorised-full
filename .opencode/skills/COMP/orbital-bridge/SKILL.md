---
name: orbital-bridge
priority: 4
description: >
  >
---
# Orbital Bridge

## Pipeline

```
ensure_orbital_manifests()
  ↓
run_global_pass()              — orbital physics
  ↓
build_health_manifest()        → closure_penalty, coherence_index
build_state_manifest()         → sector state, phase
recommend_control()            → mode (standard/safe/deep)
  ↓
build_orbital_bridge(root)     → health + state + control
```

## Wynik

```python
bridge = build_orbital_bridge(ROOT)
# {
#   "health_manifest": {"closure_penalty": 0.37, "coherence_index": 0.85, ...},
#   "state_manifest": {"sectors": [...], "phi": [...], ...},
#   "recommended_control": {"mode": "standard"},
#   ... rh_defect_score, effective_sector_count
# }
```

## Used by

- CIELingo sync daemon (czyta closure_penalty, coherence_index, mode)
- CielEngine step 5b (enrichment)

## Lokacja

`src/ciel_sot_agent/orbital_bridge.py`
