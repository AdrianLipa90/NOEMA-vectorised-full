# builder.py — .python_packages/fontTools/colorLib/builder.py

## Tożsamość
- **id_karty:** `REPO-BUILDER-1298`
- **ścieżka:** `.python_packages/fontTools/colorLib/builder.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.707`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/colorLib/builder.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.707 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
colorLib.builder: Build COLR/CPAL tables from scratch

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ColorPaletteType, LayerReuseCache, LayerListBuilder
- **funkcje:** `_beforeBuildPaintRadialGradient`, `_defaultColorStop`, `_defaultVarColorStop`, `_defaultColorLine`, `_defaultVarColorLine`, `_defaultPaintSolid`, `_buildPaintCallbacks`, `populateCOLRv0`, `buildCOLR`, `buildClipList`, `buildClipBox`, `buildPaletteLabels`, `buildCPAL`, `_is_colrv0_layer`, `_split_color_glyphs_by_version`, `_reuse_ranges`, `buildBaseGlyphPaintRecord`, `_check_base_glyphs_exist`, `_format_glyph_errors`, `buildColrV1`, `_missing_`, `_paint_tuple`, `_as_tuple`, `try_reuse`, `add`, `_beforeBuildPaintColrLayers`, `buildPaint`, `build`, `_tuple_safe`, `listToColrLayers`

## Opis
colorLib.builder: Build COLR/CPAL tables from scratch
