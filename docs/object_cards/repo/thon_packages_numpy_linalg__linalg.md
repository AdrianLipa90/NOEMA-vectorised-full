# _linalg.py — .python_packages/numpy/linalg/_linalg.py

## Tożsamość
- **id_karty:** `REPO-_LINALG-D31C`
- **ścieżka:** `.python_packages/numpy/linalg/_linalg.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.385`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/linalg/_linalg.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.385 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
Lite version of scipy.linalg.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** EigResult, EighResult, QRResult, SlogdetResult, SVDResult, LinAlgError
- **funkcje:** `_raise_linalgerror_singular`, `_raise_linalgerror_nonposdef`, `_raise_linalgerror_eigenvalues_nonconvergence`, `_raise_linalgerror_svd_nonconvergence`, `_raise_linalgerror_lstsq`, `_raise_linalgerror_qr`, `_makearray`, `isComplexType`, `_realType`, `_complexType`, `_commonType`, `_to_native_byte_order`, `_assert_2d`, `_assert_stacked_2d`, `_assert_stacked_square`, `_assert_finite`, `_is_empty_2d`, `transpose`, `_tensorsolve_dispatcher`, `tensorsolve`, `_solve_dispatcher`, `solve`, `_tensorinv_dispatcher`, `tensorinv`, `_unary_dispatcher`, `inv`, `_matrix_power_dispatcher`, `matrix_power`, `_cholesky_dispatcher`, `cholesky`

## Opis
Lite version of scipy.linalg.

Notes
-----
This module is a lite version of the linalg.py module in SciPy which
contains high-level Python interface to the LAPACK library.  The lite
version only accesses the following LAPACK functions: dgesv, zgesv,
dgeev, zgeev, dgesdd, zgesdd, dgelsd, zgelsd, dsyevd, zheevd, dgetrf,
zgetrf, dpotrf, zpotrf, dgeqrf, zgeqrf, zungqr, dorgqr.
