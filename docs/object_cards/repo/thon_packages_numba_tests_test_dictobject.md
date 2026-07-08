# test_dictobject.py — .python_packages/numba/tests/test_dictobject.py

## Tożsamość
- **id_karty:** `REPO-TEST_DICTOBJECT-A74B`
- **ścieżka:** `.python_packages/numba/tests/test_dictobject.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.277`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_dictobject.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.277 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Testing numba implementation of the numba dictionary.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestDictObject, TestDictTypeCasting, TestTypedDict, DictIterableCtor, TestDictIterableCtorJit, TestDictIterableCtorNoJit, TestDictRefctTypes, TestDictForbiddenTypes, TestDictInferred, TestNonCompiledInfer, Bag, TestDictWithJitclass, TestNoJit, TestDictIterator, TestTypedDictInitialValues, TestLiteralStrKeyDict
- **funkcje:** `test_dict_bool`, `test_dict_create`, `test_dict_get`, `test_dict_get_with_default`, `test_dict_getitem`, `test_dict_popitem`, `test_dict_popitem_many`, `test_dict_pop`, `test_dict_pop_many`, `test_dict_delitem`, `test_dict_clear`, `test_dict_items`, `test_dict_keys`, `test_dict_keys_len`, `test_dict_values`, `test_dict_values_len`, `test_dict_items_len`, `test_dict_iter`, `test_dict_contains`, `test_dict_copy`, `test_dict_setdefault`, `test_dict_equality`, `test_dict_equality_more`, `test_dict_equality_diff_type`, `test_dict_to_from_meminfo`, `test_001_cannot_downcast_key`, `test_002_cannot_downcast_default`, `test_003_cannot_downcast_key`, `test_004_cannot_downcast_key`, `test_005_cannot_downcast_value`

## Opis
Testing numba implementation of the numba dictionary.

The tests here only check that the numba typing and codegen are working
correctly.  Detailed testing of the underlying dictionary operations is done
in test_dictimpl.py.
