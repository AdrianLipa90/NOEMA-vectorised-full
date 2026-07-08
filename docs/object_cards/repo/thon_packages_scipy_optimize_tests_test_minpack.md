# test_minpack.py — .python_packages/scipy/optimize/tests/test_minpack.py

## Tożsamość
- **id_karty:** `REPO-TEST_MINPACK-9970`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test_minpack.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.418`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test_minpack.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.418 |
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
Unit tests for optimization routines from minpack.py.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ReturnShape, TestFSolve, TestRootHybr, TestRootLM, TestNfev, TestLeastSq, TestCurveFit, TestFixedPoint, test_self
- **funkcje:** `dummy_func`, `sequence_parallel`, `pressure_network`, `pressure_network_jacobian`, `pressure_network_fun_and_grad`, `test_pressure_network_no_gradient`, `test_pressure_network_with_gradient`, `test_wrong_shape_func_callable`, `test_wrong_shape_func_function`, `test_wrong_shape_fprime_callable`, `test_wrong_shape_fprime_function`, `test_func_can_raise`, `test_Dfun_can_raise`, `test_float32`, `test_reentrant_func`, `test_reentrant_Dfunc`, `test_concurrent_no_gradient`, `test_concurrent_with_gradient`, `test_pressure_network_no_gradient`, `test_pressure_network_with_gradient`, `test_pressure_network_with_gradient_combined`, `test_pressure_network_no_gradient`, `setup_method`, `zero_f`, `test_root_nfev`, `test_fsolve_nfev`, `setup_method`, `residuals`, `residuals_jacobian`, `test_basic`

## Opis
Unit tests for optimization routines from minpack.py.
