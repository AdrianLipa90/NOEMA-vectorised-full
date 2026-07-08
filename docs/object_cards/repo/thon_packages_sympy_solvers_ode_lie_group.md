# lie_group.py — .python_packages/sympy/solvers/ode/lie_group.py

## Tożsamość
- **id_karty:** `REPO-LIE_GROUP-C460`
- **ścieżka:** `.python_packages/sympy/solvers/ode/lie_group.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.802`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/solvers/ode/lie_group.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.802 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
This module contains the implementation of the internal helper functions for the lie_group hint for

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_ode_lie_group_try_heuristic`, `_ode_lie_group`, `infinitesimals`, `lie_heuristic_abaco1_simple`, `lie_heuristic_abaco1_product`, `lie_heuristic_bivariate`, `lie_heuristic_chi`, `lie_heuristic_function_sum`, `lie_heuristic_abaco2_similar`, `lie_heuristic_abaco2_unique_unknown`, `lie_heuristic_abaco2_unique_general`, `lie_heuristic_linear`, `_lie_group_remove`

## Opis
This module contains the implementation of the internal helper functions for the lie_group hint for
dsolve. These helper functions apply different heuristics on the given equation
and return the solution. These functions are used by :py:meth:`sympy.solvers.ode.single.LieGroup`

References
=========

- `abaco1_simple`, `function_sum` and `chi`  are referenced from E.S Cheb-Terrab, L.G.S Duarte
and
