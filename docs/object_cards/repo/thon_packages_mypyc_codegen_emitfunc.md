# emitfunc.py — .python_packages/mypyc/codegen/emitfunc.py

## Tożsamość
- **id_karty:** `REPO-EMITFUNC-4713`
- **ścieżka:** `.python_packages/mypyc/codegen/emitfunc.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.391`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/codegen/emitfunc.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.391 |
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
Code generation for native function bodies.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FunctionEmitterVisitor
- **funkcje:** `native_function_type`, `native_function_type_from_decl`, `native_function_header`, `generate_native_function`, `encode_c_string_literal`, `temp_name`, `visit_goto`, `error_value_check`, `visit_branch`, `visit_return`, `visit_tuple_set`, `visit_assign`, `visit_assign_multi`, `visit_load_error_value`, `visit_load_literal`, `get_attr_expr`, `visit_get_attr`, `get_attr_with_allow_error_value`, `next_branch`, `visit_set_attr`, `visit_load_static`, `visit_init_static`, `visit_tuple_get`, `get_dest_assign`, `visit_call`, `visit_method_call`, `emit_method_call`, `visit_inc_ref`, `visit_dec_ref`, `visit_box`

## Opis
Code generation for native function bodies.
