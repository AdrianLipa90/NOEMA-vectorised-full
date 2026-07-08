---
name: doc-memory-system
priority: 4
description: >
  >
---
# Doc: MEMORY_SYSTEM.md

**Plik**: `docs/MEMORY_SYSTEM.md` (291 linii)

Pokrywa:
- Memory hierarchy (3 tiers + background consolidation)
- Tier 1: NOEMA surface mmap + PhaseMemory + HolonomicMemory M0-M8
- Tier 2: TSM SQLite + StateDB + CIELBlochEncoder
- Tier 3: WPM HDF5 + BraidLedger JSONL
- Write/read routing logic
- ConsolidationResonator + CIELMemoryConsolidator

**Przeczytaj gdy**: potrzebujesz memory architecture reference.
