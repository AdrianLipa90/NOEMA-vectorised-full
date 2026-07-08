# statement.py — .python_packages/mypyc/irbuild/statement.py

## Tożsamość
- **id_karty:** `REPO-STATEMENT-1292`
- **ścieżka:** `.python_packages/mypyc/irbuild/statement.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.822`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/statement.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.822 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Transform mypy statement ASTs to mypyc IR (Intermediate Representation).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ImportFromBucket, AwaitDetector
- **funkcje:** `transform_block`, `transform_expression_stmt`, `transform_return_stmt`, `check_unsupported_cls_assignment`, `transform_assignment_stmt`, `is_simple_lvalue`, `transform_operator_assignment_stmt`, `import_globals_id_and_name`, `transform_import`, `split_import_group_to_python_and_native`, `transform_imports_without_grouping`, `transform_non_native_import_group`, `transform_import_from`, `group_consecutive`, `classify_import_from`, `transform_import_from_buckets`, `transform_import_all`, `transform_if_stmt`, `transform_while_stmt`, `transform_for_stmt`, `transform_break_stmt`, `transform_continue_stmt`, `transform_raise_stmt`, `transform_try_except`, `transform_try_except_stmt`, `try_finally_try`, `try_finally_entry_blocks`, `try_finally_body`, `try_finally_resolve_control`, `transform_try_finally_stmt`

## Opis
Transform mypy statement ASTs to mypyc IR (Intermediate Representation).

The top-level AST transformation logic is implemented in mypyc.irbuild.visitor
and mypyc.irbuild.builder.

A few statements are transformed in mypyc.irbuild.function (yield, for example).
