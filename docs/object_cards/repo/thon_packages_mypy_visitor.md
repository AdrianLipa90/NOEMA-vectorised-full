# visitor.py — .python_packages/mypy/visitor.py

## Tożsamość
- **id_karty:** `REPO-VISITOR-5DCE`
- **ścieżka:** `.python_packages/mypy/visitor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.429`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/visitor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.429 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Generic abstract syntax tree node visitor

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ExpressionVisitor, StatementVisitor, PatternVisitor, NodeVisitor
- **funkcje:** `visit_int_expr`, `visit_str_expr`, `visit_bytes_expr`, `visit_float_expr`, `visit_complex_expr`, `visit_ellipsis`, `visit_star_expr`, `visit_name_expr`, `visit_member_expr`, `visit_yield_from_expr`, `visit_yield_expr`, `visit_call_expr`, `visit_op_expr`, `visit_comparison_expr`, `visit_cast_expr`, `visit_type_form_expr`, `visit_assert_type_expr`, `visit_reveal_expr`, `visit_super_expr`, `visit_unary_expr`, `visit_assignment_expr`, `visit_list_expr`, `visit_dict_expr`, `visit_template_str_expr`, `visit_tuple_expr`, `visit_set_expr`, `visit_index_expr`, `visit_type_application`, `visit_lambda_expr`, `visit_list_comprehension`

## Opis
Generic abstract syntax tree node visitor
