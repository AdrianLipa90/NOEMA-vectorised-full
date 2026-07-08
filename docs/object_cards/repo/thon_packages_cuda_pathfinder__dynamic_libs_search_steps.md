# search_steps.py — .python_packages/cuda/pathfinder/_dynamic_libs/search_steps.py

## Tożsamość
- **id_karty:** `REPO-SEARCH_STEPS-B978`
- **ścieżka:** `.python_packages/cuda/pathfinder/_dynamic_libs/search_steps.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.301`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cuda/pathfinder/_dynamic_libs/search_steps.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.301 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Composable search steps for locating NVIDIA libraries.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FindResult, SearchContext
- **funkcje:** `_find_lib_dir_using_anchor`, `_find_using_lib_dir`, `_derive_ctk_root_linux`, `_derive_ctk_root_windows`, `derive_ctk_root`, `find_via_ctk_root`, `find_in_site_packages`, `find_in_conda`, `find_in_cuda_path`, `run_find_steps`, `libname`, `lib_searched_for`, `raise_not_found`

## Opis
Composable search steps for locating NVIDIA libraries.

Each find step is a callable with signature::

    (SearchContext) -> FindResult | None

Find steps locate a library file on disk without loading it.  The
orchestrator in :mod:`load_nvidia_dynamic_lib` handles loading, the
already-loaded check, and dependency resolution.

Step sequences are defined per search strategy so that adding a new
ste
