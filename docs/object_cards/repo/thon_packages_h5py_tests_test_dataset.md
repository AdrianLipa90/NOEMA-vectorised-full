# test_dataset.py — .python_packages/h5py/tests/test_dataset.py

## Tożsamość
- **id_karty:** `REPO-TEST_DATASET-CE60`
- **ścieżka:** `.python_packages/h5py/tests/test_dataset.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.481`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/h5py/tests/test_dataset.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.481 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Dataset testing operations.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** BaseDataset, TestRepr, TestCreateShape, TestCreateData, TestReadDirectly, TestWriteDirectly, TestCreateRequire, TestCreateChunked, TestCreateFillvalue, TestFillTime, TestCreateNamedType, TestCreateGzip, TestCreateCompressionNumber, TestCreateLZF, TestCreateSZIP, TestCreateShuffle, TestCreateFletcher32, TestCreateScaleOffset, TestExternal, TestAutoCreate
- **funkcje:** `test_get_unset_fill_value`, `test_get_chunk_details`, `test_chunk_iter`, `test_empty_shape`, `test_zero_storage_size`, `test_python_int_uint64`, `test_setitem_fancy_indexing`, `test_vlen_spacepad`, `test_vlen_nullterm`, `test_allow_unknown_filter`, `test_dset_chunk_cache`, `ds_str`, `ds_fields`, `test_array_copy`, `test_array_copy_false`, `test_array_dtype`, `test_array_scalar`, `test_array_nd`, `test_view_properties`, `test_concurrent_dataset_creation`, `test_filter_properties`, `test_store_refs`, `test_store_regionrefs`, `setUp`, `tearDown`, `test_repr_basic`, `test_repr_closed`, `test_repr_anonymous`, `test_create_scalar`, `test_create_simple`

## Opis
Dataset testing operations.

Tests all dataset operations, including creation, with the exception of:

1. Slicing operations for read and write, handled by module test_slicing
2. Type conversion for read and write (currently untested)
