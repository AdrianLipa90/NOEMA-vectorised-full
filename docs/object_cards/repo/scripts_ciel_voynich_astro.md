# ciel_voynich_astro.py — scripts/ciel_voynich_astro.py

## Tożsamość
- **id_karty:** `REPO-CIEL_VOYNICH_ASTRO-76CF`
- **ścieżka:** `scripts/ciel_voynich_astro.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.426`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_voynich_astro.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.426 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
ciel_voynich_astro.py — Voynich astro section vs. sky from TRAPPIST-1f

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_trappist1_xyz`, `load_bright_stars`, `shift_to_trappist1`, `voynich_circular_layout`, `render`, `main`

## Opis
ciel_voynich_astro.py — Voynich astro section vs. sky from TRAPPIST-1f

Hypothesis (Bio_manuscrypt2.pdf, STARS §5):
  The Voynich astronomical diagrams show the sky as seen from a planet
  in a trinary/binary star system — candidate: TRAPPIST-1 (39.5 ly).

Method:
  1. Load Yale Bright Star Catalogue (built into astropy) — ~9000 stars, mag < 6.5
  2. Transform coordinates: shift origin from Sol →
