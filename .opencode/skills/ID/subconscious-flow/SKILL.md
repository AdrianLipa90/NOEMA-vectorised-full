---
name: subconscious-flow
priority: 1
description: >
  >
---
# Subconscious Flow

## Daemon

`scripts/ciel_noema_subconscious_daemon.py` — działa w tle, co N sekund:
1. Czyta memory state z TieredMemoryOrchestrator
2. Generuje thought fragment (context + phase vector)
3. Seeduje na surface jako perturbację
4. Zapisuje do TSM

## Moduły

`src/ciel_geometry/subconscious.py` — core subconscious logic.
`src/ciel_sot_agent/subconsciousness.py` — agent-level subconscious.

## Różnica

| Warstwa | Moduł | Funkcja |
|---------|-------|---------|
| Geometry | `subconscious.py` | phase seed + memory read |
| Agent | `subconsciousness.py` | thought fragment management + sync |
