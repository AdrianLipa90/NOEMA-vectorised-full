# traverser.py — .python_packages/mypy/traverser.py

## Tożsamość
- **id_karty:** `REPO-TRAVERSER-34DF`
- **ścieżka:** `.python_packages/mypy/traverser.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.203`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/traverser.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.203 |
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
Generic node traverser visitor

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TraverserVisitor, ExtendedTraverserVisitor, ReturnSeeker, NameAndMemberCollector, StringSeeker, FuncCollectorBase, YieldSeeker, YieldFromSeeker, AwaitSeeker, ReturnCollector, YieldCollector, YieldFromCollector
- **funkcje:** `has_return_statement`, `all_name_and_member_expressions`, `has_str_expression`, `has_yield_expression`, `has_yield_from_expression`, `has_await_expression`, `all_return_statements`, `all_yield_expressions`, `visit_mypy_file`, `visit_block`, `visit_func`, `visit_func_def`, `visit_overloaded_func_def`, `visit_class_def`, `visit_decorator`, `visit_expression_stmt`, `visit_assignment_stmt`, `visit_operator_assignment_stmt`, `visit_while_stmt`, `visit_for_stmt`, `visit_return_stmt`, `visit_assert_stmt`, `visit_del_stmt`, `visit_if_stmt`, `visit_raise_stmt`, `visit_try_stmt`, `visit_with_stmt`, `visit_match_stmt`, `visit_type_alias_stmt`, `visit_member_expr`

## Opis
Generic node traverser visitor
