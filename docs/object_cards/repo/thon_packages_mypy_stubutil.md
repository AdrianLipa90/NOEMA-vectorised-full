# stubutil.py — .python_packages/mypy/stubutil.py

## Tożsamość
- **id_karty:** `REPO-STUBUTIL-1196`
- **ścieżka:** `.python_packages/mypy/stubutil.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.807`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/stubutil.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.807 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Utilities for mypy.stubgen, mypy.stubgenc, and mypy.stubdoc modules.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CantImport, AnnotationPrinter, ClassInfo, FunctionContext, SignatureGenerator, ImportTracker, BaseStubGenerator
- **funkcje:** `walk_packages`, `find_module_path_using_sys_path`, `find_module_path_and_all_py3`, `generate_guarded`, `report_missing`, `fail_missing`, `remove_misplaced_type_comments`, `remove_misplaced_type_comments`, `remove_misplaced_type_comments`, `common_dir_prefix`, `infer_method_ret_type`, `infer_method_arg_types`, `visit_any`, `visit_unbound_type`, `visit_none_type`, `visit_type_list`, `visit_union_type`, `visit_unpack_type`, `args_str`, `fullname`, `remove_self_type`, `get_function_sig`, `get_property_type`, `add_import_from`, `add_import`, `require_name`, `reexport`, `import_lines`, `get_sig_generators`, `resolve_name`

## Opis
Utilities for mypy.stubgen, mypy.stubgenc, and mypy.stubdoc modules.
