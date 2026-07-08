# gdb_support.py — .python_packages/numba/tests/gdb_support.py

## Tożsamość
- **id_karty:** `REPO-GDB_SUPPORT-0ACC`
- **ścieżka:** `.python_packages/numba/tests/gdb_support.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.427`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/gdb_support.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.427 |
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
Helpers for running gdb related testing

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GdbMIDriver
- **funkcje:** `_drive`, `supports_python`, `supports_numpy`, `_captured_expect`, `assert_output`, `assert_regex_output`, `_run_command`, `run`, `cont`, `quit`, `next`, `step`, `set_breakpoint`, `check_hit_breakpoint`, `stack_list_arguments`, `stack_list_variables`, `interpreter_exec`, `_list_features_raw`, `list_features`

## Opis
Helpers for running gdb related testing
