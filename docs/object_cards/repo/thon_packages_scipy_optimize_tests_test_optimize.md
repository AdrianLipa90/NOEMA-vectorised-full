# test_optimize.py — .python_packages/scipy/optimize/tests/test_optimize.py

## Tożsamość
- **id_karty:** `REPO-TEST_OPTIMIZE-A67F`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test_optimize.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.089`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test_optimize.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.089 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
Unit tests for optimization routines from optimize.py

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CheckOptimize, CheckOptimizeParameterized, TestOptimizeWrapperDisp, TestOptimizeWrapperNoDisp, TestOptimizeNoWrapperDisp, TestOptimizeNoWrapperNoDisp, TestOptimizeSimple, TestLBFGSBBounds, TestOptimizeScalar, TestBracket, TestNewtonCg, TestRosen, TestOptimizeResultAttributes, TestBrute, TestIterationLimits, FunctionWithGradient, TestGlobalOptimization, TestWorkers, TestAnnotations, Callback
- **funkcje:** `test_check_grad`, `test_maxfev_test`, `test_wrap_scalar_function_with_validation`, `test_obj_func_returns_scalar`, `test_neldermead_iteration_num`, `test_neldermead_respect_fp`, `test_neldermead_xatol_fatol`, `test_neldermead_adaptive`, `test_bounded_powell_outsidebounds`, `test_bounded_powell_vs_powell`, `test_onesided_bounded_powell_stability`, `test_minimize_with_scalar`, `test_brent_negative_tolerance`, `test_line_for_search`, `test_linesearch_powell`, `test_linesearch_powell_bounded`, `test_powell_limits`, `test_powell_output`, `himmelblau`, `himmelblau_grad`, `himmelblau_hess`, `test_minimize_multiple_constraints`, `f1`, `f2`, `f3`, `brute_func`, `test_cobyla_threadsafe`, `test_result_x_shape_when_len_x_is_one`, `function_with_gradient`, `test_memoize_jac_function_before_gradient`

## Opis
Unit tests for optimization routines from optimize.py

Authors:
   Ed Schofield, Nov 2005
   Andrew Straw, April 2008
