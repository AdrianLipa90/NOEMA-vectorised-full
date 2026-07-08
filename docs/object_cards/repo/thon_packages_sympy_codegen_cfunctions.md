# cfunctions.py — .python_packages/sympy/codegen/cfunctions.py

## Tożsamość
- **id_karty:** `REPO-CFUNCTIONS-C349`
- **ścieżka:** `.python_packages/sympy/codegen/cfunctions.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.848`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/codegen/cfunctions.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.848 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
This module contains SymPy functions mathcin corresponding to special math functions in the

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** expm1, log1p, exp2, log2, fma, log10, Sqrt, Cbrt, hypot, isnan, isinf
- **funkcje:** `_expm1`, `_log1p`, `_exp2`, `_log2`, `_fma`, `_log10`, `_Sqrt`, `_Cbrt`, `_hypot`, `fdiff`, `_eval_expand_func`, `_eval_rewrite_as_exp`, `eval`, `_eval_is_real`, `_eval_is_finite`, `fdiff`, `_eval_expand_func`, `_eval_rewrite_as_log`, `eval`, `_eval_is_real`, `_eval_is_finite`, `_eval_is_positive`, `_eval_is_zero`, `_eval_is_nonnegative`, `fdiff`, `_eval_rewrite_as_Pow`, `_eval_expand_func`, `eval`, `fdiff`, `eval`

## Opis
This module contains SymPy functions mathcin corresponding to special math functions in the
C standard library (since C99, also available in C++11).

The functions defined in this module allows the user to express functions such as ``expm1``
as a SymPy function for symbolic manipulation.
