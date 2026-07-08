---
name: noema-holonomic-audit
priority: 1
description: >
  >
---
# Holonomic Audit

## Sektory audytu

| Sektor | Źródło | Orbital |
|--------|--------|---------|
| CPU | /proc/stat | M4 (perception) |
| Memory | /proc/meminfo | M4 |
| Processes | /proc/*/status | M3 (cognition) |
| Systemd | systemctl list-units | M7 (braid) |
| NOEMA | all daemons | M0-M8 |

## CLI

```bash
python3 scripts/noema_holonomic_audit.py
```

Generuje: raport tekstowy + JSON + wpis do DB.
