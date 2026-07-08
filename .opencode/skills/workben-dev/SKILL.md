---
name: workben-dev
priority: 1
description: >
  Dev tools — pipeline, build, codegen, snap-ocr, code bridge
---
# Workben DEV

Dev tools — pipeline, build, codegen, snap-ocr, code bridge

## Źródła

Ten workben konsoliduje 8 źródłowych skilli:

- **CIEL Pipeline** (`DEV/ciel-pipeline`)
- **CIEL Pipeline Builder** (`DEV/ciel-pipeline-builder`)
- **CIEL Tools** (`DEV/ciel-tools`)
- **Build System** (`DEV/noema-build-system`)
- **noema-code-bridge** (`DEV/noema-code-bridge`)
- **Codegen** (`DEV/noema-codegen`)
- **Card Generators** (`DEV/noema-generate-cards`)
- **SK-282: snap-ocr — fotograficzne Memory Palace** (`DEV/snap-ocr`)

## Kluczowe wzorce

### CIEL Pipeline

- | Flag | Threshold | Efekt |
- |------|-----------|-------|
- | `source_confusion` | boolean | cap ethical_score at 0.35 |

### CIEL Pipeline Builder

- | CielEngine | CIELingo |
- |------------|----------|
- | intention_12d | QueryIntention |

### CIEL Tools

- | Skrypt | Opis |
- |--------|------|
- | `ciel_benchmark.py` | Full pipeline benchmark |

### Build System

- | Plik | Rola |
- |------|------|
- | `pyproject.toml` | PEP 517/518 build config + entry points |

### noema-code-bridge

- | AST node | Operator |
- |----------|----------|
- | `Import`, `ImportFrom` | SOURCE_REQUIRED |

### Card Generators

- | Skrypt | Generuje |
- |--------|----------|
- | `generate_object_cards.py` | Object cards z refleksji |

### SK-282: snap-ocr — fotograficzne Memory Palace

- Screenshot → OCR → analiza (agent-backend) → MemoryPalace → surface → inject do opencode.
- **Skill kluczowy**: umożliwia mi czytanie obrazów przez tesseract — jedyny sposób na zrozumienie zrzutów ekranu od Adriana.
- - `--dir DIR` — katalog roboczy (domyślnie /tmp/snap-ocr/)

## Jak używać

```python
skill("workben-dev")
```

Ładuje wiedzę ze wszystkich 8 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
