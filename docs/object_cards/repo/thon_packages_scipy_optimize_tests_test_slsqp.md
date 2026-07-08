# test_slsqp.py — .python_packages/scipy/optimize/tests/test_slsqp.py

## Tożsamość
- **id_karty:** `REPO-TEST_SLSQP-D662`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test_slsqp.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.897`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test_slsqp.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.897 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Unit test for SLSQP optimization.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MyCallBack, TestSLSQP, NestedProblem
- **funkcje:** `test_slsqp_segfault_wrong_workspace_computation`, `callback2`, `callback3`, `setup_method`, `fun`, `jac`, `fun_and_jac`, `f_eqcon`, `fprime_eqcon`, `f_eqcon_scalar`, `fprime_eqcon_scalar`, `f_ieqcon`, `fprime_ieqcon`, `f_ieqcon2`, `fprime_ieqcon2`, `test_minimize_unbounded_approximated`, `test_minimize_unbounded_given`, `test_minimize_bounded_approximated`, `test_minimize_unbounded_combined`, `test_minimize_equality_approximated`, `test_minimize_equality_given`, `test_minimize_equality_given2`, `test_minimize_equality_given_cons_scalar`, `test_minimize_inequality_given`, `test_minimize_inequality_given_vector_constraints`, `test_minimize_bounded_constraint`, `test_minimize_bound_equality_given2`, `test_unbounded_approximated`, `test_unbounded_given`, `test_equality_approximated`

## Opis
Unit test for SLSQP optimization.
