# _codata.py — .python_packages/scipy/constants/_codata.py

## Tożsamość
- **id_karty:** `REPO-_CODATA-055F`
- **ścieżka:** `.python_packages/scipy/constants/_codata.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.842`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/constants/_codata.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.842 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
Fundamental Physical Constants

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ConstantWarning
- **funkcje:** `exact2002`, `exact2006`, `exact2018`, `parse_constants_2002to2014`, `parse_constants_2018toXXXX`, `replace_exact`, `_check_obsolete`, `value`, `unit`, `precision`, `find`

## Opis
Fundamental Physical Constants
------------------------------

These constants are taken from CODATA Recommended Values of the Fundamental
Physical Constants 2022.

Object
------
physical_constants : dict
    A dictionary containing physical constants. Keys are the names of physical
    constants, values are tuples (value, units, precision).

Functions
---------
value(key):
    Returns the value o
