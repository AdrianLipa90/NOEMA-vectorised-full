# checkpattern.py — .python_packages/mypy/checkpattern.py

## Tożsamość
- **id_karty:** `REPO-CHECKPATTERN-A7CD`
- **ścieżka:** `.python_packages/mypy/checkpattern.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.507`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/checkpattern.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.507 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
Pattern checker. This file is conceptually part of TypeChecker.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PatternType, PatternChecker
- **funkcje:** `get_match_arg_names`, `get_var`, `get_type_range`, `is_uninhabited`, `accept`, `visit_as_pattern`, `visit_or_pattern`, `visit_value_pattern`, `visit_singleton_pattern`, `visit_sequence_pattern`, `contract_starred_pattern_types`, `expand_starred_pattern_types`, `visit_starred_pattern`, `visit_mapping_pattern`, `get_mapping_item_type`, `get_simple_mapping_item_type`, `visit_class_pattern`, `get_class_pattern_type_ranges`, `should_self_match`, `can_match_sequence`, `generate_types_from_names`, `update_type_map`, `construct_sequence_child`, `early_non_match`

## Opis
Pattern checker. This file is conceptually part of TypeChecker.
