# hermite.py — .python_packages/numpy/polynomial/hermite.py

## Tożsamość
- **id_karty:** `REPO-HERMITE-A6D4`
- **ścieżka:** `.python_packages/numpy/polynomial/hermite.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.020`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/polynomial/hermite.py`

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
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
==============================================================

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Hermite
- **funkcje:** `poly2herm`, `herm2poly`, `hermline`, `hermfromroots`, `hermadd`, `hermsub`, `hermmulx`, `hermmul`, `hermdiv`, `hermpow`, `hermder`, `hermint`, `hermval`, `hermval2d`, `hermgrid2d`, `hermval3d`, `hermgrid3d`, `hermvander`, `hermvander2d`, `hermvander3d`, `hermfit`, `hermcompanion`, `hermroots`, `_normed_hermite_n`, `hermgauss`, `hermweight`

## Opis
==============================================================
Hermite Series, "Physicists" (:mod:`numpy.polynomial.hermite`)
==============================================================

This module provides a number of objects (mostly functions) useful for
dealing with Hermite series, including a `Hermite` class that
encapsulates the usual arithmetic operations.  (General information
on how th
