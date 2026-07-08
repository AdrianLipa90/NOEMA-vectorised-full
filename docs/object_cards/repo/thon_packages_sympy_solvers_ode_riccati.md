# riccati.py — .python_packages/sympy/solvers/ode/riccati.py

## Tożsamość
- **id_karty:** `REPO-RICCATI-5A99`
- **ścieżka:** `.python_packages/sympy/solvers/ode/riccati.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.126`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/solvers/ode/riccati.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.126 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
This module contains :py:meth:`~sympy.solvers.ode.riccati.solve_riccati`,

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `riccati_normal`, `riccati_inverse_normal`, `riccati_reduced`, `linsolve_dict`, `match_riccati`, `val_at_inf`, `check_necessary_conds`, `inverse_transform_poly`, `limit_at_inf`, `construct_c_case_1`, `construct_c_case_2`, `construct_c_case_3`, `construct_c`, `construct_d_case_4`, `construct_d_case_5`, `construct_d_case_6`, `construct_d`, `rational_laurent_series`, `compute_m_ybar`, `solve_aux_eq`, `remove_redundant_sols`, `get_gen_sol_from_part_sol`, `solve_riccati`

## Opis
This module contains :py:meth:`~sympy.solvers.ode.riccati.solve_riccati`,
a function which gives all rational particular solutions to first order
Riccati ODEs. A general first order Riccati ODE is given by -

.. math:: y' = b_0(x) + b_1(x)w + b_2(x)w^2

where `b_0, b_1` and `b_2` can be arbitrary rational functions of `x`
with `b_2 \ne 0`. When `b_2 = 0`, the equation is not a Riccati ODE
anymore
