---
name: memory-consolidation
priority: 1
description: >
  >
---
# Memory Consolidation

## Pipeline

```
scan_and_register_files()
  ↓  skanuje raw_logs + SCAN_SOURCES
get_pending_files(limit=5)
  ↓  priority: review → pending, small first
process_file(file_row, cycle)
  ↓  read → LLM query → parse → score → verify → write DB + mirror
```

## Konstanty

```python
MEMORIES_DIR = ~/Pulpit/CIEL_memories
DB_PATH = MEMORIES_DIR / "local_test" / "consolidator.db"
RECONSOLIDATION_THRESHOLD = 0.72   # score below = requeue
MAX_RECONSOLIDATION_ATTEMPTS = 1
DEFAULT_INTERVAL = 300              # 5 min
MAX_TOKENS = 128
LLAMA_SERVER_URL = "http://127.0.0.1:18520"
```

## Backend resolution

```python
_shared_server_assessment()
  ↓ health OK?
  YES → _query_via_server()     # llama-server :18520
  NO  → _query_local_llm()      # llama_cpp.Llama direct
         ↓ both None?
         → _ask_api_fallback_permission()
           → _query_anthropic_api()  # claude-haiku
```

## Quality score

```python
# score = themes + affect + essence + hunch completeness
if score < 0.72:   # reconsolidate (1 retry, /no_think fix)
if retry_score >= score: replace with retry
if still < 0.72:   review_status = 'review'  # manual
if essence has no overlap with source text:
    clamp to min(quality, 0.55), add essence_mismatch
```

## run_cycle()

```python
def run_cycle(cycle, batch=5) -> int:
    # audit → scan → get pending → process
```

## run_daemon()

```python
def run_daemon(interval=300):
    while True:
        run_cycle(cycle)
        sleep(interval)
```

## Pliki

- `scripts/ciel_memory_consolidator.py` — główny konsolidator
- `scripts/consolidate_raw_logs_to_tsm.py` — surowy bridge do TSM
