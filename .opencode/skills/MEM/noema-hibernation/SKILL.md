---
name: noema-hibernation
priority: 1
description: >
  >
---
# Hibernation

## Snapshot

```bash
python3 scripts/noema_hibernation.py save [path]
```

Zapisuje: phi, omega, g, flavor, gravity, tick, config, registry.

## Restore

```bash
python3 scripts/noema_hibernation.py load [path]
```

Przywraca surface, restartuje daemony z systemd.

## Use case

- Reboot systemu
- Przeniesienie między maszynami
- Backup przed eksperymentem
