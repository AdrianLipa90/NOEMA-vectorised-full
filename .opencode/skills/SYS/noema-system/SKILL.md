---
name: noema-system
priority: 1
description: >
  >
---
# NOEMA System Architecture

## Warstwy

| Warstwa | Opis | Komponenty |
|---------|------|------------|
| L0: Surface | 24 oscillator MMAP | `/dev/shm/ciel_noema/{phi,omega,g,flavor,tick,gravity}` |
| L1: Kuramoto | 10Hz phase evolution | `ciel_noema_kuramoto_daemon.py` |
| L2: Bridge | real↔imaginal sync | `ciel_noema_resonance_bridge.py` |
| L3: PhaseNav | concept seeding | `ciel_noema_phasenav_daemon.py` (hot+cold) |
| L4: CIELingo | semantic closure | `ciel_noema_cielingo_sync.py` |
| L5: Agent | zero-dep HTTP | `ciel_agent_backend.py` (port 18520) |

## Daemons (10)

| Daemon | Interval | Memory |
|--------|----------|--------|
| kuramoto | 10Hz | ~60MB |
| resonance-bridge | 1s | ~22MB |
| agent-backend | on-demand | ~35MB |
| linux-sensor | 1Hz | ~15MB |
| neutrino | 1s | ~18MB |
| cielingo-sync | 60s | ~157MB |
| phasenav-hot | 1s | ~24MB |
| phasenav-cold | 30s | ~18MB |
| analog-blend | 1Hz | ~19MB |
| archiver | 50 ticks | ~20MB |
| consolidator | 60s | ~18MB |

## Pliki surface

- `/dev/shm/ciel_noema/{phi,omega,g,flavor,tick,gravity,psi_geom,R_geom,Z_geom,holonomy}`
- `/dev/shm/ciel_noema/analog/{phi_hot,phi_cold,temp,coupling,resonance,tick}`
- `/dev/shm/ciel_noema/daemon_registry`
- `/dev/shm/ciel_noema_imaginal/{phi,g,omega,flavor,tick}`
