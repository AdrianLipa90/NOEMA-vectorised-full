---
name: android-zip-analysis
priority: 5
description: >
  >
---
# Android ZIP Analysis

## Pipeline

1. `unzip -l` listing
2. Python zipfile.ZipFile do odczytu wnętrza
3. PhaseNav enrichment na znalezionych plikach
4. Dodanie do library_index przez noema_learn_file.py

## Zrodlo

- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/phase_sweep_analysis.py`
