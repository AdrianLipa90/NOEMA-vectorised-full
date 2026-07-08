# orbital_cockpit.py — src/ciel-omega-demo-main/main/apps/orbital_cockpit.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_COCKPIT-2E34`
- **ścieżka:** `src/ciel-omega-demo-main/main/apps/orbital_cockpit.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `3.153`
- **masa_semantyczna:** `0.60`

## Kotwice
- `src/ciel-omega-demo-main/main/apps/orbital_cockpit.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 3.153 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.60 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `ciel_omega_core`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
—

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** EpistemicStatus, OrbitId, WhiteThread, OrbitalNode, IdentityState, CockpitTopology
- **funkcje:** `build_default_topology`, `orbit_navigation_groups`, `flatten_navigation`, `labels`, `orbit_nodes`, `get`, `add_node`, `add_thread`, `related_threads`

## Opis
—
