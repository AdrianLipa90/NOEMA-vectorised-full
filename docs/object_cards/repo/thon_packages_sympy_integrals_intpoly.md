# intpoly.py — .python_packages/sympy/integrals/intpoly.py

## Tożsamość
- **id_karty:** `REPO-INTPOLY-515E`
- **ścieżka:** `.python_packages/sympy/integrals/intpoly.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.721`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/integrals/intpoly.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.721 |
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
Module to implement integration of uni/bivariate polynomials over

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `polytope_integrate`, `strip`, `_polynomial_integrate`, `main_integrate3d`, `main_integrate`, `polygon_integrate`, `distance_to_side`, `lineseg_integrate`, `integration_reduction`, `left_integral2D`, `integration_reduction_dynamic`, `left_integral3D`, `gradient_terms`, `hyperplane_parameters`, `cross_product`, `best_origin`, `decompose`, `point_sort`, `norm`, `intersection`, `is_vertex`, `plot_polytope`, `plot_polynomial`, `x_axis_cut`, `y_axis_cut`, `compare`, `compare3d`

## Opis
Module to implement integration of uni/bivariate polynomials over
2D Polytopes and uni/bi/trivariate polynomials over 3D Polytopes.

Uses evaluation techniques as described in Chin et al. (2015) [1].


References
===========

.. [1] Chin, Eric B., Jean B. Lasserre, and N. Sukumar. "Numerical integration
of homogeneous functions on convex and nonconvex polygons and polyhedra."
Computational Mechani
