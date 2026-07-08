---
name: cielingo-canon
priority: 1
description: >
  >
---
# CIELingo Canon (NOEMA mapping)

## Pakiety

```
cielingo_core/
├── global_layer/
│   ├── meaning_loop.py       — MeaningLoop, LoopState, SemanticScar
│   ├── global_algorithm_v02  — run_global_algorithm_v02
│   └── contracts.py          — HolonomicJReport
├── language_spaces/
│   ├── pl/                   — Polish solver
│   ├── en/                   — English solver
│   └── ja/                   — Japanese solver
├── expressive/               — ExpressiveStyle (plain/formal/...)
├── meaning/                  — MeaningRepairCandidate, repair routing
└── bridge/                   — CIELingoBridge
```

## → NOEMA surface

| CIELingo | Surface |
|----------|---------|
| closure_penalty | flavor[5] → D_f → g_boost |
| SemanticScar | `cielingo_unresolved_scars` w bridge metadata |
| MeaningLoop state | `cielingo_severity` |
| Immune flags | `cielingo_immune` → ethical score cap |
