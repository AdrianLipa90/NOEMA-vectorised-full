# point.py — .python_packages/sympy/geometry/point.py

## Tożsamość
- **id_karty:** `REPO-POINT-5B76`
- **ścieżka:** `.python_packages/sympy/geometry/point.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.895`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/geometry/point.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.895 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Geometrical Points.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Point, Point2D, Point3D
- **funkcje:** `_normalize_dimension`, `affine_rank`, `ambient_dimension`, `are_coplanar`, `distance`, `dot`, `equals`, `_eval_evalf`, `intersection`, `is_collinear`, `is_concyclic`, `is_nonzero`, `is_scalar_multiple`, `is_zero`, `length`, `midpoint`, `origin`, `orthogonal_direction`, `project`, `taxicab_distance`, `canberra_distance`, `unit`, `bounds`, `rotate`, `scale`, `transform`, `translate`, `coordinates`, `x`, `y`

## Opis
Geometrical Points.

Contains
========
Point
Point2D
Point3D

When methods of Point require 1 or more points as arguments, they
can be passed as a sequence of coordinates or Points:

>>> from sympy import Point
>>> Point(1, 1).is_collinear((2, 2), (3, 4))
False
>>> Point(1, 1).is_collinear(Point(2, 2), Point(3, 4))
False
