# ciel_natal_chart.py — scripts/ciel_natal_chart.py

## Tożsamość
- **id_karty:** `REPO-CIEL_NATAL_CHART-8C91`
- **ścieżka:** `scripts/ciel_natal_chart.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.097`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_natal_chart.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.097 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
ciel_natal_chart.py — Horoskop natalny zintegrowany z fazami Berry CIEL.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PlanetPos, Aspect
- **funkcje:** `_ephem_planet`, `compute_positions`, `find_aspects`, `_planet_xy`, `render_chart`, `main`, `draw_wheel`

## Opis
ciel_natal_chart.py — Horoskop natalny zintegrowany z fazami Berry CIEL.

Planety jako operatory na przestrzeni fazowej:
  φ_planet = ekliptyczna długość planety / (2π) → faza Berry
  Aspekty   = W_ij między planetami (cosine similarity faz)
  Domy      = 12 sektorów kołowych, każdy z φ_domain

Usage:
    python3 scripts/ciel_natal_chart.py --date 1990-09-28 --time 12:00 --lat 50.06 --lon 19.94
