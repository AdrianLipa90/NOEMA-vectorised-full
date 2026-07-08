# units.py — .python_packages/matplotlib/units.py

## Tożsamość
- **id_karty:** `REPO-UNITS-AC6F`
- **ścieżka:** `.python_packages/matplotlib/units.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.020`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/units.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.020 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
The classes here provide support for using custom classes with

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ConversionError, AxisInfo, ConversionInterface, DecimalConverter, Registry
- **funkcje:** `_is_natively_supported`, `axisinfo`, `default_units`, `convert`, `convert`, `get_converter`

## Opis
The classes here provide support for using custom classes with
Matplotlib, e.g., those that do not expose the array interface but know
how to convert themselves to arrays.  It also supports classes with
units and units conversion.  Use cases include converters for custom
objects, e.g., a list of datetime objects, as well as for objects that
are unit aware.  We don't assume any particular units imp
