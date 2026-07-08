# paths.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/paths.py

## Tożsamość
- **id_karty:** `REPO-PATHS-3292`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/paths.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.969`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/paths.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.969 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Project root path resolution for the CIEL-SOT-Agent package.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `resolve_project_root`, `resolve_existing_path`

## Opis
Project root path resolution for the CIEL-SOT-Agent package.

Provides ``resolve_project_root(anchor)`` which locates the repository root
by checking the ``CIEL_SOT_ROOT`` environment variable first, then walking
parent directories until one containing an ``integration/`` subdirectory is
found.

Also provides ``resolve_existing_path`` which returns the first candidate
relative path (under a given
