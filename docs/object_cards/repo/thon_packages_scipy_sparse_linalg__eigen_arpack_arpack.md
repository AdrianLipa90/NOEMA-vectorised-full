# arpack.py — .python_packages/scipy/sparse/linalg/_eigen/arpack/arpack.py

## Tożsamość
- **id_karty:** `REPO-ARPACK-E056`
- **ścieżka:** `.python_packages/scipy/sparse/linalg/_eigen/arpack/arpack.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.353`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/sparse/linalg/_eigen/arpack/arpack.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.353 |
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
Find a few eigenvectors and eigenvalues of a matrix.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ArpackError, ArpackNoConvergence, _ArpackParams, _SymmetricArpackParams, _UnsymmetricArpackParams, SpLuInv, LuInv, IterInv, IterOpInv
- **funkcje:** `choose_ncv`, `gmres_loose`, `_fast_spmatrix_to_csc`, `get_inv_matvec`, `get_OPinv_matvec`, `eigs`, `eigsh`, `_raise_no_convergence`, `iterate`, `extract`, `iterate`, `extract`, `_matvec`, `_matvec`, `_matvec`, `_matvec`, `mult_func`, `mult_func_M_None`

## Opis
Find a few eigenvectors and eigenvalues of a matrix.


Uses ARPACK: https://github.com/opencollab/arpack-ng
