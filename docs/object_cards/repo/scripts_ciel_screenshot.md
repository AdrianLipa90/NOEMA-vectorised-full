# ciel_screenshot.py — scripts/ciel_screenshot.py

## Tożsamość
- **id_karty:** `REPO-CIEL_SCREENSHOT-86BD`
- **ścieżka:** `scripts/ciel_screenshot.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.992`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_screenshot.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.992 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Robi screenshot strony CIEL i zapisuje do ~/.claude/ciel_site/screenshot.png

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `screenshot`

## Opis
Robi screenshot strony CIEL i zapisuje do ~/.claude/ciel_site/screenshot.png

Użycie:
  python3 scripts/ciel_screenshot.py                    # domyślna strona CIEL
  python3 scripts/ciel_screenshot.py file:///path.html  # własny URL
  python3 scripts/ciel_screenshot.py <url> <out.png>    # własny URL i output

Wymaga: playwright + chromium
  pip install playwright
  playwright install chromium --
