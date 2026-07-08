# reachability.py — .python_packages/mypy/reachability.py

## Tożsamość
- **id_karty:** `REPO-REACHABILITY-AD9F`
- **ścieżka:** `.python_packages/mypy/reachability.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.715`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/reachability.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.715 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Utilities related to determining the reachability of code (in semantic analysis).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MarkImportsUnreachableVisitor, MarkImportsMypyOnlyVisitor
- **funkcje:** `infer_reachability_of_if_statement`, `infer_reachability_of_match_statement`, `assert_will_always_fail`, `infer_condition_value`, `infer_pattern_value`, `consider_sys_version_info`, `consider_sys_platform`, `fixed_comparison`, `contains_int_or_tuple_of_ints`, `contains_sys_version_info`, `is_sys_attr`, `mark_block_unreachable`, `mark_block_mypy_only`, `visit_import`, `visit_import_from`, `visit_import_all`, `visit_import`, `visit_import_from`, `visit_import_all`, `visit_func_def`

## Opis
Utilities related to determining the reachability of code (in semantic analysis).
