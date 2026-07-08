# math2.py — .python_packages/mpmath/math2.py

## Tożsamość
- **id_karty:** `REPO-MATH2-C3A1`
- **ścieżka:** `.python_packages/mpmath/math2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.574`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpmath/math2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.574 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
This module complements the math and cmath builtin modules by providing

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_mathfun_real`, `_mathfun`, `_mathfun_n`, `nthroot`, `_sinpi_real`, `_cospi_real`, `_sinpi_complex`, `_cospi_complex`, `tanpi`, `cotpi`, `_gamma_real`, `_gamma_complex`, `rgamma`, `factorial`, `arg`, `loggamma`, `_digamma_real`, `_digamma_complex`, `_polyval`, `_erf_taylor`, `_erfc_mid`, `_erfc_asymp`, `erf`, `erfc`, `ei_asymp`, `ei_taylor`, `ei`, `e1`, `zeta`, `f`

## Opis
This module complements the math and cmath builtin modules by providing
fast machine precision versions of some additional functions (gamma, ...)
and wrapping math/cmath functions so that they can be called with either
real or complex arguments.
