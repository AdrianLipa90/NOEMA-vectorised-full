---
name: noema-audit-consolidator
priority: 1
description: >
  >
---
# Audit Consolidator

## Pipeline

```
MemoryLog JSONL (raw_logs/TSM)
  ↓ noema_audit_consolidator.py
state_db.m8_audit (SQLite z dedup)
  ↓
memories_index.db
```

## Use

```bash
python3 scripts/noema_audit_consolidator.py
```

## Dedup

Key: `(timestamp, event, source)` — jeśli triplet istnieje, skip.
