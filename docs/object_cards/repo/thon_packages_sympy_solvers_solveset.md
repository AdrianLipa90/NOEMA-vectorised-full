# solveset.py — .python_packages/sympy/solvers/solveset.py

## Tożsamość
- **id_karty:** `REPO-SOLVESET-F6E4`
- **ścieżka:** `.python_packages/sympy/solvers/solveset.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.521`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/solvers/solveset.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.521 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
This module contains functions to:

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NonlinearError, _SolveTrig1Error
- **funkcje:** `_masked`, `_invert`, `invert_real`, `_invert_real`, `_invert_trig_hyp_real`, `_invert_trig_hyp_complex`, `_invert_complex`, `_invert_abs`, `domain_check`, `_domain_check`, `_is_finite_with_finite_vars`, `_is_function_class_equation`, `_solve_as_rational`, `_solve_trig`, `_solve_trig1`, `_solve_trig2`, `_solve_as_poly`, `_solve_radical`, `_solve_abs`, `solve_decomposition`, `_solveset`, `_is_modular`, `_invert_modular`, `_solve_modular`, `_term_factors`, `_solve_exponential`, `_is_exponential`, `_solve_logarithm`, `_is_logarithmic`, `_is_lambert`

## Opis
This module contains functions to:

    - solve a single equation for a single variable, in any domain either real or complex.

    - solve a single transcendental equation for a single variable in any domain either real or complex.
      (currently supports solving in real domain only)

    - solve a system of linear equations with N variables and M equations.

    - solve a system of Non Linear
