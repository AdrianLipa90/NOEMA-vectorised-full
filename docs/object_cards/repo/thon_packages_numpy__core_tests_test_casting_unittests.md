# test_casting_unittests.py — .python_packages/numpy/_core/tests/test_casting_unittests.py

## Tożsamość
- **id_karty:** `REPO-TEST_CASTING_UNITTES-CFF8`
- **ścieżka:** `.python_packages/numpy/_core/tests/test_casting_unittests.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.340`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/_core/tests/test_casting_unittests.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.340 |
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
The tests exercise the casting machinery in a more low-level manner.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Casting, TestChanges, TestCasting
- **funkcje:** `simple_dtype_instances`, `get_expected_stringlength`, `_get_cancast_table`, `test_float_to_string`, `test_to_void`, `get_data`, `get_data_variation`, `test_simple_cancast`, `test_simple_direct_casts`, `test_numeric_to_times`, `test_time_to_time`, `string_with_modified_length`, `test_string_cancast`, `test_simple_string_casts_roundtrip`, `test_string_to_string_cancast`, `test_unicode_byteswapped_cast`, `test_void_to_string_special_case`, `test_object_to_parametric_internal_error`, `test_object_and_simple_resolution`, `test_simple_to_object_resolution`, `test_void_and_structured_with_subarray`, `test_structured_field_offsets`, `test_structured_view_offsets_parametric`, `test_object_casts_NULL_None_equivalence`, `test_nonstandard_bool_to_other`, `test_same_value_overflow`, `test_same_value_float_to_int`, `test_same_value_float_to_int_scalar`, `test_same_value_naninf`, `test_same_value_complex`

## Opis
The tests exercise the casting machinery in a more low-level manner.
The reason is mostly to test a new implementation of the casting machinery.

Unlike most tests in NumPy, these are closer to unit-tests rather
than integration tests.
