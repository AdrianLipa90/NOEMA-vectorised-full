# ircheck.py — .python_packages/mypyc/analysis/ircheck.py

## Tożsamość
- **id_karty:** `REPO-IRCHECK-A7EF`
- **ścieżka:** `.python_packages/mypyc/analysis/ircheck.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.877`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/analysis/ircheck.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.877 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Utilities for checking that internal ir is valid and consistent.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FnError, IrCheckException, OpChecker
- **funkcje:** `check_func_ir`, `assert_func_ir_valid`, `check_op_sources_valid`, `can_coerce_to`, `is_valid_ptr_displacement_type`, `is_pointer_arithmetic`, `fail`, `check_control_op_targets`, `check_type_coercion`, `check_compatibility`, `expect_float`, `expect_non_float`, `expect_primitive_type`, `visit_goto`, `visit_branch`, `visit_return`, `visit_unreachable`, `visit_assign`, `visit_assign_multi`, `visit_load_error_value`, `check_tuple_items_valid_literals`, `check_frozenset_items_valid_literals`, `visit_load_literal`, `visit_get_attr`, `visit_set_attr`, `visit_load_static`, `visit_init_static`, `visit_tuple_get`, `visit_tuple_set`, `visit_inc_ref`

## Opis
Utilities for checking that internal ir is valid and consistent.
