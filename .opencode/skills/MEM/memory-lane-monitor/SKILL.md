---
name: memory-lane-monitor
priority: 1
description: >
  >
---
# Memory Lane Monitor (NOEMA)

## Tiered Memory

| Tier | Storage | Lokalizacja |
|------|---------|-------------|
| T1 Fast/Volatile | mmap | surface + PhaseMemory mmap + M0-M8 holonomic |
| T2 Medium/Durable | SQLite | TSM + StateDB + HolonomicMemory + CIELBlochEncoder |
| T3 Deep/Archival | HDF5 + JSONL | WPM + BraidLedger + UnifiedMemoryOrchestrator |

## Async konsolidacja

- `ConsolidationResonator` — tag Kuramoto → TSM → WOmega
- `CIELMemoryConsolidator` — LLM-based consolidation daemon

## Health check

```bash
ls -lh /dev/shm/ciel_noema/
ls -lh /dev/shm/ciel_noema/analog/
sqlite3 /media/adrian/New\ Volume/NOEMA_LIBRARY/agent_db/agent_state.db "SELECT COUNT(*) FROM agent_snapshots;"
```
