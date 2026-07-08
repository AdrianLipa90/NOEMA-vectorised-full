# capture_cli.py — src/ciel_sot_agent/capture_cli.py

## Tożsamość
- **id_karty:** `REPO-CAPTURE_CLI-C61F`
- **ścieżka:** `src/ciel_sot_agent/capture_cli.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.047`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/capture_cli.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.047 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


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
