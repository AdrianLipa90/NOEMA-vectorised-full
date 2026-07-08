# BlpImagePlugin.py — .python_packages/PIL/BlpImagePlugin.py

## Tożsamość
- **id_karty:** `REPO-BLPIMAGEPLUGIN-6304`
- **ścieżka:** `.python_packages/PIL/BlpImagePlugin.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.753`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/PIL/BlpImagePlugin.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.753 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Blizzard Mipmap Format (.blp)

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Format, Encoding, AlphaEncoding, BLPFormatError, BlpImageFile, _BLPBaseDecoder, BLP1Decoder, BLP2Decoder, BLPEncoder
- **funkcje:** `unpack_565`, `decode_dxt1`, `decode_dxt3`, `decode_dxt5`, `_accept`, `_save`, `_open`, `decode`, `_load`, `_read_header`, `_safe_read`, `_read_palette`, `_read_bgra`, `_load`, `_decode_jpeg_stream`, `_load`, `_write_palette`, `encode`

## Opis
Blizzard Mipmap Format (.blp)
Jerome Leclanche <jerome@leclan.ch>

The contents of this file are hereby released in the public domain (CC0)
Full text of the CC0 license:
  https://creativecommons.org/publicdomain/zero/1.0/

BLP1 files, used mostly in Warcraft III, are not fully supported.
All types of BLP2 files used in World of Warcraft are supported.

The BLP file structure consists of a header,
