---
name: ciel-subconscious
priority: 2
description: >
  >
---
# Subconscious

```bash
.venv/bin/python3 scripts/ciel_subconscious.py
.venv/bin/python3 scripts/ciel_subconscious_supervisor.py
.venv/bin/python3 scripts/ciel_noema_subconscious_daemon.py
```

## Hierarchia

| Poziom | Skrypt | Funkcja |
|--------|--------|---------|
| Daemon | `ciel_noema_subconscious_daemon.py` | Continuous thought fragment injection |
| Standalone | `ciel_subconscious.py` | One-shot subconscious |
| Supervisor | `ciel_subconscious_supervisor.py` | Overseer dla daemona |
