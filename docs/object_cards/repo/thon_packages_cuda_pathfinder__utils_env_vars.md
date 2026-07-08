# env_vars.py — .python_packages/cuda/pathfinder/_utils/env_vars.py

## Tożsamość
- **id_karty:** `REPO-ENV_VARS-419A`
- **ścieżka:** `.python_packages/cuda/pathfinder/_utils/env_vars.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.477`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cuda/pathfinder/_utils/env_vars.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.477 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
Centralized CUDA environment variable handling.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_paths_differ`, `get_cuda_path_or_home`

## Opis
Centralized CUDA environment variable handling.

This module defines the canonical search order for CUDA Toolkit environment variables
used throughout cuda-python packages (cuda.pathfinder, cuda.core, cuda.bindings).

Search Order Priority:
    1. CUDA_PATH (higher priority)
    2. CUDA_HOME (lower priority)

If both are set and differ, CUDA_PATH takes precedence and a warning is issued.

Importan
