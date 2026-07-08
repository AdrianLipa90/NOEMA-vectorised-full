---
name: storage-fallback-json-protocol
priority: 4
description: >
  >
---
# CIEL-LNS/Ω v1.4: Storage Fallback Protocol

## Contents

- **Motivation**: CIELingo uses several storage layers: - YAML for readable cards and configs - JSON for stable interchange and fallback -
- **Canonical fallback rule**: ```text write(target_format) if error: write(JSON fallback) write(fallback report) continue pipeline ```
- **Required metadata**: Every fallback record must include: ```yaml preferred_format: hdf5 | sqlite | xlsx | graphml | other fallback_format: js
- **Epistemic rule**: Fallback is not silent. Fallback must be reported. ```text Silent fallback = invalid state transition Reported fallback 
- **Data integrity rule**: If a binary export fails, the JSON fallback must preserve at least: - batch id - object ids - relation ids - language pa
- **Implementation module**: The implementation lives in: ```text src/lingophysics/storage_fallback.py ``` It provides: ```python write_hdf5_or_json(

## Key Points

- YAML for readable cards and configs
- JSON for stable interchange and fallback
- CSV/XLSX for human spreadsheets
- SQLite for indexed relational queries
- HDF5 for dense vectors, matrices, heatmaps, and numeric datasets
- GraphML/JSON for graph exports
- matrices as nested arrays or sparse records
- provenance of the export attempt

## Code

```
The goal is not elegance. The goal is survival of state.

## Motivation

CIELingo uses several storage layers:

- YAML for readable cards and configs
- JSON for stable interchange and fallback
- CSV/XLSX for human spreadsheets
- SQLite for indexed relational queries
- HDF5 for dense vectors, matrices, heatmaps, and numeric datasets
- GraphML/JSON for graph exports

Binary and dependency-heavy formats can fail because of missing libraries, file locks, platform issues, or schema mismatches. A fail
```

```
## Required metadata

Every fallback record must include:
```

```
## Epistemic rule

Fallback is not silent. Fallback must be reported.
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/27_STORAGE_FALLBACK_JSON_PROTOCOL.md` (86 lines, 1859B)*