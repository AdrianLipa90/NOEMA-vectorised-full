# dmypy_server.py — .python_packages/mypy/dmypy_server.py

## Tożsamość
- **id_karty:** `REPO-DMYPY_SERVER-6B9C`
- **ścieżka:** `.python_packages/mypy/dmypy_server.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.462`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/dmypy_server.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.462 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Server for mypy daemon mode.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Server
- **funkcje:** `process_start_options`, `ignore_suppressed_imports`, `get_meminfo`, `find_all_sources_in_build`, `add_all_sources_to_changed`, `fix_module_deps`, `filter_out_missing_top_level_packages`, `daemonize`, `_daemonize_cb`, `daemonize`, `_response_metadata`, `serve`, `run_command`, `cmd_status`, `cmd_stop`, `cmd_run`, `cmd_check`, `cmd_recheck`, `check`, `flush_caches`, `update_stats`, `following_imports`, `initialize_fine_grained`, `fine_grained_increment`, `fine_grained_increment_follow_imports`, `find_reachable_changed_modules`, `direct_imports`, `find_added_suppressed`, `increment_output`, `pretty_messages`

## Opis
Server for mypy daemon mode.

This implements a daemon process which keeps useful state in memory
to enable fine-grained incremental reprocessing of changes.
