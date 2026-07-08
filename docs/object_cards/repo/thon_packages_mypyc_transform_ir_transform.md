# ir_transform.py — .python_packages/mypyc/transform/ir_transform.py

## Tożsamość
- **id_karty:** `REPO-IR_TRANSFORM-1A45`
- **ścieżka:** `.python_packages/mypyc/transform/ir_transform.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.742`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/transform/ir_transform.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.742 |
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
Helpers for implementing generic IR to IR transforms.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** IRTransform, PatchVisitor
- **funkcje:** `is_empty_block`, `transform_blocks`, `add`, `visit_goto`, `visit_branch`, `visit_return`, `visit_unreachable`, `visit_assign`, `visit_assign_multi`, `visit_load_error_value`, `visit_load_literal`, `visit_get_attr`, `visit_set_attr`, `visit_load_static`, `visit_init_static`, `visit_tuple_get`, `visit_tuple_set`, `visit_inc_ref`, `visit_dec_ref`, `visit_call`, `visit_method_call`, `visit_cast`, `visit_box`, `visit_unbox`, `visit_raise_standard_error`, `visit_call_c`, `visit_primitive_op`, `visit_truncate`, `visit_extend`, `visit_load_global`

## Opis
Helpers for implementing generic IR to IR transforms.
