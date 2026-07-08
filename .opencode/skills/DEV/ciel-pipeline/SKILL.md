---
name: ciel-pipeline
priority: 1
description: >
  >
---
# CIEL Pipeline

## CielEngine.step() — 12 kroków

```
Step 1:  intention_12d → intention vector
Step 2:  simulation(sector) → simulated state
Step 3:  CQCL decomposition
Step 4:  emotion → affect vector
Step 5:  soul_invariant
Step 5b: CIELingo understand_query() → immune flags
         → ethical_score capped (source_confusion→0.35, authority_risk→0.2)
Step 6-10: ethics → memory → info flow → nonlocal → inference → euler → orbital
Step 11b: CIELingo MeaningLoop → SemanticScar → repair_candidates
Step 12:  NOEMA surface bridge → TieredMemoryOrchestrator.write()
```

## Immune flags (CIELingo)

| Flag | Threshold | Efekt |
|------|-----------|-------|
| `source_confusion` | boolean | cap ethical_score at 0.35 |
| `authority_risk` | > 0.5 | cap ethical_score at 0.2 |
| `consent_bypass` | boolean | blocks response |
| `source_required` | boolean | blocks response |

## Meaning scars

`MISSING_SOURCE`, `AUTHORITY_LEAK`, `COUPLING_RESIDUE`, `FALSE_CLOSURE`
→ `build_global_meaning_signal()` → severity + repair_required

## Return dict

```python
{
    "status", "intention", "simulation", "emotion", ...,
    "cielingo_immune": {source_confusion, consent_bypass, authority_risk, source_required},
    "cielingo_meaning": {severity, repair_required, repair_candidates, unresolved_scars},
}
```

## Użycie

```python
from ciel_sot_agent.engine import CielEngine
engine = CielEngine()
result = engine.step(user_input)
```

## Plik

`src/ciel_sot_agent/engine.py`
