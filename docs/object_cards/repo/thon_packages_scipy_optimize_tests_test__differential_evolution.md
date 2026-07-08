# test__differential_evolution.py — .python_packages/scipy/optimize/tests/test__differential_evolution.py

## Tożsamość
- **id_karty:** `REPO-TEST__DIFFERENTIAL_E-4697`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test__differential_evolution.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.868`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test__differential_evolution.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.868 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Unit tests for the differential global minimization algorithm.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestDifferentialEvolutionSolver
- **funkcje:** `setup_method`, `teardown_method`, `quadratic`, `test__strategy_resolves`, `test__mutate1`, `test__mutate2`, `test__randtobest1`, `test__currenttobest1`, `test_can_init_with_dithering`, `test_invalid_mutation_values_arent_accepted`, `test_invalid_functional`, `test__scale_parameters`, `test__unscale_parameters`, `test_equal_bounds`, `test__ensure_constraint`, `test_differential_evolution`, `test_best_solution_retrieval`, `test_intermediate_result`, `test_callback_terminates`, `test_args_tuple_is_passed`, `test_init_with_invalid_strategy`, `test_bounds_checking`, `test_select_samples`, `test_maxiter_stops_solve`, `test_maxfun_stops_solve`, `test_quadratic`, `test_quadratic_from_diff_ev`, `test_rng_gives_repeatability`, `test_random_generator`, `test_exp_runs`

## Opis
Unit tests for the differential global minimization algorithm.
