# deps.py — .python_packages/mypy/server/deps.py

## Tożsamość
- **id_karty:** `REPO-DEPS-2E54`
- **ścieżka:** `.python_packages/mypy/server/deps.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.626`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/server/deps.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.626 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Generate fine-grained dependencies for AST nodes, for use in the daemon mode.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DependencyVisitor, TypeTriggersVisitor
- **funkcje:** `get_dependencies`, `get_dependencies_of_target`, `get_type_triggers`, `merge_dependencies`, `non_trivial_bases`, `has_user_bases`, `dump_all_dependencies`, `visit_mypy_file`, `visit_func_def`, `visit_decorator`, `visit_class_def`, `visit_newtype_expr`, `process_type_info`, `visit_import`, `visit_import_from`, `visit_import_all`, `visit_block`, `visit_assignment_stmt`, `process_lvalue`, `is_self_member_ref`, `get_non_partial_lvalue_type`, `visit_operator_assignment_stmt`, `visit_for_stmt`, `visit_with_stmt`, `visit_del_stmt`, `process_global_ref_expr`, `visit_name_expr`, `visit_member_expr`, `get_unimported_fullname`, `visit_super_expr`

## Opis
Generate fine-grained dependencies for AST nodes, for use in the daemon mode.

Dependencies are stored in a map from *triggers* to *sets of affected locations*.

A trigger is a string that represents a program property that has changed, such
as the signature of a specific function. Triggers are written as '<...>' (angle
brackets). When a program property changes, we determine the relevant trigger(
