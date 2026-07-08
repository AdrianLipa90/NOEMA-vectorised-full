# orbital_model.py — src/ciel_geometry/orbital_model.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_MODEL-075A`
- **ścieżka:** `src/ciel_geometry/orbital_model.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `2.981`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/orbital_model.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 2.981 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
orbital_model.py — autopoiesis orbitalna NOEMY.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

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
