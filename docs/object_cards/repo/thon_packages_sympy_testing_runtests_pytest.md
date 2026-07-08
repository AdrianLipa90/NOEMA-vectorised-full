# runtests_pytest.py — .python_packages/sympy/testing/runtests_pytest.py

## Tożsamość
- **id_karty:** `REPO-RUNTESTS_PYTEST-2CCB`
- **ścieżka:** `.python_packages/sympy/testing/runtests_pytest.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.813`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/testing/runtests_pytest.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.813 |
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
Backwards compatible functions for running tests from SymPy using pytest.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PytestPluginManager, NoPytestError, pytest
- **funkcje:** `sympy_dir`, `update_args_with_paths`, `make_absolute_path`, `test`, `doctest`, `has_pytest`, `has_randomly`, `has_split`, `has_timeout`, `has_xdist`, `find_paths_matching_partial`, `is_tests_file`, `find_tests_matching_keywords`, `is_valid_partial_path`, `main`

## Opis
Backwards compatible functions for running tests from SymPy using pytest.

SymPy historically had its own testing framework that aimed to:
- be compatible with pytest;
- operate similarly (or identically) to pytest;
- not require any external dependencies;
- have all the functionality in one file only;
- have no magic, just import the test file and execute the test functions; and
- be portable.

T
