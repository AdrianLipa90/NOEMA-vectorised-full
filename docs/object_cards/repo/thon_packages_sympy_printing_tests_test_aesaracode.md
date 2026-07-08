# test_aesaracode.py — .python_packages/sympy/printing/tests/test_aesaracode.py

## Tożsamość
- **id_karty:** `REPO-TEST_AESARACODE-0A60`
- **ścieżka:** `.python_packages/sympy/printing/tests/test_aesaracode.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.398`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/printing/tests/test_aesaracode.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.398 |
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
Important note on tests in this module - the Aesara printing functions use a

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `aesara_code_`, `aesara_function_`, `fgraph_of`, `aesara_simplify`, `theq`, `test_example_symbols`, `test_Symbol`, `test_MatrixSymbol`, `test_MatrixSymbol_wrong_dims`, `test_AppliedUndef`, `test_add`, `test_trig`, `test_many`, `test_dtype`, `test_broadcastables`, `test_broadcasting`, `test_MatMul`, `test_Transpose`, `test_MatAdd`, `test_Rationals`, `test_Integers`, `test_factorial`, `test_Derivative`, `test_aesara_function_simple`, `test_aesara_function_multi`, `test_aesara_function_numpy`, `test_aesara_function_matrix`, `test_dim_handling`, `test_aesara_function_kwargs`, `test_aesara_function_scalar`

## Opis
Important note on tests in this module - the Aesara printing functions use a
global cache by default, which means that tests using it will modify global
state and thus not be independent from each other. Instead of using the "cache"
keyword argument each time, this module uses the aesara_code_ and
aesara_function_ functions defined below which default to using a new, empty
cache instead.
