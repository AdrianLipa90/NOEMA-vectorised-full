# build.py — .python_packages/mypy/build.py

## Tożsamość
- **id_karty:** `REPO-BUILD-74F8`
- **ścieżka:** `.python_packages/mypy/build.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.509`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/build.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.509 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Facilities to analyze entire programs, including imported modules.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SCC, BuildResult, WorkerClient, FgDepMeta, BuildManager, SuppressionReason, ModuleNotFound, State, NodeInfo, AckMessage, SccRequestMessage, ModuleResult, SccResponseMessage, SourcesDataMessage, SccsDataMessage, GraphMessage
- **funkcje:** `build_error`, `build`, `build_inner`, `warn_unused_configs`, `default_data_dir`, `normpath`, `import_priority`, `load_plugins_from_config`, `load_plugins`, `take_module_snapshot`, `find_config_file_line_number`, `deps_to_json`, `write_deps_cache`, `invert_deps`, `generate_deps_for_cache`, `write_plugins_snapshot`, `read_plugins_snapshot`, `read_quickstart_file`, `read_deps_cache`, `_load_ff_file`, `_load_json_file`, `_cache_dir_prefix`, `add_catch_all_gitignore`, `exclude_from_backups`, `create_metastore`, `get_meta_ex_name`, `get_cache_names`, `options_snapshot`, `find_cache_meta`, `validate_meta`

## Opis
Facilities to analyze entire programs, including imported modules.

Parse and analyze the source files of a program in the correct order
(based on file dependencies), and collect the results.

This module only directs a build, which is performed in multiple passes per
file.  The individual passes are implemented in separate modules.

The function build() is the main interface to this module.
