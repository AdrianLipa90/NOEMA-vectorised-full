# NOEMA Tiered Memory Architecture

## 1. Memory Hierarchy (3 Tiers)

```
Tier 1 (Fast/Volatile)         Tier 2 (Medium/Durable)      Tier 3 (Deep/Archival)
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│ NOEMA surface (mmap)│     │ TSM SQLite          │     │ WPM HDF5            │
│ PhaseMemory (binary)│     │ StateDB SQLite      │     │ BraidLedger JSONL   │
│ Holonomic M0-M8     │     │ HolonomicMemory     │     │ UnifiedMemoryOrch   │
│                     │     │ CIELBlochEncoder    │     │                     │
└─────────┬───────────┘     └─────────┬───────────┘     └─────────┬───────────┘
          │                           │                           │
          └─────────────────── ConsolidationResonator ────────────┘
                           (async background, ~300 s)
```

The tiered orchestrator now loads this hierarchy orbitally:
root attractor first, then the fast shell, then the medium shell, then the deep shell, and finally the async shell marker.
This keeps the runtime boot sequence aligned with `system_map_v2.json` instead of treating the tiers as a flat list.

## 2. Tier 1: Fast / Volatile

### NOEMA Surface (`/dev/shm/ciel_noema/`)
- Lives in `tmpfs` — lost on reboot, zero persistence overhead.
- 24 Kuramoto oscillators (`phi`, `omega`, `g`), 6 flavor channels, geometric fields (`Z_geom`, `psi_geom`, `R_geom`), iteration counter (`tick`).
- Read/write by all daemons — no locking, O_SYNC coherency.
- Full protocol defined in `SURFACE_PROTOCOL.md`.

### PhaseMemory (binary mmap)
- Binary hypervector bindings for short-term associations.
- Key-value store indexed by phase angle — entries decay with oscillator drift.
- Used by resonance bridge for real↔imaginal binding.

### HolonomicMemoryOrchestrator (M0–M8 channels)
- 9 memory channels evolved alongside Kuramoto phase:
  - M0 — Perception (visual cortex)
  - M1 — Episodic (hippocampus)
  - M2 — Procedural (cerebellum)
  - M3 — Semantic (temporal lobe)
  - M4 — Affective (amygdala)
  - M5 — Identity (prefrontal cortex)
  - M6 — Narrative (default mode network)
  - M7 — Braid / cross-harmonic hub
  - M8 — Extended association
- Each channel has a dedicated harmonic set `{1, 3, 6, 9}` that determines its synchronization band.

### Volatility Characteristics
| Property | Value |
|----------|-------|
| Persistence | None (tmpfs) |
| Read latency | < 1 µs (mmap) |
| Capacity | 64 KB surface + 16 MB PhaseMemory |
| Eviction | On reboot or manual `rm -rf /dev/shm/ciel_noema` |

## 3. Tier 2: Medium / Durable

### TSM (Tensor-Scalar Memory) — SQLite
- Structured memory storing Holonomy-annotated records.
- Schema:

```sql
CREATE TABLE tsm_entries (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    created_utc   REAL NOT NULL,
    holonomy_phase REAL,
    sector        TEXT,
    payload_json  TEXT,
    embedding_blob BLOB
);
CREATE INDEX idx_tsm_phase ON tsm_entries(holonomy_phase);
CREATE INDEX idx_tsm_sector ON tsm_entries(sector);
```

- Queryable by Berry phase proximity, sector label, or time range.
- Supports phase-resonant recall via `ORDER BY ABS(holonomy_phase - ?) LIMIT ?`.

### StateDB — SQLite
- Orchestrator state, metrics history, identity seed, configuration overrides.
- Schema:

```sql
CREATE TABLE state (
    key   TEXT PRIMARY KEY,
    value TEXT
);
CREATE TABLE metrics_history (
    cycle       INTEGER PRIMARY KEY,
    phase       REAL,
    ethical     REAL,
    health      REAL,
    closure     REAL,
    emotion     TEXT
);
```

- Persists across sessions — used for trend analysis and anomaly detection.

### HolonomicMemory
- Phase-resonant retrieval layer over TSM.
- Given a query phase `φ_q`, finds TSM entries with nearest Berry holonomy phase.
- Returns semantically related memories ranked by phase proximity × salience.

