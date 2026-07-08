# typeinfer.py — .python_packages/numba/core/typeinfer.py

## Tożsamość
- **id_karty:** `REPO-TYPEINFER-F1C6`
- **ścieżka:** `.python_packages/numba/core/typeinfer.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.106`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/typeinfer.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.106 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Type inference base on CPA.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NOTSET, TypeVar, ConstraintNetwork, Propagate, ArgConstraint, BuildTupleConstraint, _BuildContainerConstraint, BuildListConstraint, BuildSetConstraint, BuildMapConstraint, ExhaustIterConstraint, PairFirstConstraint, PairSecondConstraint, StaticGetItemConstraint, TypedGetItemConstraint, CallConstraint, IntrinsicCallConstraint, GetAttrConstraint, SetItemRefinement, SetItemConstraint
- **funkcje:** `fold_arg_vars`, `_is_array_not_precise`, `register_dispatcher`, `add_type`, `lock`, `union`, `defined`, `get`, `getone`, `append`, `propagate`, `refine`, `get_call_signature`, `get_call_signature`, `resolve`, `_add_refine_map`, `refine`, `get_call_signature`, `refine`, `_refine_target_type`, `get_call_signature`, `get_call_signature`, `get_call_signature`, `get_call_signature`, `get_call_signature`, `set_context`, `copy`, `_mangle_arg_name`, `_get_return_vars`, `get_argument_types`

## Opis
Type inference base on CPA.
The algorithm guarantees monotonic growth of type-sets for each variable.

Steps:
    1. seed initial types
    2. build constraints
    3. propagate constraints
    4. unify types

Constraint propagation is precise and does not regret (no backtracing).
Constraints push types forward following the dataflow.
