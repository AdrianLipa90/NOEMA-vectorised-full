---
name: noema-analog-phasenav
priority: 1
description: >
  >
---
# Analog PhaseNav

## Bus

```python
from ciel_geometry.analog_bus import ensure_bus, open_bus, blend_phi

bus = ensure_bus()  # /dev/shm/ciel_noema/analog/
# bus["phi_hot"], bus["phi_cold"], bus["temp"], bus["coupling"], bus["resonance"], bus["tick"]
```

## Dual node

| Node | Interval | strength | temp | Funkcja |
|------|----------|----------|------|---------|
| Hot | 1s | 0.8 | 0.9 | Eksploracja — szum + operator |
| Cold | 30s | 0.2 | 0.15 | Konsolidacja — sys_operator |

```bash
.venv/bin/python3 scripts/ciel_noema_phasenav_daemon.py --node hot
.venv/bin/python3 scripts/ciel_noema_phasenav_daemon.py --node cold
```

## Blender

```python
blended = temp · phi_hot + (1 - temp) · phi_cold
surface["phi"] = inject_strength · blended + (1 - inject_strength) · surface["phi"]
```

```bash
.venv/bin/python3 scripts/noema_analog_phase_blend.py --inject-strength 0.15
```

## Pliki

- `src/ciel_geometry/analog_bus.py`
- `scripts/ciel_noema_phasenav_daemon.py`
- `scripts/noema_analog_phase_blend.py`
