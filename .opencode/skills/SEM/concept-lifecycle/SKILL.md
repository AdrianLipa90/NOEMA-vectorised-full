---
name: concept-lifecycle
priority: 1
description: >
  >
---
# Concept Lifecycle

## Fazy

```
Seed
  ↓  operator match + phase encoding
Explore
  ↓  hot PhaseNav (temp=0.9) szuka rezonansów
Consolidate
  ↓  cold PhaseNav (temp=0.15) utrwala + TSM write
Archive
  ↓  library_index.npy + knowledge_graph.json + HDF5
```

## Narzędzia

| Faza | Skrypt | Output |
|------|--------|--------|
| Seed | `noema_learn_file.py` | library_index.npy |
| Explore | hot PhaseNav daemon | analog bus phi_hot |
| Consolidate | cold PhaseNav daemon | analog bus phi_cold |
| Archive | `noema_library_indexer.py` | library_meta.npy |
| Graph | `noema_knowledge_graph.py` | 475-node graph |

## Concept w pamięci

```sql
-- TSM: structured concept
INSERT INTO concept (name, signature, phase_vector, timestamp)
VALUES (:name, :signature, :phase_vector, :timestamp)
```
