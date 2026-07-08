# test_gdb_bindings.py — .python_packages/numba/tests/test_gdb_bindings.py

## Tożsamość
- **id_karty:** `REPO-TEST_GDB_BINDINGS-97DC`
- **ścieżka:** `.python_packages/numba/tests/test_gdb_bindings.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.992`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_gdb_bindings.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.992 |
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
Tests gdb bindings

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestGdbBindImpls, TestGdbBinding, TestGdbMisc, TestGdbExceptions
- **funkcje:** `impl_gdb_call`, `impl_gdb_call_w_bp`, `impl_gdb_split_init_and_break_w_parallel`, `test_gdb_cmd_lang_cpython_quick_impl`, `test_gdb_cmd_lang_nopython_quick_impl`, `test_gdb_cmd_lang_objmode_quick_impl`, `test_gdb_split_init_and_break_cpython_impl`, `test_gdb_split_init_and_break_nopython_impl`, `test_gdb_split_init_and_break_objmode_impl`, `test_gdb_split_init_and_break_w_parallel_cpython_impl`, `test_gdb_split_init_and_break_w_parallel_nopython_impl`, `test_gdb_split_init_and_break_w_parallel_objmode_impl`, `run_cmd`, `run_test_in_separate_process`, `_inject`, `generate`, `test_call_gdb_twice`, `test_call_gdb`, `kill`, `test_template`, `gen`, `check`, `use_globals`, `nop_compiler`, `impl`, `python_func`

## Opis
Tests gdb bindings
