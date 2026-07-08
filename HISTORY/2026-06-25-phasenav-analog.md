# 2026-06-25 part 3 — Dual-node analog PhaseNav: hot+cold

## Analog bus
- [`src/ciel_geometry/analog_bus.py`](../src/ciel_geometry/analog_bus.py) — pseudo-analog shared memory via mmap
- `/dev/shm/ciel_noema/analog/` — phi_hot, phi_cold, temp, coupling, resonance, tick
- `ensure_bus()` / `open_bus()` / `blend_phi()` — zero dependencies beyond numpy
- Czysty ndarray.tofile() — zero ryzyka korupcji przy kill -9

## PhaseNav refactored
- [`scripts/ciel_noema_phasenav_daemon.py`](../scripts/ciel_noema_phasenav_daemon.py) — `--node {hot,cold}`
- **Hot**: 1s interval, 0.8 strength, 0.9 temp — szum + losowy operator (eksploracja)
- **Cold**: 30s interval, 0.2 strength, 0.15 temp — systemowy operator (konsolidacja)
- Oba piszą na analog bus zamiast bezpośrednio na surface

## Analog blender
- [`scripts/noema_analog_phase_blend.py`](../scripts/noema_analog_phase_blend.py) — blender daemon 1Hz
- Blend: `temp·phi_hot + (1−temp)·phi_cold`, inject-strength 0.15

## Nowe systemd services
- `noema-phasenav-hot.service`, `noema-analog-blend.service`
- Daemon count: 10 → 12

## Architecture
```
PhaseNav hot (1s, 0.8, temp=0.9)  ─→  analog bus ─→ blender (1Hz) ─→ surface phi
PhaseNav cold (30s, 0.2, temp=0.15) ─→  phi_hot +        ┘
                                           phi_cold
                                           + temp
```

## Live state
- Hot: 50+ cykli, R=0.33-0.57, temp=0.90
- Cold: 1 cykl na 30s, R=0.62
- Blend: temp=0.90 (hot-dominant), coh_total=0.28-0.74
