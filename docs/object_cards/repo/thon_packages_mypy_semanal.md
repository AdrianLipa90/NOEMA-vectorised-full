# semanal.py — .python_packages/mypy/semanal.py

## Tożsamość
- **id_karty:** `REPO-SEMANAL-FECF`
- **ścieżka:** `.python_packages/mypy/semanal.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.279`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/semanal.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.279 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
The semantic analyzer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SemanticAnalyzer, MakeAnyNonExplicit, MakeAnyNonUnimported
- **funkcje:** `replace_implicit_first_type`, `refers_to_fullname`, `refers_to_class_or_function`, `find_duplicate`, `remove_imported_names_from_symtable`, `make_any_non_explicit`, `make_any_non_unimported`, `apply_semantic_analyzer_patches`, `names_modified_by_assignment`, `names_modified_in_lvalue`, `is_same_var_from_getattr`, `dummy_context`, `is_valid_replacement`, `is_same_symbol`, `is_trivial_body`, `is_init_only`, `erase_func_annotations`, `type`, `is_stub_file`, `is_typeshed_stub_file`, `final_iteration`, `allow_unbound_tvars_set`, `inside_except_star_block_set`, `prepare_file`, `prepare_typing_namespace`, `prepare_builtins_namespace`, `refresh_partial`, `refresh_top_level`, `add_implicit_module_attrs`, `add_builtin_aliases`

## Opis
The semantic analyzer.

Bind names to definitions and do various other simple consistency
checks.  Populate symbol tables.  The semantic analyzer also detects
special forms which reuse generic syntax such as NamedTuple and
cast().  Multiple analysis iterations may be needed to analyze forward
references and import cycles. Each iteration "fills in" additional
bindings and references until everythin
