# _rotation_xp.py — .python_packages/scipy/spatial/transform/_rotation_xp.py

## Tożsamość
- **id_karty:** `REPO-_ROTATION_XP-09F1`
- **ścieżka:** `.python_packages/scipy/spatial/transform/_rotation_xp.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.505`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/spatial/transform/_rotation_xp.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.505 |
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
Array API backend for the `Rotation` class.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `from_quat`, `from_matrix`, `_from_matrix_orthogonal`, `from_rotvec`, `from_mrp`, `from_euler`, `from_davenport`, `as_quat`, `as_matrix`, `as_rotvec`, `as_mrp`, `as_euler`, `as_davenport`, `inv`, `magnitude`, `approx_equal`, `mean`, `reduce`, `apply`, `setitem`, `align_vectors`, `_align_vectors`, `_align_vectors_fixed`, `pow`, `_normalize_quaternion`, `_quat_canonical`, `_elementary_basis_index`, `_compute_davenport_from_quat`, `_elementary_quat_compose`, `_make_elementary_quat`

## Opis
Array API backend for the `Rotation` class.

This module provides generic, functional implementations of the `Rotation` class methods
that work with any Array API-compatible backend.
