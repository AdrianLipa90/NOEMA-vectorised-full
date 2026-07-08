---
name: noema-unified-config
priority: 1
description: >
  >
---
# Unified Config

## Plik

`noema_config.json` (w katalogu projektu)

```json
{
  "surface_root": "/dev/shm/ciel_noema",
  "memory_root": "~/Pulpit/CIEL_memories",
  "kuramoto": {
    "interval": 0.2,
    "dt": 0.05,
    "continuous": true,
    "cont_every": 10
  },
  "cielingo_sync": {
    "interval": 60,
    "blend_min": 0.02,
    "blend_max": 0.12,
    "tau_min": 0.01,
    "tau_max": 1.0,
    "tau_default": 0.353
  },
  "sonic": {
    "interval": 2.0
  },
  "consolidator": {
    "interval": 60,
    "batch": 5,
    "agent_port": 18520
  }
}
```

## Loader

```python
from ciel_geometry.noema_config import config
config.kuramoto.interval    # 0.2
config.cielingo_sync.interval  # 60
config.sonic.interval       # 2.0
```

**Env override**: `export NOEMA_CONFIG=/path/to/config.json`

## Użycie w daemonach

```python
interval = config.get("kuramoto", "interval", 0.2)
```

## Pliki

- `noema_config.json` — w repo
- `src/ciel_geometry/noema_config.py` — loader
- `.env.example` — template dla env vars
