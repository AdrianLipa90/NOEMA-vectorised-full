# laguerre.py — .python_packages/numpy/polynomial/laguerre.py

## Tożsamość
- **id_karty:** `REPO-LAGUERRE-802D`
- **ścieżka:** `.python_packages/numpy/polynomial/laguerre.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.858`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/polynomial/laguerre.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.858 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
==================================================

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Laguerre
- **funkcje:** `poly2lag`, `lag2poly`, `lagline`, `lagfromroots`, `lagadd`, `lagsub`, `lagmulx`, `lagmul`, `lagdiv`, `lagpow`, `lagder`, `lagint`, `lagval`, `lagval2d`, `laggrid2d`, `lagval3d`, `laggrid3d`, `lagvander`, `lagvander2d`, `lagvander3d`, `lagfit`, `lagcompanion`, `lagroots`, `laggauss`, `lagweight`

## Opis
==================================================
Laguerre Series (:mod:`numpy.polynomial.laguerre`)
==================================================

This module provides a number of objects (mostly functions) useful for
dealing with Laguerre series, including a `Laguerre` class that
encapsulates the usual arithmetic operations.  (General information
on how this module represents and works wit
