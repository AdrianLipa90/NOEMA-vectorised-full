# lra_theory.py — .python_packages/sympy/logic/algorithms/lra_theory.py

## Tożsamość
- **id_karty:** `REPO-LRA_THEORY-1549`
- **ścieżka:** `.python_packages/sympy/logic/algorithms/lra_theory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.764`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/logic/algorithms/lra_theory.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.764 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
Implements "A Fast Linear-Arithmetic Solver for DPLL(T)"

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UnhandledInput, LRASolver, Boundary, LRARational, LRAVariable
- **funkcje:** `_sep_const_coeff`, `_list_terms`, `_sep_const_terms`, `_eval_binrel`, `from_encoded_cnf`, `reset_bounds`, `assert_lit`, `_assert_upper`, `_assert_lower`, `_update`, `check`, `_pivot_and_update`, `_pivot`, `from_upper`, `from_lower`, `get_negated`, `get_inequality`

## Opis
Implements "A Fast Linear-Arithmetic Solver for DPLL(T)"

The LRASolver class defined in this file can be used
in conjunction with a SAT solver to check the
satisfiability of formulas involving inequalities.

Here's an example of how that would work:

    Suppose you want to check the satisfiability of
    the following formula:

    >>> from sympy.core.relational import Eq
    >>> from sympy.abc
