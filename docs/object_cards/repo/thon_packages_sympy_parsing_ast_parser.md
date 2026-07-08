# ast_parser.py — .python_packages/sympy/parsing/ast_parser.py

## Tożsamość
- **id_karty:** `REPO-AST_PARSER-F591`
- **ścieżka:** `.python_packages/sympy/parsing/ast_parser.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.866`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/parsing/ast_parser.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.866 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
This module implements the functionality to take any Python expression as a

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Transform
- **funkcje:** `parse_expr`, `visit_Constant`, `visit_Name`, `visit_Lambda`

## Opis
This module implements the functionality to take any Python expression as a
string and fix all numbers and other things before evaluating it,
thus

1/2

returns

Integer(1)/Integer(2)

We use the ast module for this. It is well documented at docs.python.org.

Some tips to understand how this works: use dump() to get a nice
representation of any node. Then write a string of what you want to get,
e.
