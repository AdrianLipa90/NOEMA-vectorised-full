# operator_algebra.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/operator_algebra.py

## Tożsamość
- **id_karty:** `REPO-OPERATOR_ALGEBRA-510E`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/operator_algebra.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.786`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/operator_algebra.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.786 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
CIELingo GLOBAL v0.2 operator algebra.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** OperatorKind, OperatorDomain, RelationalOperator
- **funkcje:** `_bounded01`, `get_default_operator`, `validate_operator_registry`, `validate`, `to_dict`

## Opis
CIELingo GLOBAL v0.2 operator algebra.

Scope:
- Defines language-independent semantic operators.
- Does not parse regional grammar.
- Does not grant SOURCE/canon by default.

Operator is not a word. A word/card may realize an operator in a language,
but GLOBAL only handles the operator contract.
