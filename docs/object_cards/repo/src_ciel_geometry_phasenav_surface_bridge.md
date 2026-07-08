# surface_bridge.py — src/ciel_geometry/phasenav/surface_bridge.py

## Tożsamość
- **id_karty:** `REPO-SURFACE_BRIDGE-6DDD`
- **ścieżka:** `src/ciel_geometry/phasenav/surface_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `0.541`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/phasenav/surface_bridge.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 0.541 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
PhaseNav → surface bridge — maps concept phases to 36 oscillator surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** PhaseNavSurfaceBridge
- **funkcje:** `load`, `seed_surface_from_concept`, `apply_trace`, `_drive_phases_from_vector`, `_modulate_omegas_from_vector`, `_find_operator_for_concept`, `concept_similarity`

## Opis
PhaseNav → surface bridge — maps concept phases to 36 oscillator surface.

Connects PhaseNav semantic navigation (concept → operator 36D vector)
to the 3-6-9 harmonic Kuramoto surface via oscillator phase seeding.
