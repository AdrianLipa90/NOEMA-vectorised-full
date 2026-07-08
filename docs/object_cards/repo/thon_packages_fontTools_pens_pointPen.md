# pointPen.py — .python_packages/fontTools/pens/pointPen.py

## Tożsamość
- **id_karty:** `REPO-POINTPEN-8DC3`
- **ścieżka:** `.python_packages/fontTools/pens/pointPen.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.159`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/pens/pointPen.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.159 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
=========

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ReverseFlipped, AbstractPointPen, BasePointToSegmentPen, PointToSegmentPen, SegmentToPointPen, GuessSmoothPointPen, ReverseContourPointPen, DecomposingPointPen
- **funkcje:** `beginPath`, `endPath`, `addPoint`, `addComponent`, `addVarComponent`, `beginPath`, `_flushContour`, `endPath`, `addPoint`, `_flushContour`, `addComponent`, `_flushContour`, `moveTo`, `lineTo`, `curveTo`, `qCurveTo`, `closePath`, `endPath`, `addComponent`, `_flushContour`, `beginPath`, `endPath`, `addPoint`, `addComponent`, `addVarComponent`, `_flushContour`, `beginPath`, `endPath`, `addPoint`, `addComponent`

## Opis
=========
PointPens
=========

Where **SegmentPens** have an intuitive approach to drawing
(if you're familiar with postscript anyway), the **PointPen**
is geared towards accessing all the data in the contours of
the glyph. A PointPen has a very simple interface, it just
steps through all the points in a call from glyph.drawPoints().
This allows the caller to provide more data for each point.
For
