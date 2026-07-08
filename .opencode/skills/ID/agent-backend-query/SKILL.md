---
name: agent-backend-query
priority: 1
description: >
  >
---
# Agent Backend Query

## Endpoint

```bash
curl -X POST http://localhost:18520/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"<text>"}]}'
```

## Response

```json
{
  "choices": [{
    "message": {
      "content": "{
        \"themes\": [...],
        \"affect\": \"calm|curious|...\",
        \"anchor_terms\": [...],
        \"essence\": \"...\",
        \"hunch\": \"...\"
      }"
    }
  }]
}
```

## Pola

| Pole | Opis |
|------|------|
| themes | bigram TF-IDF, top 5 |
| affect | z leksykonu afektywnego |
| anchor_terms | proper nouns + CamelCase + UPPERCASE + quoted |
| essence | najgęstsze zdanie (TF-IDF) |
| hunch | pattern matching (systemic/structural/inventional) |

## Plik

`scripts/ciel_agent_backend.py`
