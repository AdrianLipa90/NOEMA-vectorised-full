# checkexpr.py — .python_packages/mypy/checkexpr.py

## Tożsamość
- **id_karty:** `REPO-CHECKEXPR-BE89`
- **ścieżka:** `.python_packages/mypy/checkexpr.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.137`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/checkexpr.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.137 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
Expression type checker. This file is conceptually part of TypeChecker.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TooManyUnions, Finished, UseReverse, ExpressionChecker, HasAnyType, ArgInferSecondPassQuery, HasErasedComponentsQuery, HasUninhabitedComponentsQuery, HasAmbiguousUninhabitedComponentsQuery
- **funkcje:** `allow_fast_container_literal`, `has_any_type`, `has_coroutine_decorator`, `is_async_def`, `is_non_empty_tuple`, `is_duplicate_mapping`, `replace_callable_return_type`, `has_erased_component`, `has_uninhabited_component`, `has_ambiguous_uninhabited_component`, `arg_approximate_similarity`, `any_causes_overload_ambiguity`, `all_same_types`, `merge_typevars_in_callables_by_name`, `try_getting_literal`, `is_expr_literal_type`, `has_bytes_component`, `type_info_from_type`, `is_operator_method`, `get_partial_instance_type`, `is_type_type_context`, `reset`, `visit_name_expr`, `analyze_ref_expr`, `analyze_static_reference`, `analyze_var_ref`, `module_type`, `visit_call_expr`, `refers_to_typeddict`, `visit_call_expr_inner`

## Opis
Expression type checker. This file is conceptually part of TypeChecker.
