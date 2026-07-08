---
name: noema-secret-loader
priority: 1
description: >
  >
---
# Secret Loader

## Struktura

```
~/Pulpit/CIEL_memories/secrets/
├── github_token
├── openai_key
└── ...
```

## Usage

```python
from cielyngo.secret_loader import load_secret
token = load_secret("github_token")
```

## Zasada

- Sekrety NIGDY w repo lub commit
- Tylko w CIEL_memories/secrets/
- gitignored
