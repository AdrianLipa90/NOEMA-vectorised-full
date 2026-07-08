# polyutils.py — .python_packages/numpy/polynomial/polyutils.py

## Tożsamość
- **id_karty:** `REPO-POLYUTILS-01DD`
- **ścieżka:** `.python_packages/numpy/polynomial/polyutils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.617`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/polynomial/polyutils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.617 |
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
Utility classes and functions for the polynomial modules.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `trimseq`, `as_series`, `trimcoef`, `getdomain`, `mapparms`, `mapdomain`, `_nth_slice`, `_vander_nd`, `_vander_nd_flat`, `_fromroots`, `_valnd`, `_gridnd`, `_div`, `_add`, `_sub`, `_fit`, `_pow`, `_as_int`, `format_float`

## Opis
Utility classes and functions for the polynomial modules.

This module provides: error and warning objects; a polynomial base class;
and some routines used in both the `polynomial` and `chebyshev` modules.

Functions
---------

.. autosummary::
   :toctree: generated/

   as_series    convert list of array_likes into 1-D arrays of common type.
   trimseq      remove trailing zeros.
   trimcoef
