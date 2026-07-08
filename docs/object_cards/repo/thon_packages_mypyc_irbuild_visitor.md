# visitor.py — .python_packages/mypyc/irbuild/visitor.py

## Tożsamość
- **id_karty:** `REPO-VISITOR-C54D`
- **ścieżka:** `.python_packages/mypyc/irbuild/visitor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.023`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/visitor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.023 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
Dispatcher used when transforming a mypy AST to the IR form.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** IRBuilderVisitor
- **funkcje:** `visit_mypy_file`, `visit_class_def`, `visit_import`, `visit_import_from`, `visit_import_all`, `visit_func_def`, `visit_overloaded_func_def`, `visit_decorator`, `visit_block`, `visit_expression_stmt`, `visit_return_stmt`, `visit_assignment_stmt`, `visit_operator_assignment_stmt`, `visit_if_stmt`, `visit_while_stmt`, `visit_for_stmt`, `visit_break_stmt`, `visit_continue_stmt`, `visit_raise_stmt`, `visit_try_stmt`, `visit_with_stmt`, `visit_pass_stmt`, `visit_assert_stmt`, `visit_del_stmt`, `visit_global_decl`, `visit_nonlocal_decl`, `visit_match_stmt`, `visit_type_alias_stmt`, `visit_name_expr`, `visit_member_expr`

## Opis
Dispatcher used when transforming a mypy AST to the IR form.

mypyc.irbuild.builder and mypyc.irbuild.main are closely related.
