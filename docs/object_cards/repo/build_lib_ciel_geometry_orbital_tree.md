# orbital_tree.py — build/lib/ciel_geometry/orbital_tree.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_TREE-A659`
- **ścieżka:** `build/lib/ciel_geometry/orbital_tree.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.643`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/orbital_tree.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.643 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
orbital_tree.py — rekurencyjne drzewo orbitalne NOEMY.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
