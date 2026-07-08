# Merge: CIEL memory

Wszystkie skille z grupy ciel-memory

---

## Importy

Ten skill agreguje poniższe skille źródłowe:

- `ciel-memory-handoff` → [`.opencode/skills/ciel-memory-handoff/SKILL.md`](.opencode/skills/ciel-memory-handoff/SKILL.md) (44 linii)
- `ciel-memory-system` → [`.opencode/skills/ciel-memory-system/SKILL.md`](.opencode/skills/ciel-memory-system/SKILL.md) (27 linii)
- `ciel-memory-tools` → [`.opencode/skills/ciel-memory-tools/SKILL.md`](.opencode/skills/ciel-memory-tools/SKILL.md) (19 linii)

---

## 1. ciel-memory-handoff

*Źródło: [`.opencode/skills/ciel-memory-handoff/SKILL.md`](.opencode/skills/ciel-memory-handoff/SKILL.md)*

---
name: ciel-memory-handoff
priority: 1
description: >
  >
---

## Struktura pamięci

```
~/Pulpit/CIEL_memories/
├── raw_logs/           ← każdy prompt/response
├── memories_index.db   ← skonsolidowane
├── handoff.md          ← ostatnie wpisy sesji
├── routines.md         ← priorytety i procedury
├── secrets/            ← API keys (gitignored)
├── genesis.md          ← Akt Fundacyjny
├── mindflow.yaml       ← przepływ myśli
├── logs/               ← konsolidator output
└── experiments/        ← eksperymenty
```

## Konsolidacja

```
raw_logs (JSONL)
  ↓ consolidate_raw_logs_to_tsm.py
TSM SQLite (memory_ledger.db)
  ↓ AgentMemoryConsolidator
memories_index.db
```

## Session hook

```bash
.venv/bin/python3 scripts/ciel_session_hook.py start   # start sesji
.venv/bin/python3 scripts/ciel_session_hook.py end     # konsolidacja
```

## Plik

`scripts/ciel_session_hook.py`


---

## 2. ciel-memory-system

*Źródło: [`.opencode/skills/ciel-memory-system/SKILL.md`](.opencode/skills/ciel-memory-system/SKILL.md)*

---
name: ciel-memory-system
priority: 1
description: >
  >
---

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


---

## 3. ciel-memory-tools

*Źródło: [`.opencode/skills/ciel-memory-tools/SKILL.md`](.opencode/skills/ciel-memory-tools/SKILL.md)*

---
name: ciel-memory-tools
priority: 1
description: >
  >
---

| Tool | Function |
|------|----------|
| `ciel_memory_dump.py` | Dump full memory state |
| `ciel_memory_stop.py` | Graceful memory stop |
| `ciel_memory_consolidator.py` | Agent-level consolidation |
| `consolidate_raw_logs_to_tsm.py` | raw_logs → TSM SQLite |
| `migrate_memory_to_protected.sh` | Move sensitive data |
| `protect_memory.sh` | Chmod/chown protection |
| `ingest_memory_files.py` | Batch file ingestion |
| `inject_memory_clusters.py` | Cluster injection |


---
