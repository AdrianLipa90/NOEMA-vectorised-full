# domainmatrix.py — .python_packages/sympy/polys/matrices/domainmatrix.py

## Tożsamość
- **id_karty:** `REPO-DOMAINMATRIX-B14A`
- **ścieżka:** `.python_packages/sympy/polys/matrices/domainmatrix.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.537`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/matrices/domainmatrix.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.537 |
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
Module for the DomainMatrix class.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DomainMatrix
- **funkcje:** `DM`, `_collect_factors`, `getitem_sympy`, `extract`, `from_rep`, `from_list`, `from_list_sympy`, `from_dict_sympy`, `from_Matrix`, `get_domain`, `choose_domain`, `copy`, `convert_to`, `to_sympy`, `to_field`, `to_sparse`, `to_dense`, `to_ddm`, `to_sdm`, `to_dfm`, `to_dfm_or_ddm`, `_unify_domain`, `_unify_fmt`, `unify`, `to_Matrix`, `to_list`, `to_list_flat`, `from_list_flat`, `to_flat_nz`, `from_flat_nz`

## Opis
Module for the DomainMatrix class.

A DomainMatrix represents a matrix with elements that are in a particular
Domain. Each DomainMatrix internally wraps a DDM which is used for the
lower-level operations. The idea is that the DomainMatrix class provides the
convenience routines for converting between Expr and the poly domains as well
as unifying matrices with different domains.
