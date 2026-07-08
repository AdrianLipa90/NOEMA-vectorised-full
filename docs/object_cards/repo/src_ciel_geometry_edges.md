# edges.py — src/ciel_geometry/edges.py

## Tożsamość
- **id_karty:** `REPO-EDGES-53DE`
- **ścieżka:** `src/ciel_geometry/edges.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `5.607`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/edges.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 5.607 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
Build geodesic edges between nodes on the Poincaré disk.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** GeodesicEdge
- **funkcje:** `build_sector_edges`, `build_entity_edges`

## Opis
Build geodesic edges between nodes on the Poincaré disk.
