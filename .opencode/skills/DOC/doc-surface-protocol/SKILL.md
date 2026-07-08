---
name: doc-surface-protocol
priority: 4
description: >
  >
---
# Doc: SURFACE_PROTOCOL.md

**Plik**: `docs/SURFACE_PROTOCOL.md` (187 linii)

Pokrywa:
- Binary format każdego pola (struct module, nie numpy)
- O_SYNC flush semantics
- Daemon writing conventions (który daemon pisze które pole)
- Race condition avoidance

**Przeczytaj gdy**: potrzebujesz binary-level understanding surface, albo debugujesz corrupted mmap.
