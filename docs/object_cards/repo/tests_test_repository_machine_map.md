# test_repository_machine_map.py — tests/test_repository_machine_map.py

## Tożsamość
- **id_karty:** `REPO-TEST_REPOSITORY_MACH-D32E`
- **ścieżka:** `tests/test_repository_machine_map.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `5.155`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_repository_machine_map.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 5.155 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
Tests for current documentation consistency on main.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestRetainedFilesPresent, TestWorkflowREADME, TestIndexDocumentation, TestOperationsDocumentation, TestPackagingReadme, TestPackagingDebReadme, TestMainReadme
- **funkcje:** `test_json_machine_map_present`, `test_yaml_machine_map_present`, `test_declaration_implementation_matrix_present`, `test_repository_guide_human_present`, `test_documentation_consistency_todo_present`, `load_content`, `test_file_exists`, `test_documents_current_workflow_surface`, `test_documents_gh_repo_coupling_workflow`, `test_has_current_workflows_section`, `test_has_structural_rule_section`, `test_structural_rule_mentions_trigger`, `test_structural_rule_mentions_entrypoint`, `test_has_documentation_rule_section`, `test_coupling_workflow_describes_schedule`, `test_coupling_workflow_describes_script`, `test_coupling_workflow_describes_commit_behavior`, `load_content`, `test_file_exists`, `test_does_not_reference_declaration_implementation_matrix`, `test_does_not_reference_repository_guide_human`, `test_does_not_reference_json_machine_map`, `test_does_not_reference_yaml_machine_map`, `test_has_console_entrypoints_section`, `test_console_entrypoints_includes_gui`, `test_console_entrypoints_includes_sync`, `test_console_entrypoints_includes_gh_coupling`, `test_console_entrypoints_includes_orbital_bridge`, `test_console_entrypoints_includes_sapiens_client`, `test_console_entrypoints_includes_runtime_evidence_ingest`

## Opis
Tests for current documentation consistency on main.

These tests verify the current repository state rather than a historical
single-PR cleanup snapshot:
- retained machine-map and documentation files that are still part of main
  remain present on disk,
- `.github/workflows/README.md` reflects the currently documented workflow
  surface,
- docs and packaging surfaces remain internally consistent
