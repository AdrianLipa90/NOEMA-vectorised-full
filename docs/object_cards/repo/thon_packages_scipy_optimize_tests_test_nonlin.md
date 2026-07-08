# test_nonlin.py — .python_packages/scipy/optimize/tests/test_nonlin.py

## Tożsamość
- **id_karty:** `REPO-TEST_NONLIN-230C`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test_nonlin.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.378`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test_nonlin.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.378 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Unit tests for nonlinear solvers

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestNonlin, TestSecant, TestLinear, TestJacobianDotSolve, TestNonlinOldTests
- **funkcje:** `F`, `F2`, `F2_lucky`, `F3`, `F4_powell`, `F5`, `F6`, `_check_nonlin_func`, `_check_root`, `_check_func_fail`, `test_problem_nonlin`, `test_tol_norm_called`, `test_problem_root`, `test_no_convergence`, `test_warnings_invalid_inner_param`, `test_non_inner_prefix`, `_check_secant`, `test_broyden1`, `test_broyden2`, `test_broyden1_update`, `test_broyden2_update`, `test_anderson`, `_check`, `test_broyden1`, `test_broyden2`, `test_anderson`, `test_krylov`, `_check_autojac`, `test_jac_sparse`, `test_jac_ndarray`

## Opis
Unit tests for nonlinear solvers
Author: Ondrej Certik
May 2007
