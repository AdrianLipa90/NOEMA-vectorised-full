---
name: ciel-engine-subsystem
priority: 1
description: >
  >
---
# CielEngine Subsystem

## 12 kroków

| Step | Co robi |
|------|---------|
| 1 | intention_12d — wektor intencji |
| 2 | simulation — CQCL symulacja |
| 3 | CQCL — logiczna konsystencja |
| 4 | emotion — VAD → dominant_emotion |
| 5 | soul_invariant — topologiczna ochrona |
| 5b | CIELingo immune — understand_query → flags |
| 6 | ethics — immune flags cap ethical_score |
| 7 | memory — memory_state |
| 8 | information flow — nonlocal channel |
| 9 | nonlocal — inter-agent |
| 10 | inference — euler constraint |
| 11 | euler → orbital → CIELingo MeaningLoop |
| 11b | CIELingo meaning_signal_bridge → severity |
| 12 | NOEMA surface bridge → write |

## Return

```python
{
  "status", "intention", "simulation", "emotion", ...,
  "cielingo_immune": {...},
  "cielingo_meaning": {...}
}
```

## Plik

`src/ciel_sot_agent/engine.py`
