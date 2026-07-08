# ode.py — .python_packages/sympy/solvers/ode/ode.py

## Tożsamość
- **id_karty:** `REPO-ODE-4894`
- **ścieżka:** `.python_packages/sympy/solvers/ode/ode.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.883`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/solvers/ode/ode.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.883 |
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
This module contains :py:meth:`~sympy.solvers.ode.dsolve` and different helper

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `get_numbered_constants`, `iter_numbered_constants`, `dsolve`, `_helper_simplify`, `solve_ics`, `classify_ode`, `classify_sysode`, `check_linear_2eq_order1`, `check_nonlinear_2eq_order1`, `check_nonlinear_2eq_order2`, `check_nonlinear_3eq_order1`, `check_nonlinear_3eq_order2`, `odesimp`, `ode_sol_simplicity`, `_extract_funcs`, `_get_constant_subexpressions`, `constantsimp`, `constant_renumber`, `_handle_Integral`, `homogeneous_order`, `ode_2nd_power_series_ordinary`, `ode_2nd_power_series_regular`, `_frobenius`, `_remove_redundant_solutions`, `_is_special_case_of`, `ode_1st_power_series`, `checkinfsol`, `sysode_linear_2eq_order1`, `_linear_2eq_order1_type6`, `_linear_2eq_order1_type7`

## Opis
This module contains :py:meth:`~sympy.solvers.ode.dsolve` and different helper
functions that it uses.

:py:meth:`~sympy.solvers.ode.dsolve` solves ordinary differential equations.
See the docstring on the various functions for their uses.  Note that partial
differential equations support is in ``pde.py``.  Note that hint functions
have docstrings describing their various methods, but they are int
