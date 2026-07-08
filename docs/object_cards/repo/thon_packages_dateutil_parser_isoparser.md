# isoparser.py — .python_packages/dateutil/parser/isoparser.py

## Tożsamość
- **id_karty:** `REPO-ISOPARSER-EEA7`
- **ścieżka:** `.python_packages/dateutil/parser/isoparser.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.011`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/dateutil/parser/isoparser.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.011 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
This module offers a parser for ISO-8601 strings

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** isoparser
- **funkcje:** `_takes_ascii`, `func`, `isoparse`, `parse_isodate`, `parse_isotime`, `parse_tzstr`, `_parse_isodate`, `_parse_isodate_common`, `_parse_isodate_uncommon`, `_calculate_weekdate`, `_parse_isotime`, `_parse_tzstr`

## Opis
This module offers a parser for ISO-8601 strings

It is intended to support all valid date, time and datetime formats per the
ISO-8601 specification.

..versionadded:: 2.7.0
