# glifLib.py — .python_packages/fontTools/ufoLib/glifLib.py

## Tożsamość
- **id_karty:** `REPO-GLIFLIB-4E4D`
- **ścieżka:** `.python_packages/fontTools/ufoLib/glifLib.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.393`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/ufoLib/glifLib.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.393 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Generic module for reading and writing the .glif format.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GLIFFormatVersion, Glyph, GlyphSet, _DoneParsing, _BaseParser, _FetchUnicodesParser, _FetchImageFileNameParser, _FetchComponentBasesParser, GLIFPointPen
- **funkcje:** `glyphNameToFileName`, `readGlyphFromString`, `_writeGlyphToBytes`, `writeGlyphToString`, `_writeAdvance`, `_writeUnicodes`, `_writeNote`, `_writeImage`, `_writeGuidelines`, `_writeAnchorsFormat1`, `_writeAnchors`, `_writeLib`, `validateLayerInfoVersion3ValueForAttribute`, `validateLayerInfoVersion3Data`, `_glifTreeFromFile`, `_glifTreeFromString`, `_readGlyphFromTree`, `_readGlyphFromTreeFormat1`, `_readGlyphFromTreeFormat2`, `_readName`, `_readAdvance`, `_readNote`, `_readLib`, `_readImage`, `buildOutlineFormat1`, `_buildAnchorFormat1`, `_buildOutlineContourFormat1`, `_buildOutlinePointsFormat1`, `_buildOutlineComponentFormat1`, `buildOutlineFormat2`

## Opis
Generic module for reading and writing the .glif format.

More info about the .glif format (GLyphInterchangeFormat) can be found here:

        http://unifiedfontobject.org

The main class in this module is :class:`GlyphSet`. It manages a set of .glif files
in a folder. It offers two ways to read glyph data, and one way to write
glyph data. See the class doc string for details.
