# tz.py — .python_packages/dateutil/tz/tz.py

## Tożsamość
- **id_karty:** `REPO-TZ-42A6`
- **ścieżka:** `.python_packages/dateutil/tz/tz.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.310`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/dateutil/tz/tz.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.310 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
This module offers timezone implementations subclassing the abstract

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** tzutc, tzoffset, tzlocal, _ttinfo, _tzfile, tzfile, tzrange, tzstr, _tzicalvtzcomp, _tzicalvtz, tzical, GettzFunc, _nullcontext
- **funkcje:** `datetime_exists`, `datetime_ambiguous`, `resolve_imaginary`, `_datetime_to_timestamp`, `utcoffset`, `dst`, `tzname`, `is_ambiguous`, `fromutc`, `utcoffset`, `dst`, `tzname`, `fromutc`, `is_ambiguous`, `utcoffset`, `dst`, `tzname`, `is_ambiguous`, `_naive_is_dst`, `_isdst`, `_set_tzdata`, `_read_tzfile`, `_find_last_transition`, `_get_ttinfo`, `_find_ttinfo`, `fromutc`, `is_ambiguous`, `_resolve_ambiguous_time`, `utcoffset`, `dst`

## Opis
This module offers timezone implementations subclassing the abstract
:py:class:`datetime.tzinfo` type. There are classes to handle tzfile format
files (usually are in :file:`/etc/localtime`, :file:`/usr/share/zoneinfo`,
etc), TZ environment string (in all known formats), given ranges (with help
from relative deltas), local machine timezone, fixed offset timezone, and UTC
timezone.
