# test__basinhopping.py — .python_packages/scipy/optimize/tests/test__basinhopping.py

## Tożsamość
- **id_karty:** `REPO-TEST__BASINHOPPING-6C12`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test__basinhopping.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.631`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test__basinhopping.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.631 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
Unit tests for the basin hopping global minimization algorithm.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MyTakeStep1, MyAcceptTest, MyCallBack, TestBasinHopping, Test_Storage, Test_RandomDisplacement, Test_Metropolis, Test_AdaptiveStepsize
- **funkcje:** `func1d`, `func2d_nograd`, `func2d`, `func2d_easyderiv`, `myTakeStep2`, `setup_method`, `test_TypeError`, `test_input_validation`, `test_1d_grad`, `test_2d`, `test_njev`, `test_jac`, `test_2d_nograd`, `test_all_minimizers`, `test_all_nograd_minimizers`, `test_pass_takestep`, `test_pass_simple_takestep`, `test_pass_accept_test`, `test_pass_callback`, `test_minimizer_fail`, `test_niter_zero`, `test_rng_reproducibility`, `test_random_gen`, `test_monotonic_basin_hopping`, `create_storage`, `test_higher_f_rejected`, `test_lower_f_accepted`, `setup_method`, `test_random`, `setup_method`

## Opis
Unit tests for the basin hopping global minimization algorithm.
