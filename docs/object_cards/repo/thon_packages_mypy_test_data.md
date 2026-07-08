# data.py — .python_packages/mypy/test/data.py

## Tożsamość
- **id_karty:** `REPO-DATA-23FA`
- **ścieżka:** `.python_packages/mypy/test/data.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.437`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/data.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.437 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Utilities for processing .test files containing test case descriptions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UpdateFile, DeleteFile, DataDrivenTestCase, TestItem, DataSuiteCollector, DataFileFix, DataFileCollector, DataSuite
- **funkcje:** `_file_arg_to_module`, `parse_test_case`, `module_from_path`, `parse_test_data`, `strip_list`, `collapse_line_continuation`, `expand_variables`, `expand_errors`, `fix_win_path`, `fix_cobertura_filename`, `pytest_sessionstart`, `pytest_addoption`, `pytest_cmdline_main`, `pytest_pycollect_makeitem`, `split_test_cases`, `add_test_name_suffix`, `is_incremental`, `has_stable_flags`, `_case_fail`, `runtest`, `setup`, `teardown`, `reportinfo`, `repr_failure`, `find_steps`, `trimmed_newlines`, `collect`, `from_parent`, `collect`, `setup`

## Opis
Utilities for processing .test files containing test case descriptions.
