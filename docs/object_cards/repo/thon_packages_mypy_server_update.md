# update.py — .python_packages/mypy/server/update.py

## Tożsamość
- **id_karty:** `REPO-UPDATE-8167`
- **ścieżka:** `.python_packages/mypy/server/update.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.545`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/server/update.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.545 |
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
Update build by processing changes using fine-grained dependencies.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FineGrainedBuildManager, NormalUpdate, BlockedUpdate
- **funkcje:** `find_unloaded_deps`, `ensure_deps_loaded`, `ensure_trees_loaded`, `update_module_isolated`, `find_relative_leaf_module`, `delete_module`, `dedupe_modules`, `get_module_to_path_map`, `get_sources`, `calculate_active_triggers`, `replace_modules_with_new_variants`, `propagate_changes_using_dependencies`, `find_targets_recursive`, `reprocess_nodes`, `find_symbol_tables_recursive`, `update_deps`, `lookup_target`, `_lookup_target_impl`, `is_verbose`, `target_from_node`, `refresh_suppressed_submodules`, `extract_fnam_from_message`, `extract_possible_fnam_from_message`, `sort_messages_preserving_file_order`, `update`, `trigger`, `flush_cache`, `update_one`, `update_module`, `restore`

## Opis
Update build by processing changes using fine-grained dependencies.

Use fine-grained dependencies to update targets in other modules that
may be affected by externally-visible changes in the changed modules.

This forms the core of the fine-grained incremental daemon mode. This
module is not used at all by the 'classic' (non-daemon) incremental
mode.

Here is some motivation for this mode:

* By
