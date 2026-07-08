---
name: cielingo-core-structure
priority: 1
description: >
  >
---
# CIELingo Core Structure

## Pakiety

```
cielingo_core/
├── global_layer/
│   ├── meaning_loop.py         — MeaningLoop, LoopState, SemanticScar
│   ├── global_algorithm_v02    — run_global_algorithm_v02()
│   └── contracts.py            — HolonomicJReport, MeaningAction
├── language_spaces/
│   ├── pl/                     — PolishRegionalSolver
│   ├── en/                     — English solver
│   └── ja/                     — Japanese solver (0 cards)
├── expressive/                 — ExpressiveStyle (plain, formal, ...)
├── meaning/                    — MeaningRepairCandidate, repair routing
├── regional/                   — Regional solver base
├── alignment/                  — Semantic alignment
├── lingophysics/               — Phase-language bridge
├── semantic_neural/            — Semantic neural (heuristic fallback)
├── timing/                     — Temporal logic
├── bridge/                     — CIELingoBridge
├── io/                         — File I/O
├── doctor/                     — Diagnostics
├── noema_surface/              — Surface bridge
└── apocalypos_bridge/          — ApocalypOS integration
```

## Liczby

- 5,590 card records w atlasie
- 3,686 PL, 484 EN, 462 DE, 471 ES, 463 FR, 24 universal
- 44 `.incoming_*` pliki (sabotaż)
- 33 `except:pass` bloki
- 0 cross-importów ciel_omega ↔ cielingo

## Plik

`cielingo_core/` w kanonicznym repo
