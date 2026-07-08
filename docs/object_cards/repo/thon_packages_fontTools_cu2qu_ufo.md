# ufo.py — .python_packages/fontTools/cu2qu/ufo.py

## Tożsamość
- **id_karty:** `REPO-UFO-A777`
- **ścieżka:** `.python_packages/fontTools/cu2qu/ufo.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.918`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/cu2qu/ufo.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.918 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
Converts cubic bezier curves to quadratic splines.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GetSegmentsPen
- **funkcje:** `zip`, `_validate_positive_tolerance`, `_validate_positive_tolerances`, `_validate_length`, `_get_segments`, `_set_segments`, `_segments_to_quadratic`, `_glyphs_to_quadratic`, `glyphs_to_quadratic`, `fonts_to_quadratic`, `glyph_to_quadratic`, `font_to_quadratic`, `_add_segment`, `moveTo`, `lineTo`, `qCurveTo`, `curveTo`, `closePath`, `endPath`, `addComponent`

## Opis
Converts cubic bezier curves to quadratic splines.

Conversion is performed such that the quadratic splines keep the same end-curve
tangents as the original cubics. The approach is iterative, increasing the
number of segments for a spline until the error gets below a bound.

Respective curves from multiple fonts will be converted at once to ensure that
the resulting splines are interpolation-compa
