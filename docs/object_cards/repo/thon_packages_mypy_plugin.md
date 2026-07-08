# plugin.py — .python_packages/mypy/plugin.py

## Tożsamość
- **id_karty:** `REPO-PLUGIN-C06E`
- **ścieżka:** `.python_packages/mypy/plugin.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.812`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/plugin.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.812 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Plugin system for extending mypy.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypeAnalyzerPluginInterface, AnalyzeTypeContext, CommonPluginApi, CheckerPluginInterface, SemanticAnalyzerPluginInterface, ReportConfigContext, FunctionSigContext, FunctionContext, MethodSigContext, MethodContext, AttributeContext, ClassDefContext, DynamicClassDefContext, Plugin, ChainedPlugin
- **funkcje:** `fail`, `named_type`, `analyze_type`, `analyze_callable_args`, `lookup_fully_qualified`, `type_context`, `fail`, `named_generic_type`, `get_expression_type`, `named_type`, `builtin_type`, `named_type_or_none`, `basic_new_typeinfo`, `parse_bool`, `parse_str_literal`, `fail`, `anal_type`, `class_type`, `lookup_fully_qualified`, `lookup_fully_qualified_or_none`, `lookup_qualified`, `add_plugin_dependency`, `add_symbol_table_node`, `qualified_name`, `defer`, `final_iteration`, `is_stub_file`, `analyze_simple_literal_type`, `set_modules`, `lookup_fully_qualified`

## Opis
Plugin system for extending mypy.

At large scale the plugin system works as following:

* Plugins are collected from the corresponding mypy config file option
  (either via paths to Python files, or installed Python modules)
  and imported using importlib.

* Every module should get an entry point function (called 'plugin' by default,
  but may be overridden in the config file) that should accept
