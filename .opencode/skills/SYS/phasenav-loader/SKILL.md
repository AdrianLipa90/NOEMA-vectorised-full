---
name: phasenav-loader
priority: 4
description: >
  >
---
# PhaseNav Loader

## TeleusingData

| Field | Key from | Źródło |
|-------|----------|--------|
| `name_mass` | `normalized` | `*NAME_MASS.noema.jsonl` |
| `concept_phases` | `concept_card_id` | `*CONCEPT_PHASES.noema.jsonl` |
| `operator_vectors` | `card_id` | `*OPERATOR_VECTORS.noema.jsonl` |
| `edges` | — | `*HOLONOMIC_EDGES.noema.jsonl` |
| `orbits` | `card_id` | `*ORBIT_VECTORS.noema.jsonl` |
| `edges_by_concept` | `concept_id` | Built from edges |

## load_teleusing()

```python
from ciel_geometry.phasenav import load_teleusing
data = load_teleusing(base_path=None)  # default: /dev/shm/ciel_noema/teleusing/
```

## 5 JSONL files

| Plik | Wymagany? | Klucz |
|------|-----------|-------|
| `CIELINGO_TELEUSING_NAME_MASS.noema.jsonl` | Yes | `"normalized"` |
| `CIELINGO_TELEUSING_CONCEPT_PHASES.noema.jsonl` | Yes | `"concept_card_id"` |
| `CIELINGO_TELEUSING_OPERATOR_VECTORS.noema.jsonl` | No (auto-generate) | `"card_id"` |
| `CIELINGO_TELEUSING_HOLONOMIC_EDGES.noema.jsonl` | Yes | — |
| `CIELINGO_TELEUSING_ORBIT_VECTORS.noema.jsonl` | Yes | `"card_id"` |

**Operator vectors fallback**: jeśli plik nie istnieje → `operator_algebra.generate_operator_map()` → deterministyczne 35 wektorów.

## JSONL format

1 JSON object per line. Brak przecinków między liniami.

## Plik

`src/ciel_geometry/phasenav/loader.py` (81 lines)
