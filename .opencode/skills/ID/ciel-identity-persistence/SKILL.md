---
name: ciel-identity-persistence
priority: 1
description: >
  >
---
# CIEL Identity Persistence

NOEMA używa mmap zamiast HDF5. Tożsamość:
- phi[3:6] (M1, AGENT attractor)
- flavor[0] (coherence)
- gravity[1] (γ)

Trwa między restartami. Żadnego HDF5.

## Zrodlo

- `scripts/ciel_memory_consolidator.py`
- `scripts/ciel_lora_train.py`
- `scripts/ciel_noema_x25519_exchange.py`
