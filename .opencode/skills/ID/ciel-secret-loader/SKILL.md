---
name: ciel-secret-loader
priority: 1
description: >
  >
---
# Secret Loader

```python
from cielyngo.secret_loader import load_secret
token = load_secret("github_token")
```

## Reguły

- `/home/adrian/Pulpit/CIEL_memories/secrets/`
- Każdy sekret w osobnym pliku (jedna linia)
- `.gitignore` excludes secrets/
- Nigdy w commit lub log

## Fallback

Jeśli plik nie istnieje → `None`. Żadnych wyjątków.
