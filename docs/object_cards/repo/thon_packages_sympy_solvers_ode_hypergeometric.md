# hypergeometric.py — .python_packages/sympy/solvers/ode/hypergeometric.py

## Tożsamość
- **id_karty:** `REPO-HYPERGEOMETRIC-5DAD`
- **ścieżka:** `.python_packages/sympy/solvers/ode/hypergeometric.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.351`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/solvers/ode/hypergeometric.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.351 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
This module contains the implementation of the 2nd_hypergeometric hint for

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `match_2nd_hypergeometric`, `equivalence_hypergeometric`, `match_2nd_2F1_hypergeometric`, `equivalence`, `get_sol_2F1_hypergeometric`, `_power_counting`

## Opis
This module contains the implementation of the 2nd_hypergeometric hint for
dsolve. This is an incomplete implementation of the algorithm described in [1].
The algorithm solves 2nd order linear ODEs of the form

.. math:: y'' + A(x) y' + B(x) y = 0\text{,}

where `A` and `B` are rational functions. The algorithm should find any
solution of the form

.. math:: y = P(x) _pF_q(..; ..;\frac{\alpha x^k
