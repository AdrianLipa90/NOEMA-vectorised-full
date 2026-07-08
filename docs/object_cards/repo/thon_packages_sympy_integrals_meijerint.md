# meijerint.py — .python_packages/sympy/integrals/meijerint.py

## Tożsamość
- **id_karty:** `REPO-MEIJERINT-62CB`
- **ścieżka:** `.python_packages/sympy/integrals/meijerint.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.881`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/integrals/meijerint.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.881 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Integrate functions by rewriting them as Meijer G-functions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _CoeffExpValueError, IsNonPositiveInteger
- **funkcje:** `_has`, `_create_lookup_table`, `_mytype`, `_get_coeff_exp`, `_exponents`, `_functions`, `_find_splitting_points`, `_split_mul`, `_mul_args`, `_mul_as_two_parts`, `_inflate_g`, `_flip_g`, `_inflate_fox_h`, `_dummy`, `_dummy_`, `_is_analytic`, `_condsimp`, `_eval_cond`, `_my_principal_branch`, `_rewrite_saxena_1`, `_check_antecedents_1`, `_int0oo_1`, `_rewrite_saxena`, `_check_antecedents`, `_int0oo`, `_rewrite_inversion`, `_check_antecedents_inversion`, `_int_inversion`, `_rewrite_single`, `_rewrite1`

## Opis
Integrate functions by rewriting them as Meijer G-functions.

There are three user-visible functions that can be used by other parts of the
sympy library to solve various integration problems:

- meijerint_indefinite
- meijerint_definite
- meijerint_inversion

They can be used to compute, respectively, indefinite integrals, definite
integrals over intervals of the real line, and inverse laplace-ty
