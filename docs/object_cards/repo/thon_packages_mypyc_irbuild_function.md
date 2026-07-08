# function.py — .python_packages/mypyc/irbuild/function.py

## Tożsamość
- **id_karty:** `REPO-FUNCTION-77DD`
- **ścieżka:** `.python_packages/mypyc/irbuild/function.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.834`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/function.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.834 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Transform mypy AST functions to IR (and related things).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ArgInfo
- **funkcje:** `transform_func_def`, `transform_overloaded_func_def`, `transform_decorator`, `transform_lambda_expr`, `gen_func_item`, `gen_func_body`, `has_nested_func_self_reference`, `gen_func_ir`, `generate_getattr_wrapper`, `generate_setattr_wrapper`, `handle_ext_method`, `handle_non_ext_method`, `gen_func_ns`, `load_decorated_func`, `is_decorated`, `gen_glue`, `get_args`, `gen_glue_method`, `check_native_override`, `gen_glue_property`, `gen_glue_property_setter`, `get_func_target`, `load_type`, `load_func`, `generate_singledispatch_dispatch_function`, `gen_calls_to_correct_impl`, `gen_dispatch_func_ir`, `generate_dispatch_glue_native_function`, `generate_singledispatch_callable_class_ctor`, `add_register_method_to_callable_class`

## Opis
Transform mypy AST functions to IR (and related things).

Normal functions are translated into a list of basic blocks
containing various IR ops (defined in mypyc.ir.ops).

This also deals with generators, async functions and nested
functions. All of these are transformed into callable classes. These
have a custom __call__ method that implements the call, and state, such
as an environment containin
