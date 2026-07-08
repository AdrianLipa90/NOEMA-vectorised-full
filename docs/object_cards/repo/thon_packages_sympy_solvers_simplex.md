# simplex.py — .python_packages/sympy/solvers/simplex.py

## Tożsamość
- **id_karty:** `REPO-SIMPLEX-ACD7`
- **ścieżka:** `.python_packages/sympy/solvers/simplex.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.175`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/solvers/simplex.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.175 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Tools for optimizing a linear function for a given simplex.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UnboundedLPError, InfeasibleLPError
- **funkcje:** `_pivot`, `_choose_pivot_row`, `_simplex`, `_abcd`, `_m`, `_primal_dual`, `_rel_as_nonpos`, `_lp_matrices`, `_lp`, `lpmin`, `lpmax`, `_handle_bounds`, `linprog`, `show_linprog`, `aslist`, `ineq`, `_make_list`

## Opis
Tools for optimizing a linear function for a given simplex.

For the linear objective function ``f`` with linear constraints
expressed using `Le`, `Ge` or `Eq` can be found with ``lpmin`` or
``lpmax``. The symbols are **unbounded** unless specifically
constrained.

As an alternative, the matrices describing the objective and the
constraints, and an optional list of bounds can be passed to
``linpro
