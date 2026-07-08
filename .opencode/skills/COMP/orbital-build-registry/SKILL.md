---
name: orbital-build-registry
priority: 4
description: >
  >
---
# Orbital Build Registry

## Build scripts

| Skrypt | Buduje |
|--------|--------|
| `build_definition_db_library.py` | Definition DB z ontologii |
| `build_file_wij.py` | File-level coupling matrix W_ij |
| `build_memory_portal.py` | Memory portal edges |
| `build_nonlocal_cards_registry.py` | Nonlocal card definitions |
| `build_nonlocal_definition_edges.py` | Nonlocal edges |
| `build_orbital_definition_registry.py` | Orbital definition registry |
| `build_subsystem_sync_registry.py` | Subsystem sync registry |
| `build_word_cards_registry.py` | Word cards (CIEL vocab) |

## Use

```bash
.venv/bin/python3 scripts/build_definition_db_library.py
# ...
```
