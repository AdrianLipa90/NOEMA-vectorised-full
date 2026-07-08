# __init__.py — .python_packages/fontTools/t1Lib/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-7E04`
- **ścieżka:** `.python_packages/fontTools/t1Lib/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.028`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/t1Lib/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.028 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
fontTools.t1Lib.py -- Tools for PostScript Type 1 fonts.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** T1Error, T1Font
- **funkcje:** `read`, `write`, `readLWFN`, `readPFB`, `readOther`, `writeLWFN`, `writePFB`, `writeOther`, `isHex`, `decryptType1`, `findEncryptedChunks`, `deHexString`, `assertType1`, `longToString`, `stringToLong`, `saveAs`, `getData`, `getGlyphSet`, `parse`, `createData`, `encode_eexec`, `_make_lines`, `_tobytes`

## Opis
fontTools.t1Lib.py -- Tools for PostScript Type 1 fonts.

Functions for reading and writing raw Type 1 data:

read(path)
        reads any Type 1 font file, returns the raw data and a type indicator:
        'LWFN', 'PFB' or 'OTHER', depending on the format of the file pointed
        to by 'path'.
        Raises an error when the file does not contain valid Type 1 data.

write(path, data, kind='O