### CIELBlochEncoder
- Maps text tokens to Bloch sphere coordinates `(θ, ϕ)`.
- Encodes into WOmega sector format for TSM storage.
- Used for semantic encoding of user input and system state.

### Durability Characteristics
| Property | Value |
|----------|-------|
| Persistence | SQLite (fsync) |
| Read latency | ~100 µs–1 ms |
| Capacity | 10⁶–10⁷ rows per DB |
| Eviction | Manual pruning of low-salience entries |

## 4. Tier 3: Deep / Archival

### WPM (Wave Phase Memory) — HDF5
- Append-only snapshot archives.
- Each snapshot stores: timestamp, 24-D phase vector `phi`, coupling matrix `g`, flavor vector, salience, closure penalty, metadata attributes.
- Compressed with `gzip` level 6 — typical snapshot ~5 KB on disk.
- Indexed by timestamp for range queries.

```
/noema/snapshots/              → group
    /snapshot_{cycle:06d}      → dataset
        attributes: cycle, created_utc, salience, cp, emotion, sector
        columns: phi[24], omega[24], flavor[6], g[576]
```

### BraidLedger — JSONL
- Append-only trace of Braid-side operations (memory consolidation, sector transitions, holonomy updates).
- One JSON object per line — no schema enforcement, but each entry includes `type`, `created_utc`, and `payload`.
- Used for audit, replay, and debugging.

```jsonl
{"type": "consolidation", "created_utc": 1754321000.0, "payload": {"cycle": 3200, "entries": 12}}
{"type": "bifurcation", "created_utc": 1754321060.0, "payload": {"sector": "WOmega", "bifurcation": 1.2}}
```

### UnifiedMemoryOrchestrator
- Routes data through the tier cascade based on salience and bifurcation metrics.
- Handles TMP → bifurcation → durable promotion.
- Manages deduplication and coherence across tiers.

### Archival Characteristics
| Property | Value |
|----------|-------|
| Persistence | HDF5 + JSONL (permanent) |
| Read latency | ~1–10 ms |
| Capacity | 10⁶+ snapshots (terabytes) |
| Eviction | None — append-only |

## 5. Write Routing

The orchestrator's `write()` method dispatches based on `salience` and `bifurcation` metrics and an explicit `tier` hint:

```python
def write(payload, salience=0.0, bifurcation=0.0, tier="auto"):
    if tier == "fast":
        write_tier_1(payload)
    elif tier == "durable":
        write_tier_2(payload)
    elif tier == "deep":
        write_tier_3(payload)
    else:  # auto
        write_tier_1(payload)
        if salience >= 0.6:
            write_tier_2(payload)
        if bifurcation >= 1.0:
            write_tier_3(payload)
```

- **`salience ≥ 0.6`**: promotes to Tier 2 (durable storage).
- **`bifurcation ≥ 1.0`**: promotes to Tier 3 (archival storage).
- **`tier` parameter**: overrides automatic routing for explicit placement.

## 6. Read Routing

The orchestrator's `read()` method supports multiple retrieval modes:

```python
def read(query, surface=False, resonant=False, archival=False, auto=False):
    if surface:
        return read_tier_1()
    if resonant:
        return read_tier_2(query)
    if archival:
        return read_tier_3(query)
    if auto:
        result = read_tier_1()
        if result is None:
            result = read_tier_2(query)
        if result is None:
            result = read_tier_3(query)
        return result
```

| Mode | Tiers Queried | Use Case |
|------|---------------|----------|
| `surface` | Tier 1 only | Real-time phase state, daemon coordination |
| `resonant` | Tier 2 only | Semantic recall, structured memory |
| `archival` | Tier 3 only | Historical analysis, audit |
| `auto` | T1 → T2 → T3 (cascade) | General-purpose query, best-effort |

## 7. Consolidation Pipeline

```
Every ~300 s:
  1. ConsolidationResonator tags current Kuramoto state → TSM
  2. CIELMemoryConsolidator (LLM backend) processes raw logs → structured entries
  3. High-salience entries promoted to WPM (Tier 3)
  4. Low-salience entries pruned from Tier 1 (PhaseMemory decay)
```

