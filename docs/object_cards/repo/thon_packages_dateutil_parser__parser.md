# _parser.py — .python_packages/dateutil/parser/_parser.py

## Tożsamość
- **id_karty:** `REPO-_PARSER-D7FC`
- **ścieżka:** `.python_packages/dateutil/parser/_parser.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.971`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/dateutil/parser/_parser.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.971 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
This module offers a generic date/time string parser which is able to parse

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _timelex, _resultbase, parserinfo, _ymd, parser, _tzparser, ParserError, UnknownTimezoneWarning, _result, _result, _attr
- **funkcje:** `parse`, `_parsetz`, `get_token`, `next`, `split`, `isword`, `isnum`, `isspace`, `_repr`, `_convert`, `jump`, `weekday`, `month`, `hms`, `ampm`, `pertain`, `utczone`, `tzoffset`, `convertyear`, `validate`, `has_year`, `has_month`, `has_day`, `could_be_day`, `append`, `_resolve_from_stridxs`, `resolve_ymd`, `parse`, `_parse`, `_parse_numeric_token`

## Opis
This module offers a generic date/time string parser which is able to parse
most known formats to represent a date and/or time.

This module attempts to be forgiving with regards to unlikely input formats,
returning a datetime object even for dates which are ambiguous. If an element
of a date/time stamp is omitted, the following rules are applied:

- If AM or PM is left unspecified, a 24-hour cloc
