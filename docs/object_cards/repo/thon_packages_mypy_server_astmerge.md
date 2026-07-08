# astmerge.py — .python_packages/mypy/server/astmerge.py

## Tożsamość
- **id_karty:** `REPO-ASTMERGE-C4A9`
- **ścieżka:** `.python_packages/mypy/server/astmerge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.788`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/server/astmerge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.788 |
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
Merge a new version of a module AST and symbol table to older versions of those.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NodeReplaceVisitor, TypeReplaceVisitor
- **funkcje:** `merge_asts`, `replacement_map_from_symbol_table`, `replace_nodes_in_ast`, `replace_nodes_in_symbol_table`, `_get_ignored_slots`, `visit_mypy_file`, `visit_block`, `visit_func_def`, `visit_overloaded_func_def`, `visit_class_def`, `process_base_func`, `process_type_var_def`, `process_param_spec_def`, `process_type_var_tuple_def`, `visit_assignment_stmt`, `visit_name_expr`, `visit_member_expr`, `visit_ref_expr`, `visit_namedtuple_expr`, `visit_cast_expr`, `visit_type_form_expr`, `visit_assert_type_expr`, `visit_super_expr`, `visit_call_expr`, `visit_newtype_expr`, `visit_lambda_expr`, `visit_typeddict_expr`, `visit_enum_call_expr`, `visit_var`, `visit_type_alias`

## Opis
Merge a new version of a module AST and symbol table to older versions of those.

When the source code of a module has a change in fine-grained incremental mode,
we build a new AST from the updated source. However, other parts of the program
may have direct references to parts of the old AST (namely, those nodes exposed
in the module symbol table). The merge operation changes the identities of new
