# renderer_mpl.py — src/ciel_geometry/renderer_mpl.py

## Tożsamość
- **id_karty:** `REPO-RENDERER_MPL-1421`
- **ścieżka:** `src/ciel_geometry/renderer_mpl.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `1.173`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/renderer_mpl.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 1.173 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
Matplotlib Poincaré disk renderer — interactive orbital cockpit (Foundation Pack P6 MVP).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_node_label`, `_health_bar`, `render`, `_parse_args`, `main`

## Opis
Matplotlib Poincaré disk renderer — interactive orbital cockpit (Foundation Pack P6 MVP).

Usage:
    python -m ciel_geometry.renderer_mpl              # static snapshot
    python -m ciel_geometry.renderer_mpl --live       # auto-refresh every 5s
    python -m ciel_geometry.renderer_mpl --save out.png
