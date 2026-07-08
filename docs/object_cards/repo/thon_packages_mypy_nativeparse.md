# nativeparse.py — .python_packages/mypy/nativeparse.py

## Tożsamość
- **id_karty:** `REPO-NATIVEPARSE-DCD6`
- **ścieżka:** `.python_packages/mypy/nativeparse.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.816`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/nativeparse.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.816 |
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
Python parser that directly constructs a native AST (when compiled).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** State
- **funkcje:** `native_parse`, `expect_end_tag`, `expect_tag`, `read_statements`, `parse_to_binary_ast`, `read_statement`, `read_parameters`, `read_type_params`, `read_func_def`, `read_class_def`, `read_type_alias_stmt`, `read_try_stmt`, `read_type`, `stringify_type_name`, `extract_arg_name`, `read_call_type`, `read_pattern`, `read_block`, `read_optional_block`, `read_expression`, `read_fstring_items`, `build_fstring_join`, `collapse_consecutive_str_items`, `read_fstring_item`, `set_line_column`, `set_line_column_range`, `read_expression_list`, `read_generator_expr`, `read_loc`, `strip_contents_from_if_stmt`

## Opis
Python parser that directly constructs a native AST (when compiled).

Use a Rust extension to generate a serialized AST, and deserialize the AST directly
to a mypy AST.

NOTE: This is work in progress. To use this, you need to manually build the
      ast_serialize Rust extension. See the README at https://github.com/mypyc/ast_serialize.

Expected benefits over mypy.fastparse:
 * No intermediate n
