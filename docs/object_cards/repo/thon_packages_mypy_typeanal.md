# typeanal.py — .python_packages/mypy/typeanal.py

## Tożsamość
- **id_karty:** `REPO-TYPEANAL-E405`
- **ścieżka:** `.python_packages/mypy/typeanal.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.192`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/typeanal.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.192 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
Semantic analysis of types

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypeAnalyser, MsgCallback, DivergingAliasDetector, HasExplicitAny, HasAnyFromUnimportedType, CollectAllInnerTypesQuery, HasSelfType, FindTypeVarVisitor, TypeVarDefaultTranslator
- **funkcje:** `analyze_type_alias`, `get_omitted_any`, `fix_type_var_tuple_argument`, `fix_instance`, `instantiate_type_alias`, `set_any_tvars`, `detect_diverging_alias`, `check_for_explicit_any`, `has_explicit_any`, `has_any_from_unimported_type`, `collect_all_inner_types`, `make_optional_type`, `validate_instance`, `find_self_type`, `unknown_unpack`, `check_vec_type_args`, `lookup_qualified`, `lookup_fully_qualified`, `visit_unbound_type`, `not_declared_in_type_params`, `visit_unbound_type_nonoptional`, `pack_paramspec_args`, `cannot_resolve_type`, `apply_concatenate_operator`, `try_analyze_special_unbound_type`, `get_omitted_any`, `check_and_warn_deprecated`, `analyze_type_with_type_info`, `analyze_unbound_type_without_type_info`, `visit_any`

## Opis
Semantic analysis of types
