# annotate.py — .python_packages/mypyc/annotate.py

## Tożsamość
- **id_karty:** `REPO-ANNOTATE-6F4A`
- **ścieżka:** `.python_packages/mypyc/annotate.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.378`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/annotate.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.378 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Generate source code formatted as HTML, with bottlenecks annotated and highlighted.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Annotation, AnnotatedSource, ASTAnnotateVisitor
- **funkcje:** `generate_annotated_html`, `generate_annotations`, `function_annotations`, `get_str_literal`, `get_max_prio`, `generate_html_report`, `colorize_line`, `visit_func_def`, `visit_for_stmt`, `visit_dictionary_comprehension`, `visit_generator_expr`, `check_iteration`, `visit_class_def`, `visit_with_stmt`, `visit_assignment_stmt`, `visit_name_expr`, `visit_member_expr`, `visit_call_expr`, `check_isinstance_arg`, `visit_lambda_expr`, `annotate`, `get_type`

## Opis
Generate source code formatted as HTML, with bottlenecks annotated and highlighted.

Various heuristics are used to detect common issues that cause slower than
expected performance.
