# eigen_symmetric.py — .python_packages/mpmath/matrices/eigen_symmetric.py

## Tożsamość
- **id_karty:** `REPO-EIGEN_SYMMETRIC-8E3B`
- **ścieżka:** `.python_packages/mpmath/matrices/eigen_symmetric.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.270`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpmath/matrices/eigen_symmetric.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.270 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
The symmetric eigenvalue problem.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `r_sy_tridiag`, `c_he_tridiag_0`, `c_he_tridiag_1`, `c_he_tridiag_2`, `tridiag_eigen`, `eigsy`, `eighe`, `eigh`, `gauss_quadrature`, `svd_r_raw`, `svd_c_raw`, `svd_r`, `svd_c`, `svd`

## Opis
The symmetric eigenvalue problem.
---------------------------------

This file contains routines for the symmetric eigenvalue problem.

high level routines:

  eigsy : real symmetric (ordinary) eigenvalue problem
  eighe : complex hermitian (ordinary) eigenvalue problem
  eigh  : unified interface for eigsy and eighe
  svd_r : singular value decomposition for real matrices
  svd_c : singular value
