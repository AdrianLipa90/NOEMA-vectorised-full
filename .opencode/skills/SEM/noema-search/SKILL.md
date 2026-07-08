---
name: noema-search
priority: 1
description: >
  >
---
# NOEMA Search

## Pipeline

```
query
  ↓ query_cache (dedup)
PhaseNav operator match (library_index.npy)
  ↓
Web search fallback (requests)
  ↓
Surface enrichment + CIEL context
```

## CLI

```bash
python3 scripts/noema_search.py "query"
```

## Zrodlo

- `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`
- `src/ciel_lingophysics_lns_repo_v2_3/docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md`
