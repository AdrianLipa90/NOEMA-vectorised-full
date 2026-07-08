# exportjson.py — .python_packages/mypy/exportjson.py

## Tożsamość
- **id_karty:** `REPO-EXPORTJSON-1F1C`
- **ścieżka:** `.python_packages/mypy/exportjson.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.981`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/exportjson.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.981 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Tool to convert binary mypy cache files (.ff) to JSON (.ff.json).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Config
- **funkcje:** `convert_binary_cache_to_json`, `convert_mypy_file_to_json`, `convert_symbol_table`, `convert_symbol_table_node`, `convert_symbol_node`, `convert_func_def`, `convert_dataclass_transform_spec`, `convert_overloaded_func_def`, `convert_overload_part`, `convert_decorator`, `convert_var`, `convert_type_info`, `convert_class_def`, `convert_type_alias`, `convert_type_var_expr`, `convert_param_spec_expr`, `convert_type_var_tuple_expr`, `convert_type`, `convert_instance`, `convert_extra_attrs`, `convert_type_alias_type`, `convert_any_type`, `convert_none_type`, `convert_union_type`, `convert_tuple_type`, `convert_literal_type`, `convert_type_var_type`, `convert_callable_type`, `convert_overloaded`, `convert_type_type`

## Opis
Tool to convert binary mypy cache files (.ff) to JSON (.ff.json).

Usage:
   python -m mypy.exportjson .mypy_cache/.../my_module.data.ff

The idea is to make caches introspectable once we've switched to a binary
cache format and removed support for the older JSON cache format.

This is primarily to support existing use cases that need to inspect
cache files, and to support debugging mypy caching i
