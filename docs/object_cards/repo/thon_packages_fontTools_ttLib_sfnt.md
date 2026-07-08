# sfnt.py — .python_packages/fontTools/ttLib/sfnt.py

## Tożsamość
- **id_karty:** `REPO-SFNT-04F0`
- **ścieżka:** `.python_packages/fontTools/ttLib/sfnt.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.808`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/ttLib/sfnt.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.808 |
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
ttLib/sfnt.py -- low-level module to deal with the sfnt file format.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SFNTReader, SFNTWriter, DirectoryEntry, SFNTDirectoryEntry, WOFFDirectoryEntry, WOFFFlavorData
- **funkcje:** `compress`, `calcChecksum`, `readTTCHeader`, `writeTTCHeader`, `has_key`, `keys`, `close`, `setEntry`, `close`, `_calcMasterChecksum`, `writeMasterChecksum`, `reordersTables`, `fromFile`, `fromString`, `toString`, `loadData`, `saveData`, `decodeData`, `encodeData`, `decodeData`, `encodeData`, `_decompress`

## Opis
ttLib/sfnt.py -- low-level module to deal with the sfnt file format.

Defines two public classes:

- SFNTReader
- SFNTWriter

(Normally you don't have to use these classes explicitly; they are
used automatically by ttLib.TTFont.)

The reading and writing of sfnt files is separated in two distinct
classes, since whenever the number of tables changes or whenever
a table's length changes you need to
