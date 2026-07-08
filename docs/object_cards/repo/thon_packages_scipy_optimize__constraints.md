# _constraints.py — .python_packages/scipy/optimize/_constraints.py

## Tożsamość
- **id_karty:** `REPO-_CONSTRAINTS-292C`
- **ścieżka:** `.python_packages/scipy/optimize/_constraints.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.050`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_constraints.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.050 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Constraints definition for minimize.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NonlinearConstraint, LinearConstraint, Bounds, PreparedConstraint
- **funkcje:** `_arr_to_scalar`, `new_bounds_to_old`, `old_bound_to_new`, `strict_bounds`, `new_constraint_to_old`, `old_constraint_to_new`, `_input_validation`, `residual`, `_input_validation`, `residual`, `violation`, `fun`, `jac`, `f_eq`, `f_ineq`, `fun`, `j_eq`, `j_ineq`, `jac`

## Opis
Constraints definition for minimize.
