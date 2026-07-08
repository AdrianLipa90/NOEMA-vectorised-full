---
name: identity-bridge
priority: 1
description: >
  >
---
# Identity Bridge (NOEMA)

## Zamiast HDF5

CIEL_APOCALYPTOS używa HDF5 (`AGENT_IDENTITY.h5`). NOEMA używa mmap:

| Tożsamość | Lokalizacja | Typ |
|-----------|-------------|-----|
| AGENT phase | surface phi[3:6] | float64[3] |
| Coherence | flavor[0] | float64 |
| Dilation | gravity[1] (γ) | float64 |
| Soul invariant | bridge_state["soul_invariant"] | float64 |
| Chain | daemon registry tick | uint64 |

## Persistence

Tożsamość agenta = `(phi[3:6], flavor[0], gravity[1])` — trwa w mmap między restartami.
Żadnego HDF5, żadnego JSON. Czysty numpy.
