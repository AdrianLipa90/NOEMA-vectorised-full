# arrayobj.py — .python_packages/numba/np/arrayobj.py

## Tożsamość
- **id_karty:** `REPO-ARRAYOBJ-65E5`
- **ścieżka:** `.python_packages/numba/np/arrayobj.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.972`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/np/arrayobj.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.972 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
Implementation of operations on Array objects and objects supporting

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Indexer, EntireIndexer, IntegerIndexer, IntegerArrayIndexer, BooleanArrayIndexer, SliceIndexer, FancyIndexer, ArrayStruct, BaseSubIter, FlatSubIter, TrivialFlatSubIter, IndexedSubIter, ZeroDimSubIter, ScalarSubIter, NdIter, NdIndexIter, CContiguousFlatIter, FlatIter
- **funkcje:** `set_range_metadata`, `mark_positive`, `make_array`, `get_itemsize`, `load_item`, `store_item`, `fix_integer_index`, `normalize_index`, `normalize_indices`, `populate_array`, `update_array_info`, `normalize_axis`, `normalize_axis_overloads`, `normalize_axis_tuple`, `normalize_axis_tuple_overloads`, `getiter_array`, `_getitem_array_single_int`, `iternext_array`, `basic_indexing`, `make_view`, `_getitem_array_generic`, `getitem_arraynd_intp`, `getitem_array_tuple`, `setitem_array`, `array_len`, `array_item`, `fancy_getitem`, `fancy_getitem_array`, `offset_bounds_from_strides`, `compute_memory_extents`

## Opis
Implementation of operations on Array objects and objects supporting
the buffer protocol.
