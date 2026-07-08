# test_hashing.py — .python_packages/numba/tests/test_hashing.py

## Tożsamość
- **id_karty:** `REPO-TEST_HASHING-17F6`
- **ścieżka:** `.python_packages/numba/tests/test_hashing.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.120`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_hashing.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.120 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Test hashing of various supported types.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestHashingSetup, TestHashAlgs, BaseTest, TestNumberHashing, TestTupleHashing, TestUnicodeHashing, TestUnhashable
- **funkcje:** `hash_usecase`, `test_warn_on_fnv`, `get_expected_hash`, `get_hash_command`, `get_hash`, `test_against_cpython_gold`, `setUp`, `check_hash_values`, `int_samples`, `safe_construct`, `float_samples`, `complex_samples`, `setUp`, `tearDown`, `check_floats`, `check_complex`, `test_floats`, `test_complex`, `test_bool`, `test_ints`, `test_py310_nan_hash`, `setUp`, `tearDown`, `check_tuples`, `test_homogeneous_tuples`, `test_heterogeneous_tuples`, `test_basic_unicode`, `test_hash_passthrough`, `test_hash_passthrough_call`, `test_hash_literal`

## Opis
Test hashing of various supported types.
