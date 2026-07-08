# expression.py — .python_packages/mypyc/irbuild/expression.py

## Tożsamość
- **id_karty:** `REPO-EXPRESSION-5C09`
- **ścieżka:** `.python_packages/mypyc/irbuild/expression.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.040`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/expression.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.040 |
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
Transform mypy expression ASTs to mypyc IR (Intermediate Representation).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `transform_name_expr`, `transform_member_expr`, `check_instance_attribute_access_through_class`, `transform_super_expr`, `transform_call_expr`, `translate_call`, `translate_refexpr_call`, `translate_method_call`, `call_classmethod`, `translate_super_method_call`, `_get_vec_capacity`, `translate_vec_create_from_iterable`, `vec_from_iterable`, `translate_cast_expr`, `transform_unary_expr`, `transform_op_expr`, `try_optimize_int_floor_divide`, `transform_index_expr`, `try_constant_fold`, `try_gen_slice_op`, `transform_conditional_expr`, `set_literal_values`, `precompute_set_literal`, `transform_comparison_expr`, `try_specialize_in_expr`, `translate_is_none`, `transform_basic_comparison`, `translate_printf_style_formatting`, `transform_int_expr`, `transform_float_expr`

## Opis
Transform mypy expression ASTs to mypyc IR (Intermediate Representation).

The top-level AST transformation logic is implemented in mypyc.irbuild.visitor
and mypyc.irbuild.builder.
