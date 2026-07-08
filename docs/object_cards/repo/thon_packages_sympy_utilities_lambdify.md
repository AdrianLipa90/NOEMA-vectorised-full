# lambdify.py — .python_packages/sympy/utilities/lambdify.py

## Tożsamość
- **id_karty:** `REPO-LAMBDIFY-5FD2`
- **ścieżka:** `.python_packages/sympy/utilities/lambdify.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.001`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/utilities/lambdify.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.001 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
This module provides convenient functions to transform SymPy expressions to

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _EvaluatorPrinter, _TensorflowEvaluatorPrinter
- **funkcje:** `_import`, `lambdify`, `_module_present`, `_get_namespace`, `_recursive_to_string`, `lambdastr`, `_imp_namespace`, `implemented_function`, `_too_large_for_docstring`, `cleanup_linecache`, `sub_args`, `sub_expr`, `isiter`, `flat_indexes`, `doprint`, `_is_safe_ident`, `_preprocess`, `_subexpr`, `_print_funcargwrapping`, `_print_unpacking`, `_handle_Subs`, `_print_unpacking`, `_cleanup`, `update_dummies`, `unpack_lhs`, `_replace`, `flat_indexes`

## Opis
This module provides convenient functions to transform SymPy expressions to
lambda functions which can be used to calculate numerical values very fast.
