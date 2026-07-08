# checkmember.py — .python_packages/mypy/checkmember.py

## Tożsamość
- **id_karty:** `REPO-CHECKMEMBER-3814`
- **ścieżka:** `.python_packages/mypy/checkmember.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.484`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/checkmember.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.484 |
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
Type checking of attribute access

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MemberContext
- **funkcje:** `analyze_member_access`, `_analyze_member_access`, `may_be_awaitable_attribute`, `report_missing_attribute`, `analyze_instance_member_access`, `validate_super_call`, `analyze_type_callable_member_access`, `analyze_type_type_member_access`, `analyze_union_member_access`, `analyze_none_member_access`, `analyze_member_var_access`, `check_final_member`, `analyze_descriptor_access`, `analyze_descriptor_assign`, `is_instance_var`, `analyze_var`, `expand_without_binding`, `expand_and_bind_callable`, `expand_self_type_if_needed`, `check_self_arg`, `analyze_class_attribute_access`, `apply_class_attr_hook`, `analyze_enum_class_attribute_access`, `analyze_typeddict_access`, `add_class_tvars`, `analyze_decorator_or_funcbase_access`, `bind_self_fast`, `has_operator`, `instance_fallback`, `meta_has_operator`

## Opis
Type checking of attribute access
