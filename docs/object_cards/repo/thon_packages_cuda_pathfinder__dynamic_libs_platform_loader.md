# platform_loader.py — .python_packages/cuda/pathfinder/_dynamic_libs/platform_loader.py

## Tożsamość
- **id_karty:** `REPO-PLATFORM_LOADER-DA0C`
- **ścieżka:** `.python_packages/cuda/pathfinder/_dynamic_libs/platform_loader.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.267`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cuda/pathfinder/_dynamic_libs/platform_loader.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.267 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Platform loader seam for OS-specific dynamic linking.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PlatformLoader
- **funkcje:** `check_if_already_loaded_from_elsewhere`, `load_with_system_search`, `load_with_abs_path`

## Opis
Platform loader seam for OS-specific dynamic linking.

This module provides a small interface that hides the Linux vs Windows
implementation details of:

- already-loaded checks
- system-search loading
- absolute-path loading

The orchestration logic in :mod:`load_nvidia_dynamic_lib` should not need to
branch on platform; it calls through the loader instance exported here.
