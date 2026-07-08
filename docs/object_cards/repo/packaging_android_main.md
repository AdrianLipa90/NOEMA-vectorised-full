# main.py — packaging/android/main.py

## Tożsamość
- **id_karty:** `REPO-MAIN-D673`
- **ścieżka:** `packaging/android/main.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.011`
- **masa_semantyczna:** `0.40`

## Kotwice
- `packaging/android/main.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.011 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
CIEL Orbital Control — Android entry point (Kivy).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ControlScreen, SettingsScreen, CIELOrbitalApp
- **funkcje:** `main`, `build`, `on_start`, `refresh_status`, `_fetch_status`, `_apply_status`

## Opis
CIEL Orbital Control — Android entry point (Kivy).

This module provides a lightweight Kivy-based Android companion for the CIEL
SOT Agent.  It connects to a running ciel-sot-gui Flask server (on the same
local network or localhost via ADB forward) and displays the key observables
in a native Android UI following the Quiet Orbital Control identity.

Build with Buildozer (see packaging/android/buil
