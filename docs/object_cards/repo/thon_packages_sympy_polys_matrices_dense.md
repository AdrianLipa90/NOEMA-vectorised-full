# dense.py — .python_packages/sympy/polys/matrices/dense.py

## Tożsamość
- **id_karty:** `REPO-DENSE-EBCB`
- **ścieżka:** `.python_packages/sympy/polys/matrices/dense.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.464`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/matrices/dense.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.464 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Module for the ddm_* routines for operating on a matrix in list of lists

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `ddm_transpose`, `ddm_iadd`, `ddm_isub`, `ddm_ineg`, `ddm_imul`, `ddm_irmul`, `ddm_imatmul`, `ddm_irref`, `ddm_irref_den`, `ddm_idet`, `ddm_iinv`, `ddm_ilu_split`, `ddm_ilu`, `ddm_ilu_solve`, `ddm_berk`

## Opis
Module for the ddm_* routines for operating on a matrix in list of lists
matrix representation.

These routines are used internally by the DDM class which also provides a
friendlier interface for them. The idea here is to implement core matrix
routines in a way that can be applied to any simple list representation
without the need to use any particular matrix class. For example we can
compute the
