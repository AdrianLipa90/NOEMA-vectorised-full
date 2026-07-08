# treetransform.py — .python_packages/mypy/treetransform.py

## Tożsamość
- **id_karty:** `REPO-TREETRANSFORM-488F`
- **ścieżka:** `.python_packages/mypy/treetransform.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.429`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/treetransform.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.429 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Base visitor that implements an identity AST transform.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TransformVisitor, FuncMapInitializer
- **funkcje:** `visit_mypy_file`, `visit_import`, `visit_import_from`, `visit_import_all`, `copy_argument`, `visit_func_def`, `visit_lambda_expr`, `copy_function_attributes`, `visit_overloaded_func_def`, `visit_class_def`, `visit_global_decl`, `visit_nonlocal_decl`, `visit_block`, `visit_decorator`, `visit_var`, `visit_expression_stmt`, `visit_assignment_stmt`, `duplicate_assignment`, `visit_operator_assignment_stmt`, `visit_while_stmt`, `visit_for_stmt`, `visit_return_stmt`, `visit_assert_stmt`, `visit_del_stmt`, `visit_if_stmt`, `visit_break_stmt`, `visit_continue_stmt`, `visit_pass_stmt`, `visit_raise_stmt`, `visit_try_stmt`

## Opis
Base visitor that implements an identity AST transform.

Subclass TransformVisitor to perform non-trivial transformations.
