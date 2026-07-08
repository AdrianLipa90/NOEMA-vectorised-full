# runtests.py — .python_packages/sympy/testing/runtests.py

## Tożsamość
- **id_karty:** `REPO-RUNTESTS-7F1C`
- **ścieżka:** `.python_packages/sympy/testing/runtests.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.054`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/testing/runtests.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.054 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
This is our testing framework.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Skipped, TimeOutError, DependencyError, SymPyTests, SymPyDocTests, SymPyDocTestFinder, SymPyDocTestRunner, SymPyOutputChecker, Reporter, PyTestReporter, Transform, DummyWindow
- **funkcje:** `_indent`, `_report_failure`, `convert_to_native_paths`, `get_sympy_dir`, `setup_pprint`, `raise_on_deprecated`, `run_in_subprocess_with_hash_randomization`, `run_all_tests`, `test`, `_test`, `doctest`, `_get_doctest_blacklist`, `_doctest`, `split_list`, `sympytestfile`, `density_inv`, `test`, `_enhance_asserts`, `test_file`, `_timeout`, `matches`, `get_test_files`, `test`, `test_file`, `get_test_files`, `_check_dependencies`, `_find`, `_get_test`, `run`, `check_output`

## Opis
This is our testing framework.

Goals:

* it should be compatible with py.test and operate very similarly
  (or identically)
* does not require any external dependencies
* preferably all the functionality should be in this file only
* no magic, just import the test file and execute the test functions, that's it
* portable
