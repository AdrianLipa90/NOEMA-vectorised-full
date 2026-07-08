---
name: ciel-memory-system
priority: 1
description: >
  >
---
# CIEL Memory System

## Componenty

| System | Storage | Funkcja |
|--------|---------|---------|
| TSM | SQLite | Temporal-Structured Memory z holonomy columns |
| WPM | HDF5 | Wave-Packet Memory — snapshots z atrybutami |
| BRAID | JSONL | Braid-side traces dla synchronizacji |

## Lokacja

`src/CIEL_MEMORY_SYSTEM/TSM/`, `src/CIEL_MEMORY_SYSTEM/WPM/`, `src/CIEL_MEMORY_SYSTEM/BRAID/`

## Użycie

```python
from CIEL_MEMORY_SYSTEM.TSM import TSM
tsm = TSM("/path/to/memory_ledger.db")
```
