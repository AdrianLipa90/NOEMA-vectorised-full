---
name: cielingo-bridge
priority: 1
description: >
  >
---
# CIELingo Bridge

## Loop

```
CIELingo MeaningLoop
  ↓ closure_penalty (cp)
D_f = 2.57 - 0.57 * min(1.0, cp/1.5)
  ↓ flavor[5]
neutrino daemon → Λ = (D_f - 2) / 0.57
  ↓ flavor[4]
PMNS boost → g_boost → W_ij blend
  ↓ W_ij override
CIELingo reads override → cp
```

## CIELingo in CielEngine

| Step | Co robi |
|------|---------|
| 5b | `understand_query()` → immune flags (source_confusion, consent_bypass, authority_risk) |
| 6 | immune flags cap ethical_score |
| 11b | `MeaningLoop` → `SemanticScar[]` → `MeaningRepairCandidate[]` → severity |
| 12 | bridge metadata: `cielingo_severity`, `cielingo_repair_required`, `cielingo_repair_candidates` |

## Pliki

- `scripts/ciel_noema_cielingo_sync.py`
- `src/ciel_sot_agent/engine.py` (steps 5b, 11b, 12)
