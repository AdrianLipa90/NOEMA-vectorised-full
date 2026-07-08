# noema_watchdog.py — scripts/noema_watchdog.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_WATCHDOG-7208`
- **ścieżka:** `scripts/noema_watchdog.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.500`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_watchdog.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.500 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
NOEMA Watchdog — trzyma wszystkie daemony przy życiu.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Watchdog
- **funkcje:** `_start`, `check`, `start_all`, `stop_all`, `run`, `_handler`

## Opis
NOEMA Watchdog — trzyma wszystkie daemony przy życiu.

Jeśli któryś padnie, restartuje go. Sprawdza co 30s.
