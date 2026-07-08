# types.py — .python_packages/mypy/types.py

## Tożsamość
- **id_karty:** `REPO-TYPES-5503`
- **ścieżka:** `.python_packages/mypy/types.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.317`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/types.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.317 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
Classes for representing mypy types.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypeOfAny, Type, TypeAliasType, TypeGuardedType, RequiredType, ReadOnlyType, ProperType, TypeVarId, TypeVarLikeType, TypeVarType, ParamSpecFlavor, ParamSpecType, TypeVarTupleType, UnboundType, CallableArgument, TypeList, UnpackType, AnyType, UninhabitedType, NoneType
- **funkcje:** `deserialize_type`, `get_proper_type`, `get_proper_type`, `get_proper_type`, `get_proper_types`, `get_proper_types`, `get_proper_types`, `is_named_instance`, `has_type_vars`, `has_recursive_types`, `split_with_prefix_and_suffix`, `extend_args_for_prefix_and_suffix`, `flatten_nested_unions`, `find_unpack_in_list`, `flatten_nested_tuples`, `is_literal_type`, `is_unannotated_any`, `callable_with_ellipsis`, `remove_dups`, `type_vars_as_args`, `read_type`, `read_function_like`, `read_type_var_likes`, `read_type_opt`, `write_type_opt`, `read_type_list`, `write_type_list`, `read_type_map`, `write_type_map`, `can_be_true`

## Opis
Classes for representing mypy types.
