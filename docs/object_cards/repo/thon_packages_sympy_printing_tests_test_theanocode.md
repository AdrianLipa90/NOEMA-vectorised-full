# test_theanocode.py — .python_packages/sympy/printing/tests/test_theanocode.py

## Tożsamość
- **id_karty:** `REPO-TEST_THEANOCODE-C837`
- **ścieżka:** `.python_packages/sympy/printing/tests/test_theanocode.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.854`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/printing/tests/test_theanocode.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.854 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Important note on tests in this module - the Theano printing functions use a

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `theano_code_`, `theano_function_`, `fgraph_of`, `theano_simplify`, `theq`, `test_example_symbols`, `test_Symbol`, `test_MatrixSymbol`, `test_MatrixSymbol_wrong_dims`, `test_AppliedUndef`, `test_add`, `test_trig`, `test_many`, `test_dtype`, `test_broadcastables`, `test_broadcasting`, `test_MatMul`, `test_Transpose`, `test_MatAdd`, `test_Rationals`, `test_Integers`, `test_factorial`, `test_Derivative`, `test_theano_function_simple`, `test_theano_function_multi`, `test_theano_function_numpy`, `test_theano_function_matrix`, `test_dim_handling`, `test_theano_function_kwargs`, `test_theano_function_scalar`

## Opis
Important note on tests in this module - the Theano printing functions use a
global cache by default, which means that tests using it will modify global
state and thus not be independent from each other. Instead of using the "cache"
keyword argument each time, this module uses the theano_code_ and
theano_function_ functions defined below which default to using a new, empty
cache instead.
