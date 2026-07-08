# satellite_authority.py — src/ciel_sot_agent/satellite_authority.py

## Tożsamość
- **id_karty:** `REPO-SATELLITE_AUTHORITY-ACDE`
- **ścieżka:** `src/ciel_sot_agent/satellite_authority.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.347`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/satellite_authority.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.347 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


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
