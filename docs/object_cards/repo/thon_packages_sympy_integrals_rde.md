# rde.py — .python_packages/sympy/integrals/rde.py

## Tożsamość
- **id_karty:** `REPO-RDE-0133`
- **ścieżka:** `.python_packages/sympy/integrals/rde.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.682`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/integrals/rde.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.682 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Algorithms for solving the Risch differential equation.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `order_at`, `order_at_oo`, `weak_normalizer`, `normal_denom`, `special_denom`, `bound_degree`, `spde`, `no_cancel_b_large`, `no_cancel_b_small`, `no_cancel_equal`, `cancel_primitive`, `cancel_exp`, `solve_poly_rde`, `rischDE`

## Opis
Algorithms for solving the Risch differential equation.

Given a differential field K of characteristic 0 that is a simple
monomial extension of a base field k and f, g in K, the Risch
Differential Equation problem is to decide if there exist y in K such
that Dy + f*y == g and to find one if there are some.  If t is a
monomial over k and the coefficients of f and g are in k(t), then y is
in k(t),
