# prepare.py — .python_packages/mypyc/irbuild/prepare.py

## Tożsamość
- **id_karty:** `REPO-PREPARE-85C5`
- **ścieżka:** `.python_packages/mypyc/irbuild/prepare.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.303`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/prepare.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.303 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Prepare for IR transform.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SingledispatchInfo, SingledispatchVisitor, RegisteredImpl
- **funkcje:** `build_type_map`, `is_from_module`, `load_type_map`, `get_module_func_defs`, `prepare_func_def`, `create_generator_class_for_func`, `prepare_method_def`, `prepare_fast_path`, `is_valid_multipart_property_def`, `can_subclass_builtin`, `get_removed_base_fullname`, `find_non_acyclic_base`, `validate_acyclic_class_bases`, `prepare_class_def`, `prepare_methods_and_attributes`, `prepare_implicit_property_accessors`, `add_property_methods_for_attribute_if_needed`, `add_getter_declaration`, `add_setter_declaration`, `check_matching_args`, `prepare_init_method`, `prepare_non_ext_class_def`, `find_singledispatch_register_impls`, `get_singledispatch_register_call_info`, `registered_impl_from_possible_register_call`, `adjust_generator_classes_of_methods`, `visit_func_def`, `visit_decorator`

## Opis
Prepare for IR transform.

This needs to run after type checking and before generating IR.

For example, construct partially initialized FuncIR and ClassIR
objects for all functions and classes. This allows us to bind
references to functions and classes before we've generated full IR for
functions or classes.  The actual IR transform will then populate all
the missing bits, such as function bodies
