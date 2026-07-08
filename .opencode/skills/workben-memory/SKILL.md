---
name: workben-memory
priority: 1
description: >
  Memory — tiered memory, konsolidacja, handoff, hibernacja, import, index, recall
---
# Workben MEMORY

Memory — tiered memory, konsolidacja, handoff, hibernacja, import, index, recall

## Źródła

Ten workben konsoliduje 16 źródłowych skilli:

- **CIEL Memory System** (`MEM/ciel-memory-system`)
- **CIEL Memory Handoff** (`MEM/ciel-memory-handoff`)
- **Memory Tools** (`MEM/ciel-memory-tools`)
- **Memory Consolidation** (`MEM/memory-consolidation`)
- **Tiered Memory Orchestrator** (`MEM/tiered-memory-api`)
- **Hibernation** (`MEM/noema-hibernation`)
- **Indexer** (`MEM/noema-indexer`)
- **Learn File** (`MEM/noema-learn-file`)
- **Learned** (`MEM/noema-learned`)
- **Noemized Recall** (`MEM/noema-noemized-recall`)
- **Phase Archiver** (`MEM/noema-phase-archiver`)
- **Query Cache** (`MEM/noema-query-cache`)
- **Loader & Edges** (`MEM/loader-edges`)
- **Memory Lane Monitor (NOEMA)** (`MEM/memory-lane-monitor`)
- **Memory Lane Seed** (`MEM/memory-lane-seed`)
- **Import ChatGPT** (`MEM/noema-import-chatgpt`)

## Kluczowe wzorce

### CIEL Memory System

- | System | Storage | Funkcja |
- |--------|---------|---------|
- | TSM | SQLite | Temporal-Structured Memory z holonomy columns |

### CIEL Memory Handoff

- `scripts/ciel_session_hook.py`

### Memory Tools

- | Tool | Function |
- |------|----------|
- | `ciel_memory_dump.py` | Dump full memory state |

### Memory Consolidation

- - `scripts/ciel_memory_consolidator.py` — główny konsolidator
- - `scripts/consolidate_raw_logs_to_tsm.py` — surowy bridge do TSM

### Tiered Memory Orchestrator

- | Tier | Enum | Storage | Trwałość |
- |------|------|---------|----------|
- | Tier 1 | `Tier.FAST` | NOEMA surface mmap + PhaseMemory mmap + M0-M8 | Volatile |

### Hibernation

- Zapisuje: phi, omega, g, flavor, gravity, tick, config, registry.
- Przywraca surface, restartuje daemony z systemd.
- - Reboot systemu

### Indexer

- - `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- - `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`
- - `src/ciel_lingophysics_lns_repo_v2_3/docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md`

### Learn File

- - PhaseNav library index update
- - Knowledge graph edge
- - Surface state enriched

### Learned

- `src/noema_learned/`
- Dynamicznie generowane moduły podczas działania NOEMA:
- - Wyuczone operatory PhaseNav

### Noemized Recall

- - `scripts/noema_learn_file.py`
- - `src/ciel_geometry/phasenav/` — PhaseNav modules
- - User's TRANSFORMEM (`transformer_features.py`)

### Phase Archiver

- Co 50 ticków zapisuje:
- - phi, omega, g, flavor, gravity, tick
- - timestamp, R_coherence, γ

### Query Cache

- `scripts/noema_query_cache.py`
- - `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- - `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`

### Loader & Edges

- Geodesic arcs między entity na Poincaré disk:
- - `src/ciel_geometry/loader.py`
- - `src/ciel_geometry/edges.py`

### Memory Lane Monitor (NOEMA)

- | Tier | Storage | Lokalizacja |
- |------|---------|-------------|
- | T1 Fast/Volatile | mmap | surface + PhaseMemory mmap + M0-M8 holonomic |

### Memory Lane Seed

- 1. CIELINGO cards (5,590 records)
- 2. TSM memory_ledger.db
- 3. SHA resonator state

### Import ChatGPT

- 1. Parse ChatGPT export JSON
- 2. Extract conversations
- 3. PhaseNav enrichment per message

## Jak używać

```python
skill("workben-memory")
```

Ładuje wiedzę ze wszystkich 16 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
