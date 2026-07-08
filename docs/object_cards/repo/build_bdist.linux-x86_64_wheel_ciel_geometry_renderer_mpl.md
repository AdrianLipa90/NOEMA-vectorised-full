# renderer_mpl.py — build/bdist.linux-x86_64/wheel/ciel_geometry/renderer_mpl.py

## Tożsamość
- **id_karty:** `REPO-RENDERER_MPL-AAE3`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/renderer_mpl.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.595`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/renderer_mpl.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.595 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Matplotlib Poincaré disk renderer — interactive orbital cockpit (Foundation Pack P6 MVP).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_node_label`, `_health_bar`, `render`, `_parse_args`, `main`

## Opis
Matplotlib Poincaré disk renderer — interactive orbital cockpit (Foundation Pack P6 MVP).

Usage:
    python -m ciel_geometry.renderer_mpl              # static snapshot
    python -m ciel_geometry.renderer_mpl --live       # auto-refresh every 5s
    python -m ciel_geometry.renderer_mpl --save out.png
