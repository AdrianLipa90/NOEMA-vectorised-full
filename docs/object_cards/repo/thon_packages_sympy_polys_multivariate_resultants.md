# multivariate_resultants.py — .python_packages/sympy/polys/multivariate_resultants.py

## Tożsamość
- **id_karty:** `REPO-MULTIVARIATE_RESULTA-C383`
- **ścieżka:** `.python_packages/sympy/polys/multivariate_resultants.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.997`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/multivariate_resultants.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.997 |
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
This module contains functions for two multivariate resultants. These

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DixonResultant, MacaulayResultant
- **funkcje:** `max_degrees`, `get_dixon_polynomial`, `get_upper_degree`, `get_max_degrees`, `get_dixon_matrix`, `KSY_precondition`, `delete_zero_rows_and_columns`, `product_leading_entries`, `get_KSY_Dixon_resultant`, `_get_degree_m`, `get_size`, `get_monomials_of_certain_degree`, `get_row_coefficients`, `get_matrix`, `get_reduced_nonreduced`, `get_submatrix`

## Opis
This module contains functions for two multivariate resultants. These
are:

- Dixon's resultant.
- Macaulay's resultant.

Multivariate resultants are used to identify whether a multivariate
system has common roots. That is when the resultant is equal to zero.
