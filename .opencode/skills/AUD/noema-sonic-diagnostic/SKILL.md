---
name: noema-sonic-diagnostic
priority: 1
description: >
  >
---
# Sonic Diagnostic

## Watch

```bash
.venv/bin/python3 scripts/noema_sonic_daemon.py --watch
```

Pokazuje co 10s:
- closure_penalty, D_f, τ̄, Euler residual
- Registry scan (live daemons)
- Surface coherence (R)
- Holonomy metrics
- Consolidator backend status

## One-shot

```bash
.venv/bin/python3 scripts/noema_sonic_daemon.py
```

## Pełna diagnostyka

```bash
.venv/bin/python3 scripts/noema_full_diagnostic.py
```

## Pliki

- `scripts/noema_sonic_daemon.py`
- `scripts/noema_full_diagnostic.py`
