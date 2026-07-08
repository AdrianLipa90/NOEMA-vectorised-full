# header_descriptor.py — .python_packages/cuda/pathfinder/_headers/header_descriptor.py

## Tożsamość
- **id_karty:** `REPO-HEADER_DESCRIPTOR-7AD4`
- **ścieżka:** `.python_packages/cuda/pathfinder/_headers/header_descriptor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.370`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/cuda/pathfinder/_headers/header_descriptor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.370 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Per-header descriptor, registry, and platform-aware accessors.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `platform_include_subdirs`, `resolve_conda_anchor`

## Opis
Per-header descriptor, registry, and platform-aware accessors.

The canonical authored data lives in :mod:`header_descriptor_catalog`. This
module provides a name-keyed registry and platform-dispatch helpers consumed
by the runtime search path — keeping the search code itself platform-agnostic.