### ConsolidationResonator
- Runs as a background thread in the sync daemon.
- Computes Berry phase from current oscillator state.
- Tags `psi_geom`, `Z_geom`, `R_geom` with salience estimate.
- Inserts into TSM with `holonomy_phase` index.

### CIELMemoryConsolidator
- Optional LLM-based daemon for semantic enrichment.
- Reads raw session logs from `~/.noema/logs/`.
- Produces structured TSM entries with sector labels and embeddings.
- Falls back to direct SQL insert if LLM backend is unavailable.

### Salience Heuristics

| Signal | Weight | Description |
|--------|--------|-------------|
| Euler residual `R` | 0.3 | Low `R` → higher salience (coherent state) |
| Closure penalty `cp` | 0.25 | Low `cp` → higher salience |
| Phase variance `var(phi)` | 0.2 | Moderate variance → higher salience |
| Flavor sum `Σ flavor[0:4]` | 0.15 | High coherence → higher salience |
| Harmonic lock | 0.1 | Locked harmonics → higher salience |

`salience = clamp(Σ (weight × signal), 0.0, 1.0)`

## 8. File Locations (Anonymized)

| Layer | Path | Type | Lifespan |
|-------|------|------|----------|
| NOEMA Surface | `/dev/shm/ciel_noema/` | tmpfs binary files | Volatile (reboot) |
| Tier 1 cache | `~/.noema/tier1/` | mmap + JSON | Volatile (process) |
| Tier 2 TSM | `~/.noema/tier2/tsm.db` | SQLite | Durable |
| Tier 2 StateDB | `~/.noema/tier2/state.db` | SQLite | Durable |
| Tier 3 WPM | `~/.noema/tier3/wave_archive.h5` | HDF5 | Archival |
| Tier 3 BraidLedger | `~/.noema/tier3/braid_ledger.jsonl` | JSONL | Archival |
| Raw logs | `~/.noema/logs/` | Plain text | Configurable retention |
| Consolidated memories | `~/.noema/memories/` | JSON + embeddings | Permanent |

Actual paths are configurable via environment variables:

| Variable | Default |
|----------|---------|
| `NOEMA_TIER1_DIR` | `~/.noema/tier1` |
| `NOEMA_TIER2_DIR` | `~/.noema/tier2` |
| `NOEMA_TIER3_DIR` | `~/.noema/tier3` |
| `NOEMA_LOG_DIR` | `~/.noema/logs` |
| `NOEMA_MEMORY_DIR` | `~/.noema/memories` |
| `CIEL_MEMORIES_DIR` | `~/Pulpit/CIEL_memories` |

## 9. Thread Safety

- Tier 1 (mmap): Concurrent reads safe; writers use O_SYNC with no advisory locks — single-writer convention via daemon roles.
- Tier 2 (SQLite): WAL mode with `busy_timeout = 5000` — safe for concurrent readers + single writer.
- Tier 3 (HDF5 + JSONL): Append-only for writers; readers use copies.
- **ConsolidationResonator**: Holds a per-tier lock during promotion; never blocks daemon phase evolution.

## 10. TieredMemoryOrchestrator Singleton

```python
class TieredMemoryOrchestrator:
    """Singleton — 1310-line implementation at ciel_omega/memory/tiered_orchestrator.py"""

    def __init__(self):
        self.tier1 = NOEMASurface() | PhaseMemory() | HolonomicMemoryOrchestrator()
        self.tier2 = TSMMemory() | StateDB() | HolonomicMemory() | CIELBlochEncoder()
        self.tier3 = WPMMemory() | BraidLedger() | UnifiedMemoryOrchestrator()
        self.consolidator = ConsolidationResonator() | CIELMemoryConsolidator()

    def write(self, payload, salience=0.0, bifurcation=0.0, tier="auto"):
        ...

    def read(self, query, surface=False, resonant=False, archival=False, auto=False):
        ...

    def consolidate(self):
        """Trigger background consolidation cycle."""
        ...
```

Every CIELingo sync cycle (60 s), the orchestrator writes a snapshot with `salience ≈ 0.3–0.7`, depending on closure state and flavor coherence.
