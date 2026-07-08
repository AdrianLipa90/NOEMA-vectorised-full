# aststrip.py — .python_packages/mypy/server/aststrip.py

## Tożsamość
- **id_karty:** `REPO-ASTSTRIP-40B2`
- **ścieżka:** `.python_packages/mypy/server/aststrip.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.293`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/server/aststrip.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.293 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Strip/reset AST in-place to match state after semantic analyzer pre-analysis.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NodeStripVisitor
- **funkcje:** `strip_target`, `strip_file_top_level`, `visit_block`, `visit_class_def`, `visit_func_def`, `visit_decorator`, `visit_overloaded_func_def`, `visit_assignment_stmt`, `visit_import_from`, `visit_import_all`, `visit_for_stmt`, `visit_name_expr`, `visit_member_expr`, `visit_index_expr`, `visit_op_expr`, `strip_ref_expr`, `visit_call_expr`, `visit_super_expr`, `process_lvalue_in_method`, `enter_class`, `enter_method`

## Opis
Strip/reset AST in-place to match state after semantic analyzer pre-analysis.

Fine-grained incremental mode reruns semantic analysis main pass
and type checking for *existing* AST nodes (targets) when changes are
propagated using fine-grained dependencies.  AST nodes attributes are
sometimes changed during semantic analysis main pass, and running
semantic analysis again on those nodes would produ
