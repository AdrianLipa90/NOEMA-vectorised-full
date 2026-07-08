# evalexpr.py — .python_packages/mypy/evalexpr.py

## Tożsamość
- **id_karty:** `REPO-EVALEXPR-3F92`
- **ścieżka:** `.python_packages/mypy/evalexpr.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.164`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/evalexpr.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.164 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Evaluate an expression.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _NodeEvaluator
- **funkcje:** `evaluate_expression`, `visit_int_expr`, `visit_str_expr`, `visit_bytes_expr`, `visit_float_expr`, `visit_complex_expr`, `visit_ellipsis`, `visit_star_expr`, `visit_name_expr`, `visit_member_expr`, `visit_yield_from_expr`, `visit_yield_expr`, `visit_call_expr`, `visit_op_expr`, `visit_comparison_expr`, `visit_cast_expr`, `visit_type_form_expr`, `visit_assert_type_expr`, `visit_reveal_expr`, `visit_super_expr`, `visit_unary_expr`, `visit_assignment_expr`, `visit_list_expr`, `visit_dict_expr`, `visit_tuple_expr`, `visit_set_expr`, `visit_index_expr`, `visit_type_application`, `visit_lambda_expr`, `visit_list_comprehension`

## Opis
Evaluate an expression.

Used by stubtest; in a separate file because things break if we don't
put it in a mypyc-compiled file.
