---
name: ciel-monitoring
priority: 2
description: >
  >
---
# Monitoring

| Skrypt | Co monitoruje | Interwał |
|--------|--------------|----------|
| `ciel_monitor.py` | Engine cycle, CIEL state | 1s |
| `ciel_hw_monitor.py` | CPU/RAM/GPU | 5s |
| `ciel_orbital_monitor.py` | Orbital entities, edges | 1s |
| `ciel_system_report.py` | Full system report | on-demand |

## Zrodlo

- `scripts/ciel_memory_consolidator.py`
- `scripts/ciel_lora_train.py`
- `scripts/ciel_noema_x25519_exchange.py`
