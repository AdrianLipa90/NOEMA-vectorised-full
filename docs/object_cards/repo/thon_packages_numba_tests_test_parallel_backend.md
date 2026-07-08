# test_parallel_backend.py — .python_packages/numba/tests/test_parallel_backend.py

## Tożsamość
- **id_karty:** `REPO-TEST_PARALLEL_BACKEN-FE41`
- **ścieżka:** `.python_packages/numba/tests/test_parallel_backend.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.677`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_parallel_backend.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.677 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Tests the parallel backend

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** runnable, jit_runner, mask_runner, linalg_runner, vectorize_runner, guvectorize_runner, _proc_class_impl, TestParallelBackendBase, TestParallelBackend, TestInSubprocess, TestSpecificBackend, ThreadLayerTestHelper, TestThreadingLayerSelection, TestThreadingLayerPriority, TestMiscBackendIssues, TestForkSafetyIssues, TestTBBSpecificIssues, TestInitSafetyIssues, TestOpenMPVendors
- **funkcje:** `foo`, `ufunc_foo`, `gufunc_foo`, `chooser`, `compile_factory`, `_get_mp_classes`, `linalg`, `linalg`, `run_compile`, `run_compile`, `generate`, `run_cmd`, `run_test_in_separate_process`, `_inject`, `generate`, `run_cmd`, `_inject`, `generate`, `each_env_var`, `test_valid_env_var`, `test_invalid_env_var`, `test_omp`, `test_tbb`, `test_workqueue`, `test_omp_stack_overflow`, `test_single_thread_tbb`, `test_workqueue_aborts_on_nested_parallelism`, `test_workqueue_handles_fork_from_non_main_thread`, `test_check_threading_layer_is_gnu`, `test_par_parent_os_fork_par_child`

## Opis
Tests the parallel backend
