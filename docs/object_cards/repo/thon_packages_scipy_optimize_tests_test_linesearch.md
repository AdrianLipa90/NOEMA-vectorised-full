# test_linesearch.py — .python_packages/scipy/optimize/tests/test_linesearch.py

## Tożsamość
- **id_karty:** `REPO-TEST_LINESEARCH-7214`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test_linesearch.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.244`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test_linesearch.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.244 |
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
Tests for line search routines

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestLineSearch
- **funkcje:** `assert_wolfe`, `assert_armijo`, `assert_line_wolfe`, `assert_line_armijo`, `assert_fp_equal`, `_scalar_func_1`, `_scalar_func_2`, `_scalar_func_3`, `_line_func_1`, `_line_func_2`, `setup_method`, `scalar_iter`, `line_iter`, `test_scalar_search_wolfe1`, `test_scalar_search_wolfe2`, `test_scalar_search_wolfe2_with_low_amax`, `test_scalar_search_wolfe2_regression`, `test_scalar_search_armijo`, `test_line_search_wolfe1`, `test_line_search_wolfe2`, `test_line_search_wolfe2_bounds`, `test_line_search_armijo`, `test_armijo_terminate_1`, `test_wolfe_terminate`, `bind_index`, `phi`, `derphi`, `phi`, `derphi`, `f`

## Opis
Tests for line search routines
