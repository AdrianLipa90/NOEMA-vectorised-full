# capture_cli.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/capture_cli.py

## Tożsamość
- **id_karty:** `REPO-CAPTURE_CLI-763E`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/capture_cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.973`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/capture_cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.973 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
ciel-sot-capture — szybki zapis idei do WPM i ideas_capture.md.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_project_root`, `_write_to_wpm`, `_write_to_ideas`, `main`

## Opis
ciel-sot-capture — szybki zapis idei do WPM i ideas_capture.md.

Użycie:
  ciel-sot-capture "fragment idei"
  ciel-sot-capture --type anchor "zasada etyczna"
  ciel-sot-capture --context "sesja-2026-04-16" "pomysł na optymalizację"
