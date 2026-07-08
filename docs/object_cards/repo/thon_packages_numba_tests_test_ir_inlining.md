# test_ir_inlining.py — .python_packages/numba/tests/test_ir_inlining.py

## Tożsamość
- **id_karty:** `REPO-TEST_IR_INLINING-D75F`
- **ścieżka:** `.python_packages/numba/tests/test_ir_inlining.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.009`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_ir_inlining.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.009 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
This tests the inline kwarg to @jit and @overload etc, it has nothing to do with

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** InliningBase, TestFunctionInlining, TestRegisterJitableInlining, TestOverloadInlining, TestOverloadMethsAttrsInlining, TestGeneralInlining, TestInlineOptions, TestInlineMiscIssues, Dummy, DummyType, DummyTypeModel, CustomCompiler
- **funkcje:** `_global_func`, `_global_defn`, `_global_overload`, `_gen_involved`, `sentinel_17_cost_model`, `check`, `foo`, `test_basic_inline_never`, `test_basic_inline_always`, `test_basic_inline_combos`, `test_recursive_inline`, `test_freevar_bindings`, `test_global_binding`, `test_inline_from_another_module`, `test_inline_from_another_module_w_getattr`, `test_inline_from_another_module_w_2_getattr`, `test_inline_from_another_module_as_freevar`, `test_inline_w_freevar_from_another_module`, `test_inlining_models`, `test_inline_inside_loop`, `test_inline_inside_closure_inside_loop`, `test_inline_closure_inside_inlinable_inside_closure`, `test_inline_involved`, `test_inline_renaming_scheme`, `test_register_jitable_inlines`, `test_basic_inline_never`, `test_basic_inline_always`, `test_inline_always_kw_no_default`, `test_inline_operators_unary`, `test_inline_operators_binop`

## Opis
This tests the inline kwarg to @jit and @overload etc, it has nothing to do with
LLVM or low level inlining.
