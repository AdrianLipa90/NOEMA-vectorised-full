# bezier.py — .python_packages/matplotlib/bezier.py

## Tożsamość
- **id_karty:** `REPO-BEZIER-AA74`
- **ścieżka:** `.python_packages/matplotlib/bezier.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.163`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/bezier.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.163 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
A module providing some utility functions regarding Bézier path manipulation.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NonIntersectingPathException, BezierSegment
- **funkcje:** `_quadratic_roots_in_01`, `_real_roots_in_01`, `_get_coeff_matrix`, `get_intersection`, `get_normal_points`, `_de_casteljau1`, `split_de_casteljau`, `find_bezier_t_intersecting_with_closedpath`, `split_bezier_intersecting_with_closedpath`, `split_path_inout`, `inside_circle`, `get_cos_sin`, `check_if_parallel`, `get_parallels`, `find_control_points`, `make_wedged_bezier2`, `_comb`, `point_at_t`, `control_points`, `dimension`, `degree`, `polynomial_coefficients`, `axis_aligned_extrema`, `_f`

## Opis
A module providing some utility functions regarding Bézier path manipulation.
