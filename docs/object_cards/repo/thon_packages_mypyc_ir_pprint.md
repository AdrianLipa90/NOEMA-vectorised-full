# pprint.py — .python_packages/mypyc/ir/pprint.py

## Tożsamość
- **id_karty:** `REPO-PPRINT-B593`
- **ścieżka:** `.python_packages/mypyc/ir/pprint.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.827`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/ir/pprint.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.827 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
Utilities for pretty-printing IR in a human-readable form.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** IRPrettyPrintVisitor
- **funkcje:** `format_registers`, `format_blocks`, `format_func`, `format_modules`, `generate_names_for_ir`, `visit_goto`, `visit_branch`, `visit_return`, `visit_unreachable`, `visit_assign`, `visit_assign_multi`, `visit_load_error_value`, `visit_load_literal`, `visit_get_attr`, `borrow_prefix`, `visit_set_attr`, `visit_load_static`, `visit_init_static`, `visit_tuple_get`, `visit_tuple_set`, `visit_inc_ref`, `visit_dec_ref`, `visit_call`, `visit_method_call`, `visit_cast`, `visit_box`, `visit_unbox`, `visit_raise_standard_error`, `visit_call_c`, `visit_primitive_op`

## Opis
Utilities for pretty-printing IR in a human-readable form.
