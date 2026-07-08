# test_pipeline_audit.py — tests/test_pipeline_audit.py

## Tożsamość
- **id_karty:** `REPO-TEST_PIPELINE_AUDIT-79D3`
- **ścieżka:** `tests/test_pipeline_audit.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `4.549`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_pipeline_audit.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 4.549 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
Pipeline audit tests — verify every source module has a defined role

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestModulePresence, TestModuleDocstrings, TestEntryPoints, TestScriptsIntegrity, TestModuleImportability
- **funkcje:** `_collect_source_modules`, `_collect_scripts`, `_has_module_docstring`, `_has_callable`, `_imports_ciel_module`, `test_module_file_exists`, `test_no_unexpected_top_level_py_files`, `test_has_module_docstring`, `test_module_exports_main`, `test_gui_exports_main`, `test_gguf_manager_exports_download_helper`, `test_all_scripts_import_ciel_modules`, `test_all_run_scripts_have_if_main_guard`, `test_scripts_have_no_hardcoded_absolute_paths`, `test_integration_scripts_have_correct_structure`, `test_module_importable`, `test_sapiens_panel_submodules_importable`

## Opis
Pipeline audit tests — verify every source module has a defined role
and that no orphaned scripts exist without a corresponding entry point.

These tests reflect the "testy popeliny" requirement: confirm the full
pipeline topology is coherent, each file belongs to the system, and
no loose scripts hang without a clear integration path.
