# nonhomogeneous.py — .python_packages/sympy/solvers/ode/nonhomogeneous.py

## Tożsamość
- **id_karty:** `REPO-NONHOMOGENEOUS-CD7A`
- **ścieżka:** `.python_packages/sympy/solvers/ode/nonhomogeneous.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.562`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/solvers/ode/nonhomogeneous.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.562 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
This File contains helper functions for nth_linear_constant_coeff_undetermined_coefficients,

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_test_term`, `_get_euler_characteristic_eq_sols`, `_solve_variation_of_parameters`, `_get_const_characteristic_eq_sols`, `_get_simplified_sol`, `_undetermined_coefficients_match`, `_solve_undetermined_coefficients`, `_test_term`, `_get_trial_set`, `is_homogeneous_solution`, `_remove_coefficient`

## Opis
This File contains helper functions for nth_linear_constant_coeff_undetermined_coefficients,
nth_linear_euler_eq_nonhomogeneous_undetermined_coefficients,
nth_linear_constant_coeff_variation_of_parameters,
and nth_linear_euler_eq_nonhomogeneous_variation_of_parameters.

All the functions in this file are used by more than one solvers so, instead of creating
instances in other classes for using the
