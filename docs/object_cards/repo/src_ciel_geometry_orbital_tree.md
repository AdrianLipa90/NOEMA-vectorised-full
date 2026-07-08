# orbital_tree.py — src/ciel_geometry/orbital_tree.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_TREE-2B65`
- **ścieżka:** `src/ciel_geometry/orbital_tree.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `4.905`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/orbital_tree.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 4.905 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
orbital_tree.py — rekurencyjne drzewo orbitalne NOEMY.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** OrbitalTree
- **funkcje:** `get_satellites`, `get_parents`, `get_subsystem_chain`, `get_all_descendants`, `flatten`, `render`, `find`, `_walk`, `_render`

## Opis
orbital_tree.py — rekurencyjne drzewo orbitalne NOEMY.

Rozwija system_map_v2.json w rekurencyjne drzewo: 
każdy satelita jest potencjalnym attractorem dla własnych satelitów,
w głąb, bez ograniczeń głębokości.

Usage:
    from ciel_geometry.orbital_tree import OrbitalTree
    tree = OrbitalTree()
    tree.render("NOEMA Core", max_depth=5)  # drzewo ASCII
    tree.get_subsystem_chain("05.01.02")
