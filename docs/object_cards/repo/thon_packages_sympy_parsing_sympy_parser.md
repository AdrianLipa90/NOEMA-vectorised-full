# sympy_parser.py — .python_packages/sympy/parsing/sympy_parser.py

## Tożsamość
- **id_karty:** `REPO-SYMPY_PARSER-6C10`
- **ścieżka:** `.python_packages/sympy/parsing/sympy_parser.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.183`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/parsing/sympy_parser.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.183 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
Transform a string with Python-like source code into SymPy expression.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ParenthesisGroup, AppliedFunction, EvaluateFalseTransformer, _T
- **funkcje:** `_token_splittable`, `_token_callable`, `_add_factorial_tokens`, `_flatten`, `_group_parentheses`, `_apply_functions`, `_implicit_multiplication`, `_implicit_application`, `function_exponentiation`, `split_symbols_custom`, `implicit_multiplication`, `implicit_application`, `implicit_multiplication_application`, `auto_symbol`, `lambda_notation`, `factorial_notation`, `convert_xor`, `repeated_decimals`, `auto_number`, `rationalize`, `_transform_equals_sign`, `convert_equals_signs`, `stringify_expr`, `eval_expr`, `parse_expr`, `evaluateFalse`, `expand`, `_inner`, `_split_symbols`, `is_digit`

## Opis
Transform a string with Python-like source code into SymPy expression.
