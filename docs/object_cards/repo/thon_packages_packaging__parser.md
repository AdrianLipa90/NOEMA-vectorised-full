# _parser.py — .python_packages/packaging/_parser.py

## Tożsamość
- **id_karty:** `REPO-_PARSER-51F2`
- **ścieżka:** `.python_packages/packaging/_parser.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.240`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/packaging/_parser.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.240 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Handwritten parser of dependency specifiers.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Node, Variable, Value, Op, ParsedRequirement
- **funkcje:** `parse_requirement`, `_parse_requirement`, `_parse_requirement_details`, `_parse_requirement_marker`, `_parse_extras`, `_parse_extras_list`, `_parse_specifier`, `_parse_version_many`, `parse_marker`, `_parse_full_marker`, `_parse_marker`, `_parse_marker_atom`, `_parse_marker_item`, `_parse_marker_var`, `process_env_var`, `process_python_str`, `_parse_marker_op`, `serialize`, `_restore_value`, `serialize`, `serialize`, `serialize`

## Opis
Handwritten parser of dependency specifiers.

The docstring for each __parse_* function contains EBNF-inspired grammar representing
the implementation.
