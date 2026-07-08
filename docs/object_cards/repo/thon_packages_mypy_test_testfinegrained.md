# testfinegrained.py — .python_packages/mypy/test/testfinegrained.py

## Tożsamość
- **id_karty:** `REPO-TESTFINEGRAINED-850E`
- **ścieżka:** `.python_packages/mypy/test/testfinegrained.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.856`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/testfinegrained.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.856 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
Test cases for fine-grained incremental checking.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FineGrainedSuite, TestMessageSorting
- **funkcje:** `normalize_messages`, `should_skip`, `run_case`, `get_options`, `run_check`, `build`, `format_triggered`, `get_build_steps`, `perform_step`, `parse_sources`, `maybe_suggest`, `maybe_inspect`, `get_suggest`, `get_inspect`, `test_simple_sorting`, `test_long_form_sorting`, `test_mypy_error_prefix`, `test_new_file_at_the_end`

## Opis
Test cases for fine-grained incremental checking.

Each test cases runs a batch build followed by one or more fine-grained
incremental steps. We verify that each step produces the expected output.

See the comment at the top of test-data/unit/fine-grained.test for more
information.

N.B.: Unlike most of the other test suites, testfinegrained does not
rely on an alt_lib_path for finding source file
