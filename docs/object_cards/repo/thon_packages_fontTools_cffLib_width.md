# width.py — .python_packages/fontTools/cffLib/width.py

## Tożsamość
- **id_karty:** `REPO-WIDTH-FCBA`
- **ścieżka:** `.python_packages/fontTools/cffLib/width.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.929`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/cffLib/width.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.929 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
T2CharString glyph width optimizer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** missingdict
- **funkcje:** `cumSum`, `byteCost`, `optimizeWidthsBruteforce`, `optimizeWidths`, `main`

## Opis
T2CharString glyph width optimizer.

CFF glyphs whose width equals the CFF Private dictionary's ``defaultWidthX``
value do not need to specify their width in their charstring, saving bytes.
This module determines the optimum ``defaultWidthX`` and ``nominalWidthX``
values for a font, when provided with a list of glyph widths.
