# hyperexpand.py — .python_packages/sympy/simplify/hyperexpand.py

## Tożsamość
- **id_karty:** `REPO-HYPEREXPAND-ADD8`
- **ścieżka:** `.python_packages/sympy/simplify/hyperexpand.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.245`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/simplify/hyperexpand.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.245 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
Expand Hypergeometric (and Meijer G) functions into named

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Hyper_Function, G_Function, Formula, FormulaCollection, MeijerFormula, MeijerFormulaCollection, Operator, MultOperator, ShiftA, ShiftB, UnShiftA, UnShiftB, MeijerShiftA, MeijerShiftB, MeijerShiftC, MeijerShiftD, MeijerUnShiftA, MeijerUnShiftB, MeijerUnShiftC, MeijerUnShiftD
- **funkcje:** `_mod1`, `add_formulae`, `add_meijerg_formulae`, `make_simp`, `debug`, `_reduce_order`, `reduce_order`, `reduce_order_meijer`, `make_derivative_operator`, `apply_operators`, `devise_plan`, `try_shifted_sum`, `try_polynomial`, `try_lerchphi`, `build_hypergeometric_formula`, `hyperexpand_special`, `_hyperexpand`, `devise_plan_meijer`, `_meijergexpand`, `hyperexpand`, `add`, `addb`, `fp`, `fm`, `add`, `detect_uppergamma`, `detect_3113`, `simp`, `args`, `sizes`

## Opis
Expand Hypergeometric (and Meijer G) functions into named
special functions.

The algorithm for doing this uses a collection of lookup tables of
hypergeometric functions, and various of their properties, to expand
many hypergeometric functions in terms of special functions.

It is based on the following paper:
      Kelly B. Roach.  Meijer G Function Representations.
      In: Proceedings of the 1
