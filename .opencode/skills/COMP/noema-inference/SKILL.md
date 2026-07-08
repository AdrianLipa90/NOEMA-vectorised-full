---
name: noema-inference
priority: 1
description: >
  >
---
# Inference

## Warianty

| Skrypt | Backend | Surface |
|--------|---------|---------|
| `run_ciel_gguf.py` | GGUF model | NOEMA mmap |
| `run_ciel_inference_surface.py` | Surface + CIEL | NOEMA |
| `run_ciel_local_surface.py` | Local symulacja | None |

## Use

```bash
.venv/bin/python3 scripts/run_ciel_inference_surface.py
```
