# _linprog_rs.py — .python_packages/scipy/optimize/_linprog_rs.py

## Tożsamość
- **id_karty:** `REPO-_LINPROG_RS-F695`
- **ścieżka:** `.python_packages/scipy/optimize/_linprog_rs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.653`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_linprog_rs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.653 |
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
Revised simplex method for linear programming

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_phase_one`, `_get_more_basis_columns`, `_generate_auxiliary_problem`, `_select_singleton_columns`, `_find_nonzero_rows`, `_select_enter_pivot`, `_display_iter`, `_display_and_callback`, `_phase_two`, `_linprog_rs`

## Opis
Revised simplex method for linear programming

The *revised simplex* method uses the method described in [1]_, except
that a factorization [2]_ of the basis matrix, rather than its inverse,
is efficiently maintained and used to solve the linear systems at each
iteration of the algorithm.

.. versionadded:: 1.3.0

References
----------
.. [1] Bertsimas, Dimitris, and J. Tsitsiklis. "Introduction to
