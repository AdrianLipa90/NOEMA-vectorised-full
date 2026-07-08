# nodes.py — .python_packages/mypy/nodes.py

## Tożsamość
- **id_karty:** `REPO-NODES-4CA2`
- **ścieżka:** `.python_packages/mypy/nodes.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.609`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/nodes.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.609 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Abstract syntax tree node classes (i.e. parse tree).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NotParsed, Context, Node, Statement, Expression, FakeExpression, SymbolNode, ParseError, FileRawData, MypyFile, ImportBase, Import, ImportFrom, ImportAll, FuncBase, OverloadedFuncDef, Argument, TypeParam, FuncItem, FuncDef
- **funkcje:** `write_parse_error`, `read_parse_error`, `is_StrExpr_list`, `get_flags`, `set_flags`, `write_flags`, `read_flags`, `get_member_expr_fullname`, `check_arg_kinds`, `check_param_names`, `is_class_var`, `is_final_node`, `get_func_def`, `local_definitions`, `set_info`, `read_symbol`, `read_overload_part`, `set_line`, `str_with_options`, `accept`, `accept`, `accept`, `name`, `fullname`, `serialize`, `deserialize`, `write`, `read`, `write`, `read`

## Opis
Abstract syntax tree node classes (i.e. parse tree).
