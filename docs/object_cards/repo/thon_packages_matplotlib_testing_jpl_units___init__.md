# __init__.py — .python_packages/matplotlib/testing/jpl_units/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-2C7F`
- **ścieżka:** `.python_packages/matplotlib/testing/jpl_units/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.605`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/testing/jpl_units/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.605 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
A sample set of units for use with testing unit conversion

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `register`

## Opis
A sample set of units for use with testing unit conversion
of Matplotlib routines.  These are used because they use very strict
enforcement of unitized data which will test the entire spectrum of how
unitized data might be used (it is not always meaningful to convert to
a float without specific units given).

UnitDbl is essentially a unitized floating point number.  It has a
minimal set of support
