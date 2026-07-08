# test_listobject.py — .python_packages/numba/tests/test_listobject.py

## Tożsamość
- **id_karty:** `REPO-TEST_LISTOBJECT-4B6E`
- **ścieżka:** `.python_packages/numba/tests/test_listobject.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.276`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_listobject.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.276 |
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
Tests for the compiler components of the Numba typed-list.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestCreateAppendLength, TestBool, TestAllocation, TestToFromMeminfo, TestGetitem, TestGetitemSlice, TestSetitem, TestPop, TestListObjectDelitem, TestContains, TestCount, TestExtend, TestInsert, TestRemove, TestClear, TestReverse, TestCopy, TestIndex, TestEqualNotEqual, TestIter
- **funkcje:** `make_test_list`, `test_list_create`, `test_list_create_no_jit`, `test_nonempty_list_create_no_jit`, `test_list_bool`, `test_list_allocation`, `test_list_allocation_negative`, `test_list_to_from_meminfo`, `test_list_getitem_singleton`, `test_list_getitem_singleton_negtive_index`, `test_list_getitem_multiple`, `test_list_getitem_empty_index_error`, `test_list_getitem_multiple_index_error`, `test_list_getitem_empty_typing_error`, `test_list_getitem_integer_types_as_index`, `test_list_getitem_different_sized_uint_index`, `test_list_getitem_different_sized_int_index`, `test_list_getitem_empty_slice_defaults`, `test_list_getitem_singleton_slice_defaults`, `test_list_getitem_multiple_slice_defaults`, `test_list_getitem_multiple_slice_pos_start`, `test_list_getitem_multiple_slice_pos_stop`, `test_list_getitem_multiple_slice_pos_start_pos_stop`, `test_list_getitem_multiple_slice_pos_start_pos_stop_pos_step`, `test_list_getitem_multiple_slice_neg_start`, `test_list_getitem_multiple_slice_neg_stop`, `test_list_getitem_multiple_slice_neg_step`, `test_list_getitem_multiple_slice_pos_start_neg_step`, `test_list_getitem_multiple_slice_neg_start_neg_step`, `test_list_getitem_multiple_slice_pos_stop_neg_step`

## Opis
Tests for the compiler components of the Numba typed-list.

The tests here should exercise everything within an `@njit` context.
Importantly, the tests should not return a typed list from within such a
context as this would require code from numba/typed/typedlist.py (this is
tested separately).  Tests in this file build on each other in the order of
writing. For example, the first test, tests the
