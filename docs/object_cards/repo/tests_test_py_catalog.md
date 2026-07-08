# test_py_catalog.py — tests/test_py_catalog.py

## Tożsamość
- **id_karty:** `REPO-TEST_PY_CATALOG-D5CA`
- **ścieżka:** `tests/test_py_catalog.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `3.204`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_py_catalog.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 3.204 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Performance and correctness tests for py_catalog and noema_sot integration.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestBuildPerformance, TestTagCorrectness, TestQueryFilters, TestCoOccurrence, TestDelta, TestJsonExport, TestNoemIntegration
- **funkcje:** `_fresh_build`, `test_build_completes_under_30s`, `test_build_idempotent`, `test_file_count_realistic`, `setup_method`, `test_orbital_bridge_is_level1_bridge`, `test_noema_sot_is_level1_registry`, `test_ciel_pipeline_is_executor`, `test_tests_are_level4`, `test_noema_sot_highest_msem_in_level1`, `test_lines_of_code_populated`, `test_ciel_pipeline_loc_substantial`, `setup_method`, `test_query_by_level`, `test_query_by_tag`, `test_query_by_subsystem`, `test_query_by_min_loc`, `test_query_combined`, `setup_method`, `test_cooccurrence_table_populated`, `test_cooccurrence_mean_msem_valid`, `test_cooccurrence_count_positive`, `test_first_build_records_added`, `setup_method`, `test_json_exists`, `test_json_structure`, `test_json_entries_have_required_fields`, `setup_method`, `test_noema_py_summary_loaded`, `test_noema_context_contains_py_block`

## Opis
Performance and correctness tests for py_catalog and noema_sot integration.

Tests cover:
  - build speed (< 30s for 600 files)
  - idempotency (second build produces 0 added/removed)
  - tag correctness for known files
  - query filters (level, tag, min_loc)
  - co-occurrence table populated
  - delta tracking
  - noema_sot py_catalog summary present
