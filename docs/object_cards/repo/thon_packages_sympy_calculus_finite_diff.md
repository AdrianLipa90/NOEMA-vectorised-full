# finite_diff.py — .python_packages/sympy/calculus/finite_diff.py

## Tożsamość
- **id_karty:** `REPO-FINITE_DIFF-E59F`
- **ścieżka:** `.python_packages/sympy/calculus/finite_diff.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.398`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/calculus/finite_diff.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.398 |
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
Finite difference weights

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `finite_diff_weights`, `apply_finite_diff`, `_as_finite_diff`, `differentiate_finite`

## Opis
Finite difference weights
=========================

This module implements an algorithm for efficient generation of finite
difference weights for ordinary differentials of functions for
derivatives from 0 (interpolation) up to arbitrary order.

The core algorithm is provided in the finite difference weight generating
function (``finite_diff_weights``), and two convenience functions are provided
f
