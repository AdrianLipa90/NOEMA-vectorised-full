# emitmodule.py — .python_packages/mypyc/codegen/emitmodule.py

## Tożsamość
- **id_karty:** `REPO-EMITMODULE-CCD1`
- **ścieżka:** `.python_packages/mypyc/codegen/emitmodule.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.701`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/codegen/emitmodule.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.701 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Generate C code for a Python C extension module from Python source code.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MarkedDeclaration, MypycPlugin, GroupGenerator
- **funkcje:** `parse_and_typecheck`, `compile_scc_to_ir`, `compile_modules_to_ir`, `compile_ir_to_c`, `_load_cached_group_files`, `get_ir_cache_name`, `get_state_ir_cache_name`, `write_cache`, `load_scc_from_cache`, `collect_source_dependencies`, `collect_header_dependencies`, `compile_modules_to_c`, `generate_function_declaration`, `pointerize`, `group_dir`, `toposort`, `is_fastcall_supported`, `collect_literals`, `c_string_array_initializer`, `report_config_data`, `get_additional_deps`, `group_suffix`, `short_group_suffix`, `generate_c_for_modules`, `generate_literal_tables`, `generate_export_table`, `generate_shared_lib_init`, `generate_globals_init`, `generate_module_def`, `emit_module_def_slots`

## Opis
Generate C code for a Python C extension module from Python source code.
