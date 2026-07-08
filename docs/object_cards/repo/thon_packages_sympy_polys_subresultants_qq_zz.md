# subresultants_qq_zz.py — .python_packages/sympy/polys/subresultants_qq_zz.py

## Tożsamość
- **id_karty:** `REPO-SUBRESULTANTS_QQ_ZZ-20A4`
- **ścieżka:** `.python_packages/sympy/polys/subresultants_qq_zz.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.037`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/subresultants_qq_zz.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.037 |
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
This module contains functions for the computation

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `sylvester`, `process_matrix_output`, `subresultants_sylv`, `modified_subresultants_sylv`, `res`, `res_q`, `res_z`, `sign_seq`, `bezout`, `backward_eye`, `subresultants_bezout`, `modified_subresultants_bezout`, `sturm_pg`, `sturm_q`, `sturm_amv`, `euclid_pg`, `euclid_q`, `euclid_amv`, `modified_subresultants_pg`, `subresultants_pg`, `subresultants_amv_q`, `compute_sign`, `rem_z`, `quo_z`, `subresultants_amv`, `modified_subresultants_amv`, `correct_sign`, `subresultants_rem`, `pivot`, `rotate_r`

## Opis
This module contains functions for the computation
of Euclidean, (generalized) Sturmian, (modified) subresultant
polynomial remainder sequences (prs's) of two polynomials;
included are also three functions for the computation of the
resultant of two polynomials.

Except for the function res_z(), which computes the resultant
of two polynomials, the pseudo-remainder function prem()
of sympy is _not_
