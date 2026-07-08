---
name: ciel-memory-handoff
priority: 1
description: >
  >
---
# CIEL Memory Handoff

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
