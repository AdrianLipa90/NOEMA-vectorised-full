# test_single.py — .python_packages/sympy/solvers/ode/tests/test_single.py

## Tożsamość
- **id_karty:** `REPO-TEST_SINGLE-BC08`
- **ścieżka:** `.python_packages/sympy/solvers/ode/tests/test_single.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.620`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/solvers/ode/tests/test_single.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.620 |
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
This File contains test functions for the individual hints used for solving ODEs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_add_example_keys`, `_ode_solver_test`, `_test_all_hints`, `_test_dummy_sol`, `_test_an_example`, `_test_particular_example`, `_test_all_examples_for_one_hint`, `test_SingleODESolver`, `test_linear_coefficients`, `test_1st_homogeneous_coeff_ode`, `test_slow_examples_1st_homogeneous_coeff_ode`, `test_nth_linear_constant_coeff_homogeneous`, `test_slow_examples_nth_linear_constant_coeff_homogeneous`, `test_Airy_equation`, `test_lie_group`, `test_separable_reduced`, `test_slow_examples_separable_reduced`, `test_2nd_2F1_hypergeometric`, `test_2nd_2F1_hypergeometric_integral`, `test_2nd_nonlinear_autonomous_conserved`, `test_2nd_nonlinear_autonomous_conserved_integral`, `test_2nd_linear_bessel_equation`, `test_nth_algebraic`, `test_slow_examples_nth_linear_constant_coeff_var_of_parameters`, `test_nth_linear_constant_coeff_var_of_parameters`, `test_nth_linear_constant_coeff_variation_of_parameters__integral`, `test_slow_examples_1st_exact`, `test_1st_exact`, `test_1st_exact_integral`, `test_slow_examples_nth_order_reducible`

## Opis
This File contains test functions for the individual hints used for solving ODEs.

Examples of each solver will be returned by _get_examples_ode_sol_name_of_solver.

Examples should have a key 'XFAIL' which stores the list of hints if they are
expected to fail for that hint.

Functions that are for internal use:

1) _ode_solver_test(ode_examples) - It takes a dictionary of examples returned by
