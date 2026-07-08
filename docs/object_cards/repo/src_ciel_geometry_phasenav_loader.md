# loader.py — src/ciel_geometry/phasenav/loader.py

## Tożsamość
- **id_karty:** `REPO-LOADER-44AA`
- **ścieżka:** `src/ciel_geometry/phasenav/loader.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `6.058`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/phasenav/loader.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 6.058 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Load PhaseNav data — concept cards, phases, orbits, edges.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** PhaseNavData
- **funkcje:** `load_phasenav`, `_default_path`, `_lines`, `_load_jsonl_map`, `_load_orbit_map`

## Opis
Load PhaseNav data — concept cards, phases, orbits, edges.

Supports both JSONL files and direct in-memory loading.
