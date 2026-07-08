---
name: noema-agent-backend
priority: 1
description: >
  >
---
# Agent Backend

## API

```
GET /agent/health
GET /agent/reflect?query=<text>
```

## Extractors

| Pole | Metoda |
|------|--------|
| themes | bigram TF-IDF |
| affect | lexicon-based |
| anchor_terms | proper + CamelCase + UPPERCASE + quoted |
| essence | najgęstsze zdanie (TF-IDF density) |
| hunch | pattern matching (regrets, fears, if...then) |

## Performance

- 0.0-0.1s/request
- Zero dependencies poza stdlib
- No GGUF, no llama.cpp, no transformers

## Systemd

`noema-agent-backend.service`

## Plik

`scripts/ciel_agent_backend.py`
