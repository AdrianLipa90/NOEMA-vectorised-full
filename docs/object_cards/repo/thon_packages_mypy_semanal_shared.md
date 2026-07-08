# semanal_shared.py — .python_packages/mypy/semanal_shared.py

## Tożsamość
- **id_karty:** `REPO-SEMANAL_SHARED-4938`
- **ścieżka:** `.python_packages/mypy/semanal_shared.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.454`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/semanal_shared.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.454 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Shared definitions used by different parts of semantic analysis.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SemanticAnalyzerCoreInterface, SemanticAnalyzerInterface, _NamedTypeCallback, HasPlaceholders
- **funkcje:** `set_callable_name`, `calculate_tuple_fallback`, `paramspec_args`, `paramspec_kwargs`, `has_placeholder`, `find_dataclass_transform_spec`, `require_bool_literal_argument`, `require_bool_literal_argument`, `require_bool_literal_argument`, `parse_bool`, `lookup_qualified`, `lookup_fully_qualified`, `lookup_fully_qualified_or_none`, `fail`, `note`, `incomplete_feature_enabled`, `record_incomplete_ref`, `defer`, `is_incomplete_namespace`, `final_iteration`, `is_future_flag_set`, `is_stub_file`, `is_func_scope`, `type`, `lookup`, `named_type`, `named_type_or_none`, `accept`, `anal_type`, `get_and_bind_all_tvars`

## Opis
Shared definitions used by different parts of semantic analysis.
