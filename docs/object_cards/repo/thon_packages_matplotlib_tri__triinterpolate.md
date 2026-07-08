# _triinterpolate.py — .python_packages/matplotlib/tri/_triinterpolate.py

## Tożsamość
- **id_karty:** `REPO-_TRIINTERPOLATE-D01A`
- **ścieżka:** `.python_packages/matplotlib/tri/_triinterpolate.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.975`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/tri/_triinterpolate.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.975 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Interpolation inside triangular grids.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TriInterpolator, LinearTriInterpolator, CubicTriInterpolator, _ReducedHCT_Element, _DOF_estimator, _DOF_estimator_user, _DOF_estimator_geom, _DOF_estimator_min_E, _Sparse_Matrix_coo
- **funkcje:** `_cg`, `_safe_inv22_vectorized`, `_pseudo_inv22sym_vectorized`, `_scalar_vectorized`, `_transpose_vectorized`, `_roll_vectorized`, `_to_matrix_vectorized`, `_extract_submatrices`, `_interpolate_multikeys`, `_interpolate_single_key`, `gradient`, `_interpolate_single_key`, `gradient`, `_interpolate_single_key`, `_compute_dof`, `_get_alpha_vec`, `_get_jacobian`, `_compute_tri_eccentricities`, `get_function_values`, `get_function_derivatives`, `get_function_hessians`, `get_d2Sidksij2`, `get_bending_matrices`, `get_Hrot_from_J`, `get_Kff_and_Ff`, `compute_dz`, `compute_dof_from_df`, `get_dof_vec`, `compute_dz`, `compute_dz`

## Opis
Interpolation inside triangular grids.
