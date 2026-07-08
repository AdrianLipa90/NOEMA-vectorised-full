# orbital_tree.py — build/bdist.linux-x86_64/wheel/ciel_geometry/orbital_tree.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_TREE-6F3F`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/orbital_tree.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.453`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/orbital_tree.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.453 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


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
