# stubgen.py — .python_packages/mypy/stubgen.py

## Tożsamość
- **id_karty:** `REPO-STUBGEN-15A8`
- **ścieżka:** `.python_packages/mypy/stubgen.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.257`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/stubgen.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.257 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
Generator of dynamically typed draft stubs for arbitrary modules.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Options, StubSource, AliasPrinter, DefinitionFinder, ReferenceFinder, ASTStubGenerator, SelfTraverser
- **funkcje:** `find_defined_names`, `get_assigned_names`, `find_referenced_names`, `is_none_expr`, `find_method_names`, `find_self_initializers`, `get_qualified_name`, `remove_blacklisted_modules`, `split_pyc_from_py`, `is_blacklisted_path`, `normalize_path_separators`, `collect_build_targets`, `find_module_paths_using_imports`, `is_non_library_module`, `translate_module_name`, `find_module_paths_using_search`, `mypy_options`, `parse_source_file`, `generate_asts_for_modules`, `generate_stub_for_py_module`, `generate_stubs`, `parse_options`, `main`, `module`, `path`, `visit_call_expr`, `_visit_ref_expr`, `visit_name_expr`, `visit_member_expr`, `_visit_literal_node`

## Opis
Generator of dynamically typed draft stubs for arbitrary modules.

The logic of this script can be split in three steps:
* parsing options and finding sources:
  - use runtime imports be default (to find also C modules)
  - or use mypy's mechanisms, if importing is prohibited
* (optionally) semantically analysing the sources using mypy (as a single set)
* emitting the stubs text:
  - for Python mo
