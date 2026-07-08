# test_linprog.py — .python_packages/scipy/optimize/tests/test_linprog.py

## Tożsamość
- **id_karty:** `REPO-TEST_LINPROG-5925`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test_linprog.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.818`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test_linprog.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.818 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Unit test for Linear Programming

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LinprogCommonTests, LinprogSimplexTests, LinprogIPTests, LinprogRSTests, LinprogHiGHSTests, TestLinprogSimplexDefault, TestLinprogSimplexBland, TestLinprogSimplexNoPresolve, TestLinprogIPDense, TestLinprogIPSparse, TestLinprogIPSparsePresolve, TestLinprogIPSpecific, TestLinprogRSCommon, TestLinprogRSBland, TestLinprogHiGHSSimplexDual, TestLinprogHiGHSIPM, TestLinprogHiGHSMIP, AutoscaleTests, TestAutoscaleIP, TestAutoscaleSimplex
- **funkcje:** `_assert_iteration_limit_reached`, `_assert_infeasible`, `_assert_unbounded`, `_assert_unable_to_find_basic_feasible_sol`, `_assert_success`, `magic_square`, `lpgen_2d`, `very_random_gen`, `nontrivial_problem`, `l1_regression_prob`, `generic_callback_test`, `test_unknown_solvers_and_options`, `test_choose_solver`, `test_deprecation`, `test_highs_status_message`, `test_bug_17380`, `cb`, `test_callback`, `test_disp`, `test_docstring_example`, `test_type_error`, `test_aliasing_b_ub`, `test_aliasing_b_eq`, `test_non_ndarray_args`, `test_unknown_options`, `test_integrality_without_highs`, `test_invalid_inputs`, `test_sparse_constraints`, `test_maxiter`, `test_bounds_fixed`

## Opis
Unit test for Linear Programming
