# surface_bridge.py — build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/surface_bridge.py

## Tożsamość
- **id_karty:** `REPO-SURFACE_BRIDGE-7750`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/surface_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.069`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/surface_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.069 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
PhaseNav → surface bridge — maps concept phases to 24 oscillator surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TeleusingSurfaceBridge
- **funkcje:** `load`, `seed_surface_from_concept`, `apply_trace`, `_drive_phases_from_vector`, `_modulate_omegas_from_vector`, `_find_operator_for_concept`, `concept_similarity`

## Opis
PhaseNav → surface bridge — maps concept phases to 24 oscillator surface.

Connects PhaseNav semantic navigation (concept → operator 24D vector)
to the 3-6-9 harmonic Kuramoto surface via oscillator phase seeding.
