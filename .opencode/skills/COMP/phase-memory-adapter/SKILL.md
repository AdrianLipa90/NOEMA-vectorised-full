---
name: phase-memory-adapter
priority: 4
description: >
  >
---
# Phase Memory Adapter

## Storage

```
query text → hypervector (binary HD computing)
  + phase signature (24D from phasenav_enrich)
  + flavor snapshot
```

## Retrieval

```
query → hypervector
  → cosine similarity z pamięcią
  → top-k + phase resonance filter
  → zwraca phase/flavor + text reference
```

## Plik

`src/ciel_geometry/phase_memory_adapter.py`
