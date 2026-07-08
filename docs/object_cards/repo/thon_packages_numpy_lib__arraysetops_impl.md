# _arraysetops_impl.py — .python_packages/numpy/lib/_arraysetops_impl.py

## Tożsamość
- **id_karty:** `REPO-_ARRAYSETOPS_IMPL-9FA6`
- **ścieżka:** `.python_packages/numpy/lib/_arraysetops_impl.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.370`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/lib/_arraysetops_impl.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.370 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
Set operations for arrays based on sorting.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UniqueAllResult, UniqueCountsResult, UniqueInverseResult
- **funkcje:** `_ediff1d_dispatcher`, `ediff1d`, `_unpack_tuple`, `_unique_dispatcher`, `unique`, `_unique1d`, `_unique_all_dispatcher`, `unique_all`, `_unique_counts_dispatcher`, `unique_counts`, `_unique_inverse_dispatcher`, `unique_inverse`, `_unique_values_dispatcher`, `unique_values`, `_intersect1d_dispatcher`, `intersect1d`, `_setxor1d_dispatcher`, `setxor1d`, `_isin`, `_isin_dispatcher`, `isin`, `_union1d_dispatcher`, `union1d`, `_setdiff1d_dispatcher`, `setdiff1d`, `reshape_uniq`

## Opis
Set operations for arrays based on sorting.

Notes
-----

For floating point arrays, inaccurate results may appear due to usual round-off
and floating point comparison issues.

Speed could be gained in some operations by an implementation of
`numpy.sort`, that can provide directly the permutation vectors, thus avoiding
calls to `numpy.argsort`.

Original author: Robert Cimrman
