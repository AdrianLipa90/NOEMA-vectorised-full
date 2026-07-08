# ciel_launch.py — scripts/ciel_launch.py

## Tożsamość
- **id_karty:** `REPO-CIEL_LAUNCH-C9D2`
- **ścieżka:** `scripts/ciel_launch.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.979`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_launch.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.979 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
CIEL/Ω System Launcher

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `ensure_gui_deps`, `start_pipeline`, `create_desktop_file`, `main`, `_open_browser`

## Opis
CIEL/Ω System Launcher

Uruchamia cały system CIEL:
  1. Sprawdza i instaluje zależności GUI
  2. Uruchamia CIEL pipeline (synchronize → orbital_bridge) w tle
  3. Otwiera GUI NiceGUI z ikoną Logo1.png w przeglądarce

Użycie:
    python scripts/ciel_launch.py
    python scripts/ciel_launch.py --no-pipeline   # tylko GUI
    python scripts/ciel_launch.py --port 9090
