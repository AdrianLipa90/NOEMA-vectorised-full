# test_iterative.py — .python_packages/scipy/sparse/linalg/_isolve/tests/test_iterative.py

## Tożsamość
- **id_karty:** `REPO-TEST_ITERATIVE-29F5`
- **ścieżka:** `.python_packages/scipy/sparse/linalg/_isolve/tests/test_iterative.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.277`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/sparse/linalg/_isolve/tests/test_iterative.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.277 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Test functions for the sparse.linalg._isolve module

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Case, SingleTest, IterativeParams, TestQMR, TestGMRES
- **funkcje:** `_assert_success`, `solver`, `xp_case`, `case`, `test_maxiter`, `test_convergence`, `test_precond_dummy`, `test_precond_inverse`, `test_atol`, `test_zero_rhs`, `test_maxiter_worsening`, `_setup_random_system`, `test_x0_working`, `test_x0_equals_Mb`, `test_x0_solves_problem_exactly`, `test_show`, `test_positional_error`, `test_invalid_atol`, `test_nD`, `generate_tests`, `callback`, `inverse`, `rinverse`, `matvec`, `rmatvec`, `cb`, `test_leftright_precond`, `test_basic`, `test_callback`, `test_abi`

## Opis
Test functions for the sparse.linalg._isolve module
