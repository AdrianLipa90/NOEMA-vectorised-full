# test_codegen.py — .python_packages/numba/tests/test_codegen.py

## Tożsamość
- **id_karty:** `REPO-TEST_CODEGEN-47F4`
- **ścieżka:** `.python_packages/numba/tests/test_codegen.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.577`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_codegen.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.577 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Tests for numba.core.codegen.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** JITCPUCodegenTestCase, TestWrappers
- **funkcje:** `setUp`, `tearDown`, `compile_module`, `_check_unserialize_sum`, `test_get_pointer_to_function`, `test_magic_tuple`, `_check_serialize_unserialize`, `_check_unserialize_other_process`, `test_serialize_unserialize_bitcode`, `test_unserialize_other_process_bitcode`, `test_serialize_unserialize_object_code`, `test_unserialize_other_process_object_code`, `test_cache_disabled_inspection`, `test_library_lifetime`, `test_noinline_on_main_call`, `foo`

## Opis
Tests for numba.core.codegen.
