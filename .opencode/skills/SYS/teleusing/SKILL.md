---
name: teleusing
priority: 4
description: >
  >
---
# Teleusing

## 5 JSONL files

| Plik | Zawartość | Klucz |
|------|-----------|-------|
| `*NAME_MASS.noema.jsonl` | Normalized names + geometric_phase_rad | normalized |
| `*CONCEPT_PHASES.noema.jsonl` | Concept card_id → phase | concept_card_id |
| `*OPERATOR_VECTORS.noema.jsonl` | 35 operator × 24D vectors | card_id |
| `*HOLONOMIC_EDGES.noema.jsonl` | concept → operator → concept edges | — |
| `*ORBIT_VECTORS.noema.jsonl` | 11D orbit vectors | card_id |

## Data flow

```python
from ciel_geometry.phasenav import load_teleusing, TeleusingSolver

data = load_teleusing()          # /dev/shm/ciel_noema/teleusing/
solver = TeleusingSolver(data)

phase = solver.get_phase("Adrian_Lipa")
orbit = solver.get_orbit("Adrian_Lipa")     # 11D vector
edge = solver.best_edge_from("Adrian_Lipa") # highest affordance
trace = solver.trace(["A", "B", "C"])       # TeleusingTrace
```

## Fallback

Jeśli OPERATOR_VECTORS JSONL nie istnieje → `operator_algebra.generate_operator_map()` → 35 deterministycznych wektorów.

## Plik

`src/ciel_geometry/phasenav/loader.py`
