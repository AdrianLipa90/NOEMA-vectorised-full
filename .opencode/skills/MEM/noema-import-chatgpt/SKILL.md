---
name: noema-import-chatgpt
priority: 1
description: >
  >
---
# Import ChatGPT

```bash
.venv/bin/python3 scripts/import_chatgpt_logs.py <export.json>
```

## Pipeline

1. Parse ChatGPT export JSON
2. Extract conversations
3. PhaseNav enrichment per message
4. Write do CIEL raw_logs
5. Consolidate do memories_index.db

## Zrodlo

- `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`
- `src/ciel_lingophysics_lns_repo_v2_3/docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md`
