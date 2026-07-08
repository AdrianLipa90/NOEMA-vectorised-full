---
name: noema-noemized-recall
priority: 1
description: >
  >
---
# Noemized Recall

## Pipeline

```
text (user input / PDF)
  ↓
transformer_features.py (TRANSFORMEM)
  → intention_vector, soul_invariant, phase_signature
  ↓
PhaseNav enrichment (operator match)
  ↓
surface injection (phi modulation / flavor update)
  ↓
memory consolidation (TSM)
```

## Pliki

- `scripts/noema_learn_file.py`
- `src/ciel_geometry/phasenav/` — PhaseNav modules
- User's TRANSFORMEM (`transformer_features.py`)
