# constraints.py — .python_packages/mypy/constraints.py

## Tożsamość
- **id_karty:** `REPO-CONSTRAINTS-D857`
- **ścieżka:** `.python_packages/mypy/constraints.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.257`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/constraints.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.257 |
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
Type inference constraints.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Constraint, ConstraintBuilderVisitor
- **funkcje:** `infer_constraints_for_callable`, `infer_constraints`, `_infer_constraints`, `_is_type_type`, `_unwrap_type_type`, `infer_constraints_if_possible`, `select_trivial`, `merge_with_any`, `handle_recursive_union`, `any_constraints`, `filter_satisfiable`, `exclude_non_meta_vars`, `is_same_constraints`, `is_same_constraint`, `is_similar_constraints`, `_is_similar_constraints`, `neg_op`, `find_matching_overload_item`, `find_matching_overload_items`, `get_tuple_fallback_from_unpack`, `repack_callable_args`, `build_constraints_for_simple_unpack`, `infer_directed_arg_constraints`, `infer_callable_arguments_constraints`, `filter_imprecise_kinds`, `visit_unbound_type`, `visit_any`, `visit_none_type`, `visit_uninhabited_type`, `visit_erased_type`

## Opis
Type inference constraints.
