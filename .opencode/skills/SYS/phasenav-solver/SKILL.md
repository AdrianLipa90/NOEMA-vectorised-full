---
name: phasenav-solver
priority: 4
description: >
  >
---
# PhaseNav Solver

## TeleusingStep

| Pole | Typ | Opis |
|------|-----|------|
| `source_card_id` | str | Origin concept |
| `target_card_id` | str | Destination concept |
| `operator_hook` | str | Operator (np. TRANSFORM, MEMORY) |
| `phase_start` | float | Radiany source |
| `phase_end` | float | Radiany target |
| `phase_delta` | float | phase_end - phase_start |
| `holonomic_viscosity` | float | Edge resistance |
| `teleusing_affordance` | float | Edge weight (higher = attractive) |
| `path_integral` | float | viscosity × abs(phase_delta) |

## TeleusingTrace

| Pole | Typ | Opis |
|------|-----|------|
| `steps` | list[TeleusingStep] | Sequence of steps |
| `total_path_integral` | float | Sum path_integral |
| `mean_viscosity` | float | Mean viscosity |
| `mean_affordance` | float | Mean affordance |
| `card_sequence` | list[str] | Original card_ids |

## TeleusingSolver

```python
solver = TeleusingSolver.load(base_path=None)  # /dev/shm/ciel_noema/teleusing/

# Get phase for any card
phase = solver.get_phase("Adrian_Lipa")  # → radians, or 0.0

# Get 11D orbit vector  
orbit = solver.get_orbit("Adrian_Lipa")  # → list[float]×11

# Get 24D operator vector
vec = solver.get_operator_vector("operator:TRANSFORM")  # → list[float]×24

# Best edge from concept (highest affordance)
edge = solver.best_edge_from("Adrian_Lipa")
# → {concept_id, operator_hook, teleusing_affordance, ...} or None

# Trace a path
trace = solver.trace(["card_A", "card_B", "card_C"])
# trace.steps[0].operator_hook, trace.total_path_integral, ...
```

## Orbit dimensions (11)

```python
ORBIT_DIMS = ["mass", "sin", "cos", "align", "tension", "j_bus",
              "visc", "afford", "word_int", "file_int", "tele_ctrl"]
```

## Data flow

```
load_teleusing() → TeleusingData
    ↓
TeleusingSolver(data)
    ↓ trace(card_ids) → TeleusingTrace
    ↓ get_phase() / get_orbit() / get_operator_vector()
    ↓ best_edge_from() → edge dict
```

## Plik

`src/ciel_geometry/phasenav/solver.py` (110 lines)
