---
name: workben-phasenav
priority: 1
description: >
  PhaseNav — solver, enrichment, algebra, analog bus, operator system, Poincaré viz
---
# Workben PHASENAV

PhaseNav — solver, enrichment, algebra, analog bus, operator system, Poincaré viz

## Źródła

Ten workben konsoliduje 10 źródłowych skilli:

- **PhaseNav Solver** (`SYS/phasenav-solver`)
- **PhaseNav Enrichment** (`SYS/phasenav-enrichment`)
- **PhaseNav Loader** (`SYS/phasenav-loader`)
- **Analog PhaseNav** (`SYS/noema-analog-phasenav`)
- **Phase Algebra** (`COMP/phase-algebra`)
- **Phase Memory Adapter** (`COMP/phase-memory-adapter`)
- **LoRA** (`COMP/noema-lora`)
- **Poincaré Disk** (`VIZ/poincare-disk`)
- **Orbital Visualization** (`VIZ/poincare-orbital-viz`)
- **Renderer: Poincaré Disk** (`VIZ/renderer-phasedisk`)

## Kluczowe wzorce

### PhaseNav Solver

- | Pole | Typ | Opis |
- |------|-----|------|
- | `source_card_id` | str | Origin concept |

### PhaseNav Enrichment

- IDENTITY, DIFFERENCE, ORDER, COMPOSITION, ADDITION,
- FORCE, NEGATION, QUESTION, TRANSFORM, RETURN,
- FOLD, BOUNDARY, SCOPE, AFFECT, CONSENT,

### PhaseNav Loader

- | Field | Key from | Źródło |
- |-------|----------|--------|
- | `name_mass` | `normalized` | `*NAME_MASS.noema.jsonl` |

### Analog PhaseNav

- | Node | Interval | strength | temp | Funkcja |
- |------|----------|----------|------|---------|
- | Hot | 1s | 0.8 | 0.9 | Eksploracja — szum + operator |

### Phase Algebra

- | Kanał | Oscylatory | Funkcja | Harmoniczne |
- |-------|-----------|---------|-------------|
- | M0 | 0-2 | Perception | {1,3} |

### Phase Memory Adapter

- `src/ciel_geometry/phase_memory_adapter.py`

### LoRA

- - `scripts/ciel_lora_init.py`
- - `scripts/ciel_lora_train.py`
- - `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`

### Poincaré Disk

- OrchOrbital: entity_count=21, mean_coupling=0.8514
- - Adrian_Lipa: coupling=0.97 (konstytutywny)
- - relational_contract: coupling=1.0 (nienaruszalny)

### Orbital Visualization

- | Renderer | Output | Use case |
- |----------|--------|----------|
- | `renderer_ascii.py` | Terminal (60×20) | Debug bez X11 |

### Renderer: Poincaré Disk

- Terminalowy Poincaré disk — entities jako kropki, edges jako linie.
- Do debugowania bez X11.
- Interaktywny orbital cockpit — entity circles z coupling labels,

## Jak używać

```python
skill("workben-phasenav")
```

Ładuje wiedzę ze wszystkich 10 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
