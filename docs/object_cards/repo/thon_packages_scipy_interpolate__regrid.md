# _regrid.py — .python_packages/scipy/interpolate/_regrid.py

## Tożsamość
- **id_karty:** `REPO-_REGRID-4243`
- **ścieżka:** `.python_packages/scipy/interpolate/_regrid.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.906`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/interpolate/_regrid.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.906 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
Regrid (2-D smoothing B-splines via separable 1-D FITPACK kernels)

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PackedMatrix, F
- **funkcje:** `_ndbspline_call_like_bivariate`, `return_NdBSpline`, `_stack_augmented_fitpack`, `_solve_2d_fitpack`, `_p_search_hit_s`, `_apply_bbox_grid`, `_build_design_matrices`, `_initialise_knots`, `_add_knots`, `_regrid_fitpack`, `_regrid`, `shape`, `todense`, `tocsr`, `g`

## Opis
Regrid (2-D smoothing B-splines via separable 1-D FITPACK kernels)
==================================================================

1) Overview
-----------
This module fits a bivariate tensor-product B-spline surface to gridded data
`Z[i, j]` sampled on strictly increasing coordinates `x[i]`, `y[j]`. It mirrors
the adaptive spirit of FITPACK's REGRID/fpgrre (knot growth + smoothing
parameter se
