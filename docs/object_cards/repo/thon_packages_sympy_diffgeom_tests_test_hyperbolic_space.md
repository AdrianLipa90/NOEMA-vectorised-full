# test_hyperbolic_space.py — .python_packages/sympy/diffgeom/tests/test_hyperbolic_space.py

## Tożsamość
- **id_karty:** `REPO-TEST_HYPERBOLIC_SPAC-C580`
- **ścieżka:** `.python_packages/sympy/diffgeom/tests/test_hyperbolic_space.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.567`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/diffgeom/tests/test_hyperbolic_space.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.567 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
unit test describing the hyperbolic half-plane with the Poincare metric. This

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `test_H2`

## Opis
unit test describing the hyperbolic half-plane with the Poincare metric. This
is a basic model of hyperbolic geometry on the (positive) half-space

{(x,y) \in R^2 | y > 0}

with the Riemannian metric

ds^2 = (dx^2 + dy^2)/y^2

It has constant negative scalar curvature = -2

https://en.wikipedia.org/wiki/Poincare_half-plane_model
