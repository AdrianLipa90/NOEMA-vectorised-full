# typeops.py — .python_packages/mypy/typeops.py

## Tożsamość
- **id_karty:** `REPO-TYPEOPS-E993`
- **ścieżka:** `.python_packages/mypy/typeops.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.371`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/typeops.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.371 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Miscellaneous type operations and helpers for use during type checking.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypeVarExtractor, FreezeTypeVarsVisitor
- **funkcje:** `is_recursive_pair`, `tuple_fallback`, `get_self_type`, `type_object_type`, `is_valid_constructor`, `type_object_type_from_function`, `class_callable`, `map_type_from_supertype`, `supported_self_type`, `bind_self`, `erase_to_bound`, `callable_corresponding_argument`, `simple_literal_type`, `is_simple_literal`, `make_simplified_union`, `_remove_redundant_union_items`, `_get_type_method_ret_type`, `true_only`, `false_only`, `true_or_false`, `erase_def_to_union_or_bound`, `erase_to_union_or_bound`, `function_type`, `callable_type`, `try_getting_str_literals`, `try_getting_str_literals_from_type`, `try_getting_int_literals_from_type`, `try_getting_literals_from_type`, `is_literal_type_like`, `is_singleton_identity_type`

## Opis
Miscellaneous type operations and helpers for use during type checking.

NOTE: These must not be accessed from mypy.nodes or mypy.types to avoid import
      cycles. These must not be called from the semantic analysis main pass
      since these may assume that MROs are ready.
