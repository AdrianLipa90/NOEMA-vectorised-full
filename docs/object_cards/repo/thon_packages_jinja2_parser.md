# parser.py — .python_packages/jinja2/parser.py

## Tożsamość
- **id_karty:** `REPO-PARSER-20AD`
- **ścieżka:** `.python_packages/jinja2/parser.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.795`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/jinja2/parser.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.795 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Parse tokens from the lexer into nodes for the compiler.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Parser
- **funkcje:** `fail`, `_fail_ut_eof`, `fail_unknown_tag`, `fail_eof`, `is_tuple_end`, `free_identifier`, `parse_statement`, `parse_statements`, `parse_set`, `parse_for`, `parse_if`, `parse_with`, `parse_autoescape`, `parse_block`, `parse_extends`, `parse_import_context`, `parse_include`, `parse_import`, `parse_from`, `parse_signature`, `parse_call_block`, `parse_filter_block`, `parse_macro`, `parse_print`, `parse_assign_target`, `parse_assign_target`, `parse_assign_target`, `parse_expression`, `parse_condexpr`, `parse_or`

## Opis
Parse tokens from the lexer into nodes for the compiler.
