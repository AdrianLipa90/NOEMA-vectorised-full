# index_methods.py — .python_packages/sympy/tensor/index_methods.py

## Tożsamość
- **id_karty:** `REPO-INDEX_METHODS-9344`
- **ścieżka:** `.python_packages/sympy/tensor/index_methods.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.899`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/tensor/index_methods.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.899 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
Module with functions operating on IndexedBase, Indexed and Idx objects

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** IndexConformanceException
- **funkcje:** `_unique_and_repeated`, `_remove_repeated`, `_get_indices_Mul`, `_get_indices_Pow`, `_get_indices_Add`, `get_indices`, `get_contraction_structure`

## Opis
Module with functions operating on IndexedBase, Indexed and Idx objects

- Check shape conformance
- Determine indices in resulting expression

etc.

Methods in this module could be implemented by calling methods on Expr
objects instead.  When things stabilize this could be a useful
refactoring.
