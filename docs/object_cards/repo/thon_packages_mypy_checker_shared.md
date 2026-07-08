# checker_shared.py — .python_packages/mypy/checker_shared.py

## Tożsamość
- **id_karty:** `REPO-CHECKER_SHARED-8537`
- **ścieżka:** `.python_packages/mypy/checker_shared.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.384`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/checker_shared.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.384 |
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
Shared definitions used by different parts of type checker.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypeRange, ExpressionCheckerSharedApi, TypeCheckerSharedApi, CheckerScope
- **funkcje:** `accept`, `analyze_ref_expr`, `check_call`, `transform_callee_type`, `method_fullname`, `check_method_call_by_name`, `visit_typeddict_index_expr`, `infer_literal_expr_type`, `analyze_static_reference`, `expr_checker`, `named_type`, `lookup_typeinfo`, `lookup_type`, `handle_cannot_determine_type`, `handle_partial_var_type`, `check_subtype`, `check_subtype`, `check_subtype`, `get_final_context`, `conditional_types_with_intersection`, `conditional_types_with_intersection`, `conditional_types_with_intersection`, `narrow_type_by_identity_equality`, `check_deprecated`, `warn_deprecated`, `type_is_iterable`, `iterable_item_type`, `checking_await_set`, `get_precise_awaitable_type`, `add_any_attribute_to_type`

## Opis
Shared definitions used by different parts of type checker.
