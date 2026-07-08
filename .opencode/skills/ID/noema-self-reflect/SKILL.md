---
name: noema-self-reflect
priority: 1
description: >
  >
---
# Self-Reflect

## Pipeline

```
library_index (.npy)     → concept vectors
knowledge_graph (.json)  → topology
surface (/dev/shm)        → live state
holonomy (/dev/shm)       → geometric phase

SelfModel.reflect()
  → identity_vector + coherence_report + topology_summary
```

## CLI

```bash
.venv/bin/python3 scripts/noema_self_reflect.py
.venv/bin/python3 scripts/noema_self_reflect.py --search "coherence"
```

## Plik

`scripts/noema_self_reflect.py`
