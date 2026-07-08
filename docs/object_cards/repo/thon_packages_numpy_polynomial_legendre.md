# legendre.py — .python_packages/numpy/polynomial/legendre.py

## Tożsamość
- **id_karty:** `REPO-LEGENDRE-5A0E`
- **ścieżka:** `.python_packages/numpy/polynomial/legendre.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.751`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/polynomial/legendre.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.751 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
==================================================

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Legendre
- **funkcje:** `poly2leg`, `leg2poly`, `legline`, `legfromroots`, `legadd`, `legsub`, `legmulx`, `legmul`, `legdiv`, `legpow`, `legder`, `legint`, `legval`, `legval2d`, `leggrid2d`, `legval3d`, `leggrid3d`, `legvander`, `legvander2d`, `legvander3d`, `legfit`, `legcompanion`, `legroots`, `leggauss`, `legweight`

## Opis
==================================================
Legendre Series (:mod:`numpy.polynomial.legendre`)
==================================================

This module provides a number of objects (mostly functions) useful for
dealing with Legendre series, including a `Legendre` class that
encapsulates the usual arithmetic operations.  (General information
on how this module represents and works wit
