# stats.py — .python_packages/mypy/stats.py

## Tożsamość
- **id_karty:** `REPO-STATS-92F2`
- **ścieżka:** `.python_packages/mypy/stats.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.786`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/stats.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.786 |
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
Utilities for calculating and reporting statistics about types.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** StatisticsVisitor, HasAnyQuery, HasAnyQuery2
- **funkcje:** `dump_type_stats`, `is_special_module`, `is_imprecise`, `is_imprecise2`, `is_generic`, `is_complex`, `is_special_form_any`, `get_original_any`, `visit_mypy_file`, `visit_import_from`, `visit_import_all`, `process_import`, `visit_import`, `visit_func_def`, `enter_scope`, `is_checked_scope`, `visit_class_def`, `visit_type_application`, `visit_assignment_stmt`, `visit_expression_stmt`, `visit_pass_stmt`, `visit_break_stmt`, `visit_continue_stmt`, `visit_name_expr`, `visit_yield_from_expr`, `visit_call_expr`, `record_call_target_precision`, `record_callable_target_precision`, `visit_member_expr`, `visit_op_expr`

## Opis
Utilities for calculating and reporting statistics about types.
