# test_gguf_manager.py — tests/test_gguf_manager.py

## Tożsamość
- **id_karty:** `REPO-TEST_GGUF_MANAGER-B29A`
- **ścieżka:** `tests/test_gguf_manager.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `3.956`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_gguf_manager.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 3.956 |
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
Tests for the CIEL GGUF model manager.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestKnownModels, TestModelSpec, TestGGUFManagerPaths, TestGGUFManagerListModels, TestGGUFManagerManifest, TestGGUFManagerEnsureModel, TestSHA256Verification, TestModuleHelpers
- **funkcje:** `test_registry_not_empty`, `test_default_key_present`, `test_each_spec_has_name_and_url`, `test_spec_tags_are_list`, `test_create_minimal`, `test_create_full`, `test_models_dir_uses_custom_path`, `test_model_path_returns_expected_name`, `test_model_path_unknown_key_returns_none`, `test_is_installed_false_when_file_missing`, `test_is_installed_true_when_file_present`, `test_list_empty_when_dir_missing`, `test_list_returns_gguf_files`, `test_list_includes_size_and_path`, `test_load_manifest_empty_when_missing`, `test_save_and_load_manifest_round_trip`, `test_manifest_path_is_inside_models_dir`, `test_ensure_returns_existing_file`, `test_ensure_raises_for_unknown_key`, `test_ensure_calls_download_when_missing`, `test_progress_callback_receives_calls`, `test_partial_file_cleaned_on_download_error`, `test_sha256_mismatch_raises_and_removes_file`, `test_get_model_path_returns_none_when_missing`, `test_get_model_path_returns_path_when_present`, `test_download_default_model_calls_ensure`, `test_default_models_dir_env_var`, `test_default_models_dir_xdg`, `fake_download`, `cb`

## Opis
Tests for the CIEL GGUF model manager.

These tests do NOT perform real network downloads.  They verify:
- GGUFManager API contracts
- model_path / is_installed logic
- list_models with real filesystem
- manifest read/write round-trip
- ensure_model download path is exercised via monkeypatching
- ModelSpec and KNOWN_MODELS registry
- Module-level helpers (get_model_path, download_default_model)
