# satellite_authority.py — build/lib/ciel_sot_agent/satellite_authority.py

## Tożsamość
- **id_karty:** `REPO-SATELLITE_AUTHORITY-BFB1`
- **ścieżka:** `build/lib/ciel_sot_agent/satellite_authority.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.202`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/satellite_authority.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.202 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Authority loading and lookup for satellite subsystems.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_satellite_authority_matrix`, `get_satellite_authority`, `require_export_surface`, `require_interaction_surface`, `require_io_stack`, `project_authority_summary`, `resolve_root`

## Opis
Authority loading and lookup for satellite subsystems.

Satellite subsystems live beyond the bridge horizon and must not silently
override canonical runtime state. This module centralizes the authority
matrix so code surfaces can read, expose, and enforce the same rules.
