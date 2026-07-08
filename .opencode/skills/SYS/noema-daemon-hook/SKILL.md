---
name: noema-daemon-hook
priority: 1
description: >
  >
---
# noema_daemon — Unified Daemon

## Pętla główna

```
while True:
    read_surface()
    evolve_surface()          # Kuramoto + harmonics + AGENT attractor
    linux_sensor.snapshot()   # system metrics → flavor/phi
    analog_blend()            # hot+cold PhaseNav blend
    dual_surface_step()       # PLL sync z imaginal
    write_surface()
    registry.heartbeat()
    sleep(interval)
```

## Zastępuje

- `ciel_noema_kuramoto_daemon.py`
- `ciel_noema_linux_sensor_daemon.py`
- `noema_agent_lock.py`
- `noema_analog_phase_blend.py`
- `noema_dual_sync.py`
