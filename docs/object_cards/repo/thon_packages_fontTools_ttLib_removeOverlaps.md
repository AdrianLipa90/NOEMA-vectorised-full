# removeOverlaps.py — .python_packages/fontTools/ttLib/removeOverlaps.py

## Tożsamość
- **id_karty:** `REPO-REMOVEOVERLAPS-007A`
- **ścieżka:** `.python_packages/fontTools/ttLib/removeOverlaps.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.979`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/ttLib/removeOverlaps.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.979 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Simplify TrueType glyphs by merging overlapping contours/components.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RemoveOverlapsError
- **funkcje:** `skPathFromGlyph`, `skPathFromGlyphComponent`, `componentsOverlap`, `ttfGlyphFromSkPath`, `_charString_from_SkPath`, `_round_path`, `_simplify`, `_same_path`, `removeTTGlyphOverlaps`, `_remove_glyf_overlaps`, `_remove_charstring_overlaps`, `_remove_cff_overlaps`, `removeOverlaps`, `main`, `_get_nth_component_path`

## Opis
Simplify TrueType glyphs by merging overlapping contours/components.

Requires https://github.com/fonttools/skia-pathops
