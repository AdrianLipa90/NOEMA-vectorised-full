---
name: noema-watchdog
priority: 1
description: >
  >
---
# Watchdog

## Skanowanie

```python
from ciel_geometry.daemon_registry import Registry
reg = Registry()
daemons = reg.scan(stale_seconds=6.0)
# daemons with last_heartbeat > 6s ago → stale → restart
```

## Restart

```bash
systemctl --user restart noema-<name>
```

## Plik

`scripts/noema_watchdog.py`

## Zrodlo

- `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`
- `src/ciel_lingophysics_lns_repo_v2_3/docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md`
