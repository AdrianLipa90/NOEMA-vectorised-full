# checker.py — .python_packages/mypy/checker.py

## Tożsamość
- **id_karty:** `REPO-CHECKER-1415`
- **ścieżka:** `.python_packages/mypy/checker.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.451`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/checker.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.451 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Mypy type checker.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DeferredNode, FineGrainedDeferredNode, PartialTypeScope, LocalTypeMap, TypeChecker, TypeCheckerAsSemanticAnalyzer, CollectArgTypeVarTypes, TypeTransformVisitor, InvalidInferredTypes, SetNothingToAny, DisjointDict, VarAssignVisitor, EqualityDomainInfo, EqualityValueInfo
- **funkcje:** `conditional_types`, `conditional_types`, `conditional_types`, `conditional_types_to_typemaps`, `gen_unique_name`, `is_true_literal`, `is_false_literal`, `is_literal_none`, `is_literal_not_implemented`, `_is_empty_generator_function`, `builtin_item_type`, `is_unreachable_map`, `and_conditional_maps`, `or_conditional_maps`, `reduce_conditional_maps`, `reduce_or_conditional_type_maps`, `reduce_and_conditional_type_maps`, `has_custom_eq_checks`, `convert_to_typetype`, `flatten`, `flatten_types_if_tuple`, `expand_func`, `are_argument_counts_overlapping`, `expand_callable_variants`, `is_unsafe_overlapping_overload_signatures`, `detach_callable`, `overload_can_never_match`, `is_more_general_arg_prefix`, `is_same_arg_prefix`, `infer_operator_assignment_method`

## Opis
Mypy type checker.

Infer types of expressions and type-check the AST. We use multi-pass architecture,
this means we re-visit the AST until either all types are inferred, or we hit the
upper limit on number of passes (currently 3). The number of passes is intentionally
low, mostly to keep performance predictable. An example of code where more than one
pass is needed:

    def foo() -> None:
