---
date: 2026-06-27
tags: [knowledge-db, cielingo, bridge, engine, integration]
---

# 2026-06-27 part 4 — Knowledge DB → CIELingo bridge + engine integration

## knowledge_bridge.py
- [`src/cielingo_core/bridge/knowledge_bridge.py`](../src/cielingo_core/bridge/knowledge_bridge.py)
- `query(text, top_n)` → TF-IDF cosine similarity nad 545 dokami (~0.85s)
- `check_coverage(text)` → coverage score + match count (0.57s)
- `get_neighbors(idx)` → semantic affinity z bazy (0.01s)
- Optymalizacja: tylko candidate docs (współdzielące term z query)

## engine.py step 5b
- `understand_query()` + `check_coverage()` → immune flags z realną bazą
- Jeśli `covered=True` → obniża `authority_risk` i `source_required`

## engine.py step 11b
- `_cielingo_meaning` wzbogacone o `knowledge_docs` (top 3) i `knowledge_coverage`
- Realne źródła zamiast pustych candidates

## Co to zmienia
- CIELingo nie diagnozuje w próżni — sprawdza bazę dokumentów
- `source_required=True` bez pokrycia → MISSING_SOURCE scar
- `source_required=True` z pokryciem → obniżona severity, repair candidate z plikami

## Architecture
```
engine.py step 5b
├── understand_query(text)       — CIELingo intent analysis
├── check_coverage(text)         — knowledge DB TF-IDF → coverage score
├── query(text, top_n=3)         — top docs z filenames/themes
└── _cielingo_immune flags       — grounded in real document coverage

engine.py step 11b
├── SemanticScar[]               — MISSING_SOURCE, AUTHORITY_LEAK, etc.
├── route_repairs_for_meaning_loop
├── build_global_meaning_signal  — severity
└── _cielingo_meaning            — knowledge_docs + knowledge_coverage
```

## Zero błędów
- knowledge_bridge.py + engine.py syntax OK, wszystkie importy resolve
