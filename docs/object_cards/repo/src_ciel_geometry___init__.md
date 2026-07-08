# __init__.py — src/ciel_geometry/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-099F`
- **ścieżka:** `src/ciel_geometry/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `4.608`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/__init__.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 4.608 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

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
ciel_geometry — Poincaré disk geometry engine for CIEL orbital system.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
ciel_geometry — Poincaré disk geometry engine for CIEL orbital system.

CIEL ORBITAL BINDING — HARDCODED CHECK przy każdym imporcie.
Jeśli binding_status nie jest ACTIVE → system działa w trybie degradowanym.

Exports are loaded lazily so module CLIs like
``python -m ciel_geometry.noema_surface_mmap`` do not trigger duplicate-import
warnings via eager package side effects.
