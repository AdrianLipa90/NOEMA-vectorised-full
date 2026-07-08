# modulefinder.py — .python_packages/mypy/modulefinder.py

## Tożsamość
- **id_karty:** `REPO-MODULEFINDER-1E0C`
- **ścieżka:** `.python_packages/mypy/modulefinder.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.144`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/modulefinder.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.144 |
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
Low-level infrastructure to find modules.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SearchPaths, ModuleNotFoundReason, BuildSource, BuildSourceSet, FindModuleCache
- **funkcje:** `matches_exclude`, `matches_gitignore`, `find_gitignores`, `is_init_file`, `verify_module`, `highest_init_level`, `mypy_path`, `default_lib_path`, `get_search_dirs`, `compute_search_paths`, `load_stdlib_py_versions`, `parse_version`, `typeshed_py_version`, `asdict`, `error_message_templates`, `is_source`, `clear`, `find_module_via_source_set`, `find_lib_path_dirs`, `get_toplevel_possibilities`, `find_module`, `_typeshed_has_version`, `_find_module_non_stub_helper`, `_update_ns_ancestors`, `_can_find_module_in_parent_dir`, `_find_module`, `find_modules_recursive`

## Opis
Low-level infrastructure to find modules.

This builds on fscache.py; find_sources.py builds on top of this.
