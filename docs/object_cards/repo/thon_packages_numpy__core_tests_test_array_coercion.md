# test_array_coercion.py — .python_packages/numpy/_core/tests/test_array_coercion.py

## Tożsamość
- **id_karty:** `REPO-TEST_ARRAY_COERCION-DDF9`
- **ścieżka:** `.python_packages/numpy/_core/tests/test_array_coercion.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.848`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/_core/tests/test_array_coercion.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.848 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Tests for array coercion, mainly through testing `np.array` results directly.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestStringDiscovery, TestScalarDiscovery, TestTimeScalars, TestNested, TestBadSequences, TestArrayLikes, TestAsArray, TestSpecialAttributeLookupFailure, MyArr, _SequenceLike, ArrayDunder, ArrayInterface, ArrayStruct, WeirdArrayLike, WeirdArrayInterface, MyScalar, mylist, mylist, baditem, ArraySubclass
- **funkcje:** `arraylikes`, `scalar_instances`, `is_parametric_dtype`, `test_subarray_from_array_construction`, `test_empty_string`, `test_string_to_float_coercion_errors`, `ndarray`, `subclass`, `test_basic_stringlength`, `test_nested_arrays_stringlength`, `test_unpack_first_level`, `test_void_special_case`, `test_char_special_case`, `test_char_special_case_deep`, `test_unknown_object`, `test_scalar`, `test_scalar_promotion`, `test_scalar_coercion`, `test_scalar_coercion_same_as_cast_and_assignment`, `test_pyscalar_subclasses`, `test_default_dtype_instance`, `test_scalar_to_int_coerce_does_not_cast`, `test_coercion_basic`, `test_coercion_timedelta_convert_to_number`, `test_coercion_assignment_datetime`, `test_coercion_assignment_timedelta`, `test_nested_simple`, `test_pathological_self_containing`, `test_nested_arraylikes`, `test_uneven_depth_ragged`

## Opis
Tests for array coercion, mainly through testing `np.array` results directly.
Note that other such tests exist, e.g., in `test_api.py` and many corner-cases
are tested (sometimes indirectly) elsewhere.
