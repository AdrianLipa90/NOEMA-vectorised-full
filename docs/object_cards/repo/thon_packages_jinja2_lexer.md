# lexer.py — .python_packages/jinja2/lexer.py

## Tożsamość
- **id_karty:** `REPO-LEXER-C7A4`
- **ścieżka:** `.python_packages/jinja2/lexer.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.072`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/jinja2/lexer.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.072 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
Implements a Jinja / Python combination lexer. The ``Lexer`` class

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Failure, Token, TokenStreamIterator, TokenStream, OptionalLStrip, _Rule, Lexer
- **funkcje:** `_describe_token_type`, `describe_token`, `describe_token_expr`, `count_newlines`, `compile_rules`, `get_lexer`, `test`, `test_any`, `eos`, `push`, `look`, `skip`, `next_if`, `skip_if`, `close`, `expect`, `_normalize_newlines`, `tokenize`, `wrap`, `tokeniter`, `c`

## Opis
Implements a Jinja / Python combination lexer. The ``Lexer`` class
is used to do some preprocessing. It filters out invalid operators like
the bitshift operators we don't allow in templates. It separates
template code and python code in expressions.
