# join.py — .python_packages/mypy/join.py

## Tożsamość
- **id_karty:** `REPO-JOIN-ED5D`
- **ścieżka:** `.python_packages/mypy/join.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.114`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/join.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.114 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
Calculation of the least upper bound types (joins).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** InstanceJoiner, TypeJoinVisitor
- **funkcje:** `trivial_join`, `join_types`, `join_types`, `join_types`, `is_better`, `normalize_callables`, `is_similar_callables`, `is_similar_params`, `update_callable_ids`, `match_generic_callables`, `join_similar_callables`, `safe_join`, `safe_meet`, `combine_similar_callables`, `combine_arg_names`, `object_from_instance`, `object_or_any_from_type`, `join_type_list`, `unpack_callback_protocol`, `join_instances`, `join_instances_via_supertype`, `visit_unbound_type`, `visit_union_type`, `visit_any`, `visit_none_type`, `visit_uninhabited_type`, `visit_deleted_type`, `visit_erased_type`, `visit_type_var`, `visit_param_spec`

## Opis
Calculation of the least upper bound types (joins).
