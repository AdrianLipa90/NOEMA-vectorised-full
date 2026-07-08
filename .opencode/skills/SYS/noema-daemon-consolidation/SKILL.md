---
name: noema-daemon-consolidation
priority: 1
description: >
  >
---
# noema-daemon-consolidation

## Merges

| Przed | Po | Zapisane |
|-------|----|----------|
| resonance-bridge (22.5MB) + agent-lock (29MB) | resonance-bridge (22.5MB) z DB logging | 29MB + 1 process |
| resonance-bridge + dual-sync (23MB) | + _copy_g_and_omega() inline | 23MB + 1 process |
| nonlocal-proxy 1s fixed | adaptive stretch 1s→5s idle | CPU |

## Consolidated resonance bridge

```
Resonance Bridge
├── dual_surface_step()         — PLL sync real↔imaginal (1s)
├── _copy_g_and_omega()         — real g/omega → imaginal (1s)
├── _log_agent_state()          — SQLite agent_snapshots/operator_log (5s)
├── _nonlocal_broadcast()       — channel 1 broadcast (30s)
└── resonance_snapshot() report — console log (5s)
```

## Single source of truth

**Kuramoto daemon** jest JEDYNYM writerm agent attractor na real surface.
Resonance bridge tylko czyta i loguje. Żadnego race condition.

## Pliki

- `scripts/ciel_noema_resonance_bridge.py`
- `scripts/ciel_noema_nonlocal_proxy.py` (+adaptive idle stretch)
