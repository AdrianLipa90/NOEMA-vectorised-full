---
name: noema-codegen
priority: 1
description: >
  >
---
# Codegen

## Pipeline

```
user prompt
  ↓ query_cache → PhaseNav enrichment noema_query_cache.py
operator / concept match
  ↓
noema_codegen.py — generuje kod z PhaseNav operatora
  ↓
Surface metadata + CIEL state as context
```

## Use

```bash
alias noema_codegen='python3 /home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/scripts/noema_codegen.py'
```
