# checkstrformat.py — .python_packages/mypy/checkstrformat.py

## Tożsamość
- **id_karty:** `REPO-CHECKSTRFORMAT-B34C`
- **ścieżka:** `.python_packages/mypy/checkstrformat.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.171`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/checkstrformat.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.171 |
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
Format expression type checker.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ConversionSpecifier, StringFormatterChecker
- **funkcje:** `compile_format_re`, `compile_new_format_re`, `parse_conversion_specifiers`, `parse_format_value`, `find_non_escaped_targets`, `has_type_component`, `has_key`, `has_star`, `check_str_format_call`, `check_specs_in_format_call`, `perform_special_format_checks`, `find_replacements_in_call`, `get_expr_by_position`, `get_expr_by_name`, `auto_generate_keys`, `apply_field_accessors`, `validate_and_transform_accessors`, `check_str_interpolation`, `analyze_conversion_specifiers`, `check_simple_str_interpolation`, `check_mapping_str_interpolation`, `build_dict_type`, `build_replacement_checkers`, `replacement_checkers`, `checkers_for_star`, `check_placeholder_type`, `checkers_for_regular_type`, `check_s_special_cases`, `checkers_for_c_type`, `conversion_type`

## Opis
Format expression type checker.

This file is conceptually part of ExpressionChecker and TypeChecker. Main functionality
is located in StringFormatterChecker.check_str_format_call() for '{}'.format(), and in
StringFormatterChecker.check_str_interpolation() for printf-style % interpolation.

Note that although at runtime format strings are parsed using custom parsers,
here we use a regexp-based app
