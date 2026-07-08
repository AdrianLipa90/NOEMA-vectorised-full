# paths.py — build/lib/ciel_geometry/paths.py

## Tożsamość
- **id_karty:** `REPO-PATHS-46F5`
- **ścieżka:** `build/lib/ciel_geometry/paths.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.502`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/paths.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.502 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
NOEMA Paths — single source of truth for all file paths.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _PathAccessor, _NoemaPaths
- **funkcje:** `_find_config`, `_resolve_vars`, `_expand`, `_replace`, `_get_dict`, `_load`, `surface_file`, `surface_subdir`, `resolve`, `config_path`, `dump`, `reload`

## Opis
NOEMA Paths — single source of truth for all file paths.

Usage:
    from ciel_geometry.paths import P

    # Root directories
    P.MEMORY           # /media/adrian/New Volume1/CIEL_memories
    P.LIBRARY          # /media/adrian/New Volume1/NOEMA_LIBRARY
    P.PHASE_DATA       # /media/adrian/New Volume1/NOEMA_PHASE_DATA
    P.SURFACE          # /dev/shm/ciel_noema

    # Databases
    P.DB.TASK
