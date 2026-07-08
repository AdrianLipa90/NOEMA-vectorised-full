# testtypes.py — .python_packages/mypy/test/testtypes.py

## Tożsamość
- **id_karty:** `REPO-TESTTYPES-2DAF`
- **ścieżka:** `.python_packages/mypy/test/testtypes.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.523`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/testtypes.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.523 |
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
Test cases for mypy types and type operations.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypesSuite, TypeOpsSuite, JoinSuite, MeetSuite, SameTypeSuite, RemoveLastKnownValueSuite, ShallowOverloadMatchingSuite, TestExpandTypeLimitGetProperType
- **funkcje:** `make_call`, `setUp`, `test_any`, `test_simple_unbound_type`, `test_generic_unbound_type`, `test_callable_type`, `test_callable_type_with_default_args`, `test_callable_type_with_var_args`, `test_tuple_type_str`, `test_type_variable_binding`, `test_generic_function_type`, `test_type_alias_expand_once`, `test_recursive_nested_in_non_recursive`, `test_indirection_no_infinite_recursion`, `setUp`, `test_trivial_expand`, `test_trivial_expand_recursive`, `test_expand_naked_type_var`, `test_expand_basic_generic_types`, `assert_expand`, `test_trivial_erase`, `test_erase_with_type_variable`, `test_erase_with_generic_type`, `test_erase_with_generic_type_recursive`, `test_erase_with_tuple_type`, `test_erase_with_function_type`, `test_erase_with_type_object`, `test_erase_with_type_type`, `assert_erase`, `test_is_more_precise`

## Opis
Test cases for mypy types and type operations.
