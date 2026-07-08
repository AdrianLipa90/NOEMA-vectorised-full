# _fortran_format_parser.py — .python_packages/scipy/io/_harwell_boeing/_fortran_format_parser.py

## Tożsamość
- **id_karty:** `REPO-_FORTRAN_FORMAT_PARS-05E2`
- **ścieżka:** `.python_packages/scipy/io/_harwell_boeing/_fortran_format_parser.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.823`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/_harwell_boeing/_fortran_format_parser.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.823 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Preliminary module to handle Fortran formats for IO. Does not use this outside

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** BadFortranFormat, IntFormat, ExpFormat, Token, Tokenizer, FortranFormatParser
- **funkcje:** `number_digits`, `from_number`, `fortran_format`, `python_format`, `from_number`, `fortran_format`, `python_format`, `input`, `next_token`, `parse`, `_get_min`, `_expect`, `_parse_format`, `_next`

## Opis
Preliminary module to handle Fortran formats for IO. Does not use this outside
scipy.sparse io for now, until the API is deemed reasonable.

The *Format classes handle conversion between Fortran and Python format, and
FortranFormatParser can create *Format instances from raw Fortran format
strings (e.g. '(3I4)', '(10I3)', etc...)
