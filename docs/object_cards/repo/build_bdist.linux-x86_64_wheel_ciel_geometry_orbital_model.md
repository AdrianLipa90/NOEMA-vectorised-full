# orbital_model.py — build/bdist.linux-x86_64/wheel/ciel_geometry/orbital_model.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_MODEL-252F`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/orbital_model.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.385`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/orbital_model.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.385 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
orbital_model.py — autopoiesis orbitalna NOEMY.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Orbit, System, OrbitalUniverse
- **funkcje:** `id`, `resonance_ratio`, `orbital_radius`, `to_dict`, `attractor_count`, `satellite_count`, `total_orbits`, `net_gravity`, `total_weight`, `mean_phase`, `add_orbit`, `add_orbit_raw`, `add_mutual_orbit`, `orbits`, `orbit_count`, `systems`, `get_system`, `set_system_meta`, `system_count`, `get_satellites`, `get_attractors`, `get_orbit_between`, `has_mutual`, `get_primary_attractors`, `get_multi_orbit_systems`, `compute_phase_field`, `compute_coherence`, `render`, `_render_nbody`, `_render_from`

## Opis
orbital_model.py — autopoiesis orbitalna NOEMY.

Systemy emergują z orbit. Nie ma osobnej definicji systemu —
system jest zbiorem swoich relacji orbitalnych.

Każda orbita = attractor → satelita z właściwościami:
  - weight: siła sprzężenia (W_ij w Kuramoto)
  - phase_shift: przesunięcie fazowe Δφ
  - resonance: stosunek częstotliwości (np. "3:2", "1:1")
  - harmonic: numer harmonicznej

Model jes
