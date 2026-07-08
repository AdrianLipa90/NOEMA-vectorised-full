# function.py — .python_packages/sympy/core/function.py

## Tożsamość
- **id_karty:** `REPO-FUNCTION-BA63`
- **ścieżka:** `.python_packages/sympy/core/function.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.080`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/core/function.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.080 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
There are three types of functions implemented in SymPy:

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PoleError, ArgumentIndexError, BadSignatureError, BadArgumentsError, FunctionClass, Application, Function, DefinedFunction, AppliedUndef, UndefSageHelper, UndefinedFunction, WildFunction, Derivative, Lambda, Subs, CustomStrPrinter
- **funkcje:** `_coeff_isneg`, `arity`, `_reduce_undef`, `_rebuild_undef`, `_derivative_dispatch`, `diff`, `expand`, `_mexpand`, `expand_mul`, `expand_multinomial`, `expand_log`, `expand_func`, `expand_trig`, `expand_complex`, `expand_power_base`, `expand_power_exp`, `count_ops`, `nfloat`, `free_symbols`, `xreplace`, `nargs`, `_valid_nargs`, `eval`, `func`, `_eval_subs`, `_diff_wrt`, `_new_`, `_should_evalf`, `class_key`, `_eval_evalf`

## Opis
There are three types of functions implemented in SymPy:

    1) defined functions (in the sense that they can be evaluated) like
       exp or sin; they have a name and a body:
           f = exp
    2) undefined function which have a name but no body. Undefined
       functions can be defined using a Function class as follows:
           f = Function('f')
       (the result will be a Function in
