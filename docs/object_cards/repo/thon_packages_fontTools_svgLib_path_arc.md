# arc.py — .python_packages/fontTools/svgLib/path/arc.py

## Tożsamość
- **id_karty:** `REPO-ARC-0885`
- **ścieżka:** `.python_packages/fontTools/svgLib/path/arc.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.103`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/svgLib/path/arc.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.103 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Convert SVG Path's elliptical arcs to Bezier curves.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** EllipticalArc
- **funkcje:** `_map_point`, `_parametrize`, `_decompose_to_cubic_curves`, `draw`

## Opis
Convert SVG Path's elliptical arcs to Bezier curves.

The code is mostly adapted from Blink's SVGPathNormalizer::DecomposeArcToCubic
https://github.com/chromium/chromium/blob/93831f2/third_party/
blink/renderer/core/svg/svg_path_parser.cc#L169-L278
