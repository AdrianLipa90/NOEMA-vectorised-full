# __init__.py — .python_packages/scipy/sparse/linalg/_eigen/arpack/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-FA47`
- **ścieżka:** `.python_packages/scipy/sparse/linalg/_eigen/arpack/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.045`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/sparse/linalg/_eigen/arpack/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.045 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
Eigenvalue solver using iterative methods.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
Eigenvalue solver using iterative methods.

Find k eigenvectors and eigenvalues of a matrix A using the
Arnoldi/Lanczos iterative methods from ARPACK [1]_,[2]_.

These methods are most useful for large sparse matrices.

  - eigs(A,k)
  - eigsh(A,k)

References
----------
.. [1] ARPACK Software, http://www.caam.rice.edu/software/ARPACK/
.. [2] R. B. Lehoucq, D. C. Sorensen, and C. Yang,  ARPACK USE
