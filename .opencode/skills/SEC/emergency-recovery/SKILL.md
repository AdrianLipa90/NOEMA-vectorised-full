---
name: emergency-recovery
priority: 1
description: >
  >
---
# Emergency Recovery

## Sytuacja 1: mmap corrupted

```bash
systemctl --user stop noema-kuramoto.service
rm -f /dev/shm/ciel_noema/surface
systemctl --user start noema-kuramoto.service
```

Automatyczna reinicjalizacja przez `ensure_surface()`.

## Sytuacja 2: Daemon hang

```bash
systemctl --user restart noema-<name>.service
# lub --kill-when-stuck
```

Watchdog restartuje automatycznie po 6s bez heartbeat.

## Sytuacja 3: Wszystkie daemony martwe

```bash
systemctl --user restart noema.target
# lub:
systemctl --user start 'noema-*'
```

## Sytuacja 4: System reboot

Hibernate przed rebootem, restore po:

```bash
python3 scripts/noema_hibernation.py save /tmp/noema_snapshot.npz
reboot
python3 scripts/noema_hibernation.py load /tmp/noema_snapshot.npz
```

## Sytuacja 5: CIEL closure > 0.5

- Znaleźć źródło (PMNS blend za wysoki? τ za niski?)
- Zmniejszyć blend ratio w CIELingo sync
- Poczekać na naturalny decay cp

## Sytuacja 6: AGENT attractor stracił lock

- Sprawdzić omega[3] (M1). Powinno być < 5.
- Jeśli CPU noise > 10: restart linux-sensor
- Ręczne seedowanie: `apply_agent_attractor(surface, strength=0.5)`
