# __init__.py — .python_packages/fontTools/ufoLib/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-779E`
- **ścieżka:** `.python_packages/fontTools/ufoLib/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.618`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/ufoLib/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.618 |
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
A library for importing .ufo files and their descendants.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UFOFormatVersion, UFOFileStructure, _UFOBaseIO, UFOReader, UFOWriter
- **funkcje:** `_sniffFileStructure`, `makeUFOPath`, `validateFontInfoVersion2ValueForAttribute`, `validateInfoVersion2Data`, `validateFontInfoVersion3ValueForAttribute`, `validateInfoVersion3Data`, `_flipDict`, `convertFontInfoValueForAttributeFromVersion1ToVersion2`, `convertFontInfoValueForAttributeFromVersion2ToVersion1`, `_convertFontInfoDataVersion1ToVersion2`, `_convertFontInfoDataVersion2ToVersion1`, `convertFontInfoValueForAttributeFromVersion2ToVersion3`, `convertFontInfoValueForAttributeFromVersion3ToVersion2`, `_convertFontInfoDataVersion3ToVersion2`, `_convertFontInfoDataVersion2ToVersion3`, `getFileModificationTime`, `_getPlist`, `_writePlist`, `_get_path`, `_get_formatVersion`, `formatVersionTuple`, `_get_fileStructure`, `_upConvertKerning`, `readBytesFromPath`, `getReadFileForPath`, `_readMetaInfo`, `readMetaInfo`, `_readGroups`, `readGroups`, `getKerningGroupConversionRenameMaps`

## Opis
A library for importing .ufo files and their descendants.
Refer to http://unifiedfontobject.org for the UFO specification.

The main interfaces are the :class:`.UFOReader` and :class:`.UFOWriter`
classes, which support versions 1, 2, and 3 of the UFO specification.

Set variables are available for external use that list the font
info attribute names for the `fontinfo.plist` formats. These are:

-
