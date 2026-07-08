# test_gguf_comparison.py — tests/test_gguf_comparison.py

## Tożsamość
- **id_karty:** `REPO-TEST_GGUF_COMPARISON-A33F`
- **ścieżka:** `tests/test_gguf_comparison.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `1.947`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_gguf_comparison.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 1.947 |
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
GGUF presence vs. absence comparison tests.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestGGUFAbsent, TestGGUFPresent, TestGGUFComparison, TestGGUFPhasedState
- **funkcje:** `_make_registry`, `_make_couplings`, `test_is_installed_returns_false`, `test_list_models_returns_empty`, `test_manifest_shows_no_models`, `test_get_model_path_returns_none`, `test_pipeline_runs_without_gguf`, `test_sync_quality_without_gguf`, `mgr_with_model`, `test_is_installed_returns_true`, `test_list_models_returns_one_entry`, `test_manifest_includes_model_name`, `test_get_model_path_returns_path`, `test_ensure_model_returns_existing_file`, `test_pipeline_unchanged_with_gguf_present`, `_run_pipeline`, `test_closure_defect_identical_with_and_without_gguf`, `test_gguf_absent_is_faster_than_with_download`, `test_manifest_schema_consistent_across_states`, `test_gguf_model_spec_fields_match_known_models`, `test_pipeline_throughput_unaffected_by_gguf_presence`, `test_gguf_ext_has_non_zero_weight`, `test_gguf_weight_is_lower_than_python_weight`

## Opis
GGUF presence vs. absence comparison tests.

These tests document and verify the observable differences in CIEL-SOT-Agent
behaviour depending on whether a GGUF language-model file is present on
disk.

Key findings documented as assertions:
- The framework is fully functional without any GGUF model (no hard
  dependency on a model file for the core pipeline).
- When a GGUF model is present, GGUFMan
