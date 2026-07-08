---
name: v1-0-batch01-local-library-patch-report
priority: 5
description: >
  >
---
# v1.0 Batch01 Local Library Patch Report

## Contents

- **Added**: - 36 concept cards × 5 languages = 180 language panels. - Separate concept/operator library growth model. - Batch01 YAML
- **Important limitation**: This is a curated seed, not an authoritative multilingual dictionary. Synonyms, antonyms, forms, and
- **Next recommended patch**: v1.1 should add the `BatchRegistry` and a conflict detector: ```text new card -> compare to prior cards -> tag synonyms/
- **Test result**: Local test command: ```bash PYTHONPATH=. pytest -q ``` Result: `20 passed`.

## Key Points

- 36 concept cards × 5 languages = 180 language panels.
- Separate concept/operator library growth model.
- Batch01 YAML/JSON/CSV/XLSX artifacts.
- SQLite database: `data/sqlite/cielingo_batch01_v1_0.sqlite`.
- HDF5 matrix store: `data/hdf5/cielingo_batch01_v1_0.h5`.
- Graph exports: JSON and GraphML.
- Heatmaps: grammar gauge distance and concept-operator incidence.
- Tests for concept/operator separation and batch counts.

## Code

```
## Test result

Local test command:
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/reports/v1_0_batch01_local_library_patch_report.md` (36 lines, 1058B)*