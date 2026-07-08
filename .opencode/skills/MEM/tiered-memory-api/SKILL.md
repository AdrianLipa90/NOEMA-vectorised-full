---
name: tiered-memory-api
priority: 1
description: >
  >
---
# Tiered Memory Orchestrator

## Tiers

| Tier | Enum | Storage | Trwałość |
|------|------|---------|----------|
| Tier 1 | `Tier.FAST` | NOEMA surface mmap + PhaseMemory mmap + M0-M8 | Volatile |
| Tier 2 | `Tier.MEDIUM` | TSM SQLite + StateDB + HolonomicMemory + BlochEncoder | Durable |
| Tier 3 | `Tier.DEEP` | WPM HDF5 + BraidLedger JSONL + UnifiedMemoryOrchestrator | Archival |
| Async | `Tier.ASYNC` | ConsolidationResonator + CIELMemoryConsolidator | Background |

## Singleton

```python
from CIEL_OMEGA_COMPLETE_SYSTEM.ciel_omega.memory.tiered_orchestrator import TieredMemoryOrchestrator, WriteMode, ReadMode

tmo = TieredMemoryOrchestrator()  # singleton
```

## Write API

```python
def write(self, content: str,
          metadata: dict | None = None,
          mode: WriteMode = WriteMode.AUTO) -> TieredWriteResult:
```

**WriteMode routing:**

| Mode | Tiers |
|------|-------|
| `FAST` | Tier 1 only |
| `DURABLE` | Tier 1 + Tier 2 |
| `DEEP` | Tier 1 + Tier 2 + Tier 3 |
| `AUTO` | Tier 1 zawsze + Tier 2 jeśli metadata.salience ≥ 0.6 + Tier 3 jeśli metadata.bifurcation ≥ 1 |

```python
# Tier 1: surface mmap write (phi, flavor) + PhaseMemory bind + M0-M8 evolve
# Tier 2: TSM SQLite insert (HolonomicMemory.stamp_new) + Hebbian update
# Tier 3: UnifiedMemoryOrchestrator.capture() → promote_if_bifurcated()
```

## Read API

```python
def read(self, query: str,
         mode: ReadMode = ReadMode.AUTO,
         top_k: int = 10) -> TieredReadResult:
```

**ReadMode routing:**

| Mode | Tiers searched |
|------|----------------|
| `SURFACE` | Tier 1 only |
| `RESONANT` | Tier 2 only (HolonomicMemory phase-resonant) |
| `DEEP` | Tier 2 + Tier 3 (full archival) |
| `AUTO` | query < 3 słów: Tier1 → Tier2; query ≥ 3 słów: Tier2 → Tier1 |

## Snapshot

```python
snap: TieredSnapshot = tmo.snapshot()
# snap.tier1, snap.tier2, snap.tier3 — stan każdego tieru
```

## Consolidation (co 50 cykli)

```python
tmo.consolidate()  # wywołuje ConsolidationResonator.run():
# 1. load_consolidations(400) → ostatnie 400 rekordów
# 2. Kuramoto sync: ω = M_sem·2π + Lorentz(σ=0.3), K_ij = Σ M_sem(t)
# 3. Write tag cards → object_cards/db/consolidations/
# 4. Write → TSM (D_type='episodic', phi_berry, winding_n)
# 5. Update Bloch encoder (lr=0.02)
```

## Health

```python
status = tmo.health()
# {tier1: {alive, n_fields}, tier2: {tsm_size, db_alive}, tier3: {wpm_alive}}
```

## Lokacja

`src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/tiered_orchestrator.py` (~1310 lines)
