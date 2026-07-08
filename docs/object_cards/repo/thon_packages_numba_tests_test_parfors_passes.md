# test_parfors_passes.py — .python_packages/numba/tests/test_parfors_passes.py

## Tożsamość
- **id_karty:** `REPO-TEST_PARFORS_PASSES-BFB5`
- **ścieżka:** `.python_packages/numba/tests/test_parfors_passes.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.731`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_parfors_passes.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.731 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Tests for sub-components of parfors.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MyPipeline, BaseTest, TestConvertSetItemPass, TestConvertNumpyPass, TestConvertReducePass, TestConvertLoopPass, TestPreParforPass, sub_pass_class
- **funkcje:** `_run_parfor`, `run_parfor_sub_pass`, `run_parfor_pre_pass`, `_run_parallel`, `run_parallel`, `run_parallel_check_output_array`, `check_records`, `test_setitem_full_slice`, `test_setitem_slice_stop_bound`, `test_setitem_slice_start_bound`, `test_setitem_gather_if_scalar`, `test_setitem_gather_if_array`, `check_numpy_allocators`, `check_numpy_random`, `test_numpy_allocators`, `test_numpy_random`, `test_numpy_arrayexpr`, `test_numpy_arrayexpr_ufunc`, `test_numpy_arrayexpr_boardcast`, `test_numpy_arrayexpr_reshaped`, `test_reduce_max_basic`, `test_reduce_max_masked`, `test_prange_reduce_simple`, `test_prange_map_simple`, `test_prange_two_args`, `test_prange_three_args`, `test_prange_map_inner_loop`, `test_prange_map_nested_prange`, `test_prange_map_none_index`, `test_prange_map_overwrite_index`

## Opis
Tests for sub-components of parfors.
These tests are aimed to produce a good-enough coverage of parfor passes
so that refactoring on these passes are easier with faster testing turnaround.
