# test_cython_abi.py — .python_packages/scipy/linalg/tests/test_cython_abi.py

## Tożsamość
- **id_karty:** `REPO-TEST_CYTHON_ABI-FA5B`
- **ścieżka:** `.python_packages/scipy/linalg/tests/test_cython_abi.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.208`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/linalg/tests/test_cython_abi.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.208 |
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
Regression test for the cython_blas / cython_lapack binary interface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_extract_capi`, `test_cython_blas_abi_stability`, `test_cython_lapack_abi_stability`

## Opis
Regression test for the cython_blas / cython_lapack binary interface.

The __pyx_capi__ dict of each module contains PyCapsule objects whose
*name* string encodes the C-level function signature that Cython checks
at import time when another module does ``cimport``.  Any change to
those strings is a binary incompatibility that breaks every downstream
package (e.g., scikit-learn, statsmodels) compil
