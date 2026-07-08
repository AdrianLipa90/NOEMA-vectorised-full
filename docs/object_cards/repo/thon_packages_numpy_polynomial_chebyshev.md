# chebyshev.py — .python_packages/numpy/polynomial/chebyshev.py

## Tożsamość
- **id_karty:** `REPO-CHEBYSHEV-B825`
- **ścieżka:** `.python_packages/numpy/polynomial/chebyshev.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.969`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/polynomial/chebyshev.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.969 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
====================================================

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Chebyshev
- **funkcje:** `_cseries_to_zseries`, `_zseries_to_cseries`, `_zseries_mul`, `_zseries_div`, `_zseries_der`, `_zseries_int`, `poly2cheb`, `cheb2poly`, `chebline`, `chebfromroots`, `chebadd`, `chebsub`, `chebmulx`, `chebmul`, `chebdiv`, `chebpow`, `chebder`, `chebint`, `chebval`, `chebval2d`, `chebgrid2d`, `chebval3d`, `chebgrid3d`, `chebvander`, `chebvander2d`, `chebvander3d`, `chebfit`, `chebcompanion`, `chebroots`, `chebinterpolate`

## Opis
====================================================
Chebyshev Series (:mod:`numpy.polynomial.chebyshev`)
====================================================

This module provides a number of objects (mostly functions) useful for
dealing with Chebyshev series, including a `Chebyshev` class that
encapsulates the usual arithmetic operations.  (General information
on how this module represents and w
