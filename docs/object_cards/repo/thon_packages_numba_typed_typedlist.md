# typedlist.py — .python_packages/numba/typed/typedlist.py

## Tożsamość
- **id_karty:** `REPO-TYPEDLIST-D3BA`
- **ścieżka:** `.python_packages/numba/typed/typedlist.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.098`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/typed/typedlist.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.098 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Python wrapper that connects CPython interpreter to the Numba typed-list.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _Sequence, List, Typer
- **funkcje:** `_make_list`, `_length`, `_allocated`, `_is_mutable`, `_make_mutable`, `_make_immutable`, `_append`, `_setitem`, `_getitem`, `_contains`, `_count`, `_pop`, `_delitem`, `_extend`, `_insert`, `_remove`, `_clear`, `_reverse`, `_copy`, `_eq`, `_ne`, `_lt`, `_le`, `_gt`, `_ge`, `_index`, `_sort`, `_from_meminfo_ptr`, `typedlist_empty`, `box_lsttype`

## Opis
Python wrapper that connects CPython interpreter to the Numba typed-list.

This is the code that is used when creating typed lists outside of a `@jit`
context and when returning a typed-list from a `@jit` decorated function. It
basically a Python class that has a Numba allocated typed-list under the hood
and uses `@jit` functions to access it. Since it inherits from MutableSequence
it should reall
