# polynomial.py — .python_packages/numpy/polynomial/polynomial.py

## Tożsamość
- **id_karty:** `REPO-POLYNOMIAL-8511`
- **ścieżka:** `.python_packages/numpy/polynomial/polynomial.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.999`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/polynomial/polynomial.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.999 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
=================================================

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Polynomial
- **funkcje:** `polyline`, `polyfromroots`, `polyadd`, `polysub`, `polymulx`, `polymul`, `polydiv`, `polypow`, `polyder`, `polyint`, `polyval`, `polyvalfromroots`, `_polyval2d_dispatcher`, `_polygrid2d_dispatcher`, `polyval2d`, `polygrid2d`, `polyval3d`, `polygrid3d`, `polyvander`, `polyvander2d`, `polyvander3d`, `polyfit`, `polycompanion`, `polyroots`, `_str_term_unicode`, `_str_term_ascii`, `_repr_latex_term`

## Opis
=================================================
Power Series (:mod:`numpy.polynomial.polynomial`)
=================================================

This module provides a number of objects (mostly functions) useful for
dealing with polynomials, including a `Polynomial` class that
encapsulates the usual arithmetic operations.  (General information
on how this module represents and works with pol
