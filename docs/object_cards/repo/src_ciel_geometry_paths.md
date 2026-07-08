# paths.py — src/ciel_geometry/paths.py

## Tożsamość
- **id_karty:** `REPO-PATHS-2521`
- **ścieżka:** `src/ciel_geometry/paths.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `3.501`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/paths.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 3.501 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
NOEMA Paths — single source of truth for all file paths.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** _PathAccessor, _NoemaPaths
- **funkcje:** `_find_config`, `_resolve_vars`, `_expand`, `_replace`, `_get_dict`, `_load`, `surface_file`, `surface_subdir`, `resolve`, `config_path`, `dump`, `reload`

## Opis
NOEMA Paths — single source of truth for all file paths.

Usage:
    from ciel_geometry.paths import P

    # Root directories
    P.MEMORY           # /home/adrian/new_volume_rw/CIEL_memories
    P.LIBRARY          # /home/adrian/new_volume_rw/NOEMA_LIBRARY
    P.PHASE_DATA       # /home/adrian/new_volume_rw/NOEMA_PHASE_DATA
    P.SURFACE          # /dev/shm/ciel_noema

    # Databases
    P.DB.T
