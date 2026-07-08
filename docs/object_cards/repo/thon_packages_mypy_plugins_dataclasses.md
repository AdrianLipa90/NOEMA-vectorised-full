# dataclasses.py — .python_packages/mypy/plugins/dataclasses.py

## Tożsamość
- **id_karty:** `REPO-DATACLASSES-72D4`
- **ścieżka:** `.python_packages/mypy/plugins/dataclasses.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.785`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/plugins/dataclasses.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.785 |
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
Plugin that provides support for dataclasses.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DataclassAttribute, DataclassTransformer
- **funkcje:** `add_dataclass_tag`, `dataclass_tag_callback`, `dataclass_class_maker_callback`, `_get_transform_spec`, `_is_dataclasses_decorator`, `_has_direct_dataclass_transform_metaclass`, `_get_expanded_dataclasses_fields`, `_meet_replace_sigs`, `replace_function_sig_callback`, `is_processed_dataclass`, `check_post_init`, `to_argument`, `expand_type`, `to_var`, `serialize`, `deserialize`, `expand_typevar_from_subtype`, `transform`, `_add_dunder_replace`, `_add_internal_replace_method`, `_add_internal_post_init_method`, `add_slots`, `reset_init_only_vars`, `_get_assignment_statements_from_if_statement`, `_get_assignment_statements_from_block`, `collect_attributes`, `_freeze`, `_propertize_callables`, `_is_kw_only_type`, `_add_dataclass_fields_magic_attribute`

## Opis
Plugin that provides support for dataclasses.
