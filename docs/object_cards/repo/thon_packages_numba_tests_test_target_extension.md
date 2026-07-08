# test_target_extension.py — .python_packages/numba/tests/test_target_extension.py

## Tożsamość
- **id_karty:** `REPO-TEST_TARGET_EXTENSIO-EB5F`
- **ścieżka:** `.python_packages/numba/tests/test_target_extension.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.451`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_target_extension.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.451 |
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
This tests the target extension API to ensure that rudimentary expected

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DPU, JITDPUCodegen, DPUContext, DPUTarget, DPUDispatcher, djit, TestTargetHierarchySelection, TestTargetOffload, DispatcherSwitcher, DPUOffloadCompiler
- **funkcje:** `constant_dummy`, `literal_int_to_number`, `const_int`, `const_float`, `intrin_add`, `ol_add`, `_customize_tm_options`, `_customize_tm_features`, `_add_module`, `set_env`, `create_module`, `init`, `refresh`, `target_data`, `codegen`, `call_conv`, `get_env_body`, `get_env_manager`, `get_generator_state`, `post_lowering`, `create_cpython_wrapper`, `create_cfunc_wrapper`, `get_executable`, `_toplevel_target_context`, `_toplevel_typing_context`, `target_context`, `typing_context`, `compile`, `get_dispatcher`, `dispatcher_wrapper`

## Opis
This tests the target extension API to ensure that rudimentary expected
behaviours are present and correct. It uses a piece of fake hardware as a
target, the Dummy Processing Unit (DPU), to do this. The DPU borrows a lot from
the CPU but is part of the GPU class of target. The DPU target has deliberately
strange implementations of fundamental operations so as to make it identifiable
in testing.
