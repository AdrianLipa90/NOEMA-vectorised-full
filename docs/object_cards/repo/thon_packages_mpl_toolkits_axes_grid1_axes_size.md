# axes_size.py — .python_packages/mpl_toolkits/axes_grid1/axes_size.py

## Tożsamość
- **id_karty:** `REPO-AXES_SIZE-69B8`
- **ścieżka:** `.python_packages/mpl_toolkits/axes_grid1/axes_size.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.977`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpl_toolkits/axes_grid1/axes_size.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.977 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Provides classes of simple units that will be used with `.AxesDivider`

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _Base, Add, Fixed, Scaled, AxesX, AxesY, MaxExtent, MaxWidth, MaxHeight, Fraction, _AxesDecorationsSize
- **funkcje:** `_get_axes_aspect`, `from_any`, `get_size`, `get_size`, `get_size`, `get_size`, `get_size`, `get_size`, `add_artist`, `get_size`, `get_size`, `get_size`

## Opis
Provides classes of simple units that will be used with `.AxesDivider`
class (or others) to determine the size of each Axes. The unit
classes define `!get_size` method that returns a tuple of two floats,
meaning relative and absolute sizes, respectively.

Note that this class is nothing more than a simple tuple of two
floats. Take a look at the Divider class to see how these two
values are used.
