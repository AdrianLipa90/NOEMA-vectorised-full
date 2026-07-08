# wigner.py — .python_packages/sympy/physics/wigner.py

## Tożsamość
- **id_karty:** `REPO-WIGNER-83B5`
- **ścieżka:** `.python_packages/sympy/physics/wigner.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.184`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/wigner.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.184 |
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
Wigner, Clebsch-Gordan, Racah, and Gaunt coefficients

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Wigner3j
- **funkcje:** `_calc_factlist`, `_int_or_halfint`, `wigner_3j`, `clebsch_gordan`, `_big_delta_coeff`, `racah`, `wigner_6j`, `wigner_9j`, `gaunt`, `real_gaunt`, `dot_rot_grad_Ynm`, `wigner_d_small`, `wigner_d`, `doit`, `alpha`

## Opis
Wigner, Clebsch-Gordan, Racah, and Gaunt coefficients

Collection of functions for calculating Wigner 3j, 6j, 9j,
Clebsch-Gordan, Racah as well as Gaunt coefficients exactly, all
evaluating to a rational number times the square root of a rational
number [Rasch03]_.

Please see the description of the individual functions for further
details and examples.

References
==========

.. [Regge58] 'Symmet
