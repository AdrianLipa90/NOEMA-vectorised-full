# messages.py — .python_packages/mypy/messages.py

## Tożsamość
- **id_karty:** `REPO-MESSAGES-7C57`
- **ścieżka:** `.python_packages/mypy/messages.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.848`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/messages.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.848 |
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
Facilities for generating error messages during type checking.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MessageBuilder, CollectAllNamedTypesQuery
- **funkcje:** `quote_type_string`, `should_format_arg_as_type`, `format_callable_args`, `format_type_inner`, `collect_all_named_types`, `scoped_type_var_name`, `find_type_overlaps`, `format_type`, `format_type_bare`, `format_type_distinctly`, `pretty_class_or_static_decorator`, `pretty_callable`, `get_first_arg`, `variance_string`, `get_missing_protocol_members`, `get_conflict_protocol_types`, `get_bad_protocol_flags`, `capitalize`, `extract_type`, `strip_quotes`, `format_string_list`, `format_item_name_list`, `callable_name`, `for_function`, `wrong_type_arg_count`, `find_defining_module`, `_real_quick_ratio`, `best_matches`, `pretty_seq`, `append_invariance_notes`

## Opis
Facilities for generating error messages during type checking.

Don't add any non-trivial message construction logic to the type
checker, as it can compromise clarity and make messages less
consistent. Add such logic to this module instead. Literal messages, including those
with format args, should be defined as constants in mypy.message_registry.

Historically we tried to avoid all message string
