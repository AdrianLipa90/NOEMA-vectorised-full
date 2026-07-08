# semanal_main.py — .python_packages/mypy/semanal_main.py

## Tożsamość
- **id_karty:** `REPO-SEMANAL_MAIN-86A5`
- **ścieżka:** `.python_packages/mypy/semanal_main.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.653`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/semanal_main.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.653 |
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
Top-level logic for the semantic analyzer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `semantic_analysis_for_scc`, `cleanup_builtin_scc`, `semantic_analysis_for_targets`, `process_top_levels`, `order_by_subclassing`, `process_functions`, `process_top_level_function`, `get_all_leaf_targets`, `semantic_analyze_target`, `check_type_arguments`, `check_type_arguments_in_targets`, `apply_class_plugin_hooks`, `apply_hooks_to_class`, `calculate_class_properties`, `check_blockers`

## Opis
Top-level logic for the semantic analyzer.

The semantic analyzer binds names, resolves imports, detects various
special constructs that don't have dedicated AST nodes after parse
(such as 'cast' which looks like a call), populates symbol tables, and
performs various simple consistency checks.

Semantic analysis of each SCC (strongly connected component; import
cycle) is performed in one unit. Eac
