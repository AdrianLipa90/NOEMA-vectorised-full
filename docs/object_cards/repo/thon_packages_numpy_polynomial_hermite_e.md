# hermite_e.py — .python_packages/numpy/polynomial/hermite_e.py

## Tożsamość
- **id_karty:** `REPO-HERMITE_E-002F`
- **ścieżka:** `.python_packages/numpy/polynomial/hermite_e.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.678`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/polynomial/hermite_e.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.678 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
===================================================================

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** HermiteE
- **funkcje:** `poly2herme`, `herme2poly`, `hermeline`, `hermefromroots`, `hermeadd`, `hermesub`, `hermemulx`, `hermemul`, `hermediv`, `hermepow`, `hermeder`, `hermeint`, `hermeval`, `hermeval2d`, `hermegrid2d`, `hermeval3d`, `hermegrid3d`, `hermevander`, `hermevander2d`, `hermevander3d`, `hermefit`, `hermecompanion`, `hermeroots`, `_normed_hermite_e_n`, `hermegauss`, `hermeweight`

## Opis
===================================================================
HermiteE Series, "Probabilists" (:mod:`numpy.polynomial.hermite_e`)
===================================================================

This module provides a number of objects (mostly functions) useful for
dealing with Hermite_e series, including a `HermiteE` class that
encapsulates the usual arithmetic operations.  (General inf
