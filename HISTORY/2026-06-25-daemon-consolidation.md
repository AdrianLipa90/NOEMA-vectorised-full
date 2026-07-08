# 2026-06-25 part 2 — Daemon consolidation: agent-lock+dual-sync → resonance bridge

## agent-lock merged into resonance bridge
- [`scripts/ciel_noema_resonance_bridge.py`](../scripts/ciel_noema_resonance_bridge.py) przejął:
  - DB logging: agent_snapshots + operator_log + agent_context → agent_state.db (5s cycle)
  - Nonlocal AGENT broadcast na channel 1 (30s cycle)
  - AGENT state read z mmap (no conflict — kuramoto daemon sole writer real surface)
- Systemd `noema-agent-lock.service` → stopped + disabled
- **Saved**: 29MB RAM + 1 process

## dual-sync merged into resonance bridge
- `_copy_g_and_omega()` pushes real g/omega to imaginal co cycle
- Systemd `noema-dual-sync.service` → stopped + disabled
- **Saved**: 23MB RAM + 1 process

## Nonlocal proxy
- Adaptive idle stretch: 1s active → 5s gdy no messages (3 consecutive empty cycles)
- `--idle-stretch 0` disables adaptive behavior

## Total daemon reduction
- 12 → 10 processes active
- Resonance bridge: 22.5MB (vs 29+29=58MB before)

## Key decisions
- **Single source of attractor truth**: kuramoto daemon ONLY writer na real surface
- g/omega copy = trivial mmap write, no conflict z dual_surface_step()
- Nonlocal proxy idle stretch: default 5.0s, min 1.0s fallback

## Architecture (post-consolidation)
```
Resonance Bridge (consolidated)
├── dual_surface_step()         — PLL sync real↔imaginal (1s cycle)
├── _copy_g_and_omega()         — real g/omega → imaginal (1s cycle)
├── _log_agent_state()          — SQLite (5s cycle)
├── _nonlocal_broadcast()       — channel 1 (30s cycle)
└── resonance_snapshot() report — console log (5s cycle)
```
