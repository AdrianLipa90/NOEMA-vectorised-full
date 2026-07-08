# basePen.py — .python_packages/fontTools/pens/basePen.py

## Tożsamość
- **id_karty:** `REPO-BASEPEN-7E1E`
- **ścieżka:** `.python_packages/fontTools/pens/basePen.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.494`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/pens/basePen.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.494 |
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
fontTools.pens.basePen.py -- Tools and base classes to build pen objects.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PenError, OpenContourError, AbstractPen, NullPen, LoggingPen, MissingComponentError, DecomposingPen, BasePen, _TestPen
- **funkcje:** `decomposeSuperBezierSegment`, `decomposeQuadraticSegment`, `moveTo`, `lineTo`, `curveTo`, `qCurveTo`, `closePath`, `endPath`, `addComponent`, `addVarComponent`, `moveTo`, `lineTo`, `curveTo`, `qCurveTo`, `closePath`, `endPath`, `addComponent`, `addVarComponent`, `addComponent`, `addVarComponent`, `_moveTo`, `_lineTo`, `_curveToOne`, `_closePath`, `_endPath`, `_qCurveToOne`, `_getCurrentPoint`, `closePath`, `endPath`, `moveTo`

## Opis
fontTools.pens.basePen.py -- Tools and base classes to build pen objects.

The Pen Protocol

A Pen is a kind of object that standardizes the way how to "draw" outlines:
it is a middle man between an outline and a drawing. In other words:
it is an abstraction for drawing outlines, making sure that outline objects
don't need to know the details about how and where they're being drawn, and
that drawi
