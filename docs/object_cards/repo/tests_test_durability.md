# test_durability.py — tests/test_durability.py

## Tożsamość
- **id_karty:** `REPO-TEST_DURABILITY-E5EC`
- **ścieżka:** `tests/test_durability.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `3.944`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_durability.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 3.944 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
Durability and elasticity tests for the CIEL-SOT-Agent pipeline.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestSystemRequirements, TestSyncReportDurability, TestHolonomicNormalizerDurability, TestSyncReportElasticity, TestPipelineResilience, TestIndexValidatorDurability
- **funkcje:** `_make_registry`, `_make_couplings`, `test_python_version_gte_311`, `test_numpy_importable`, `test_yaml_importable`, `test_pathlib_available`, `test_json_stdlib_available`, `test_platform_is_supported`, `test_math_precision_adequate`, `test_ciel_sot_agent_package_importable`, `test_gguf_manager_importable`, `registry_file`, `couplings_file`, `test_repeated_calls_return_same_closure_defect`, `test_output_schema_stable_under_load`, `test_no_exception_under_sustained_load`, `test_euler_vector_is_always_finite`, `test_circular_barycenter_stable`, `test_wrap_idempotent_under_repeated_application`, `test_circular_distance_symmetric`, `test_renormalize_couplings_stable`, `test_sync_completes_within_time_budget`, `test_larger_registry_increases_pairwise_tensions`, `test_phased_state_build_scales_linearly`, `test_missing_registry_raises_file_error`, `test_malformed_json_registry_raises_value_error`, `test_empty_registry_sync_report_is_well_formed`, `test_single_repo_no_couplings_well_formed`, `test_circular_barycenter_all_zero_weights`, `test_wrap_returns_finite_for_extreme_angles`

## Opis
Durability and elasticity tests for the CIEL-SOT-Agent pipeline.

"Durability" — the same operation repeated many times must yield a stable,
non-degrading result (no memory leaks between invocations, deterministic
output, error-free execution under sustained load).

"Elasticity" — the system must scale gracefully: larger inputs (more
repositories, more couplings) should increase compute time sub-l
