# ast_helpers.py — .python_packages/mypyc/irbuild/ast_helpers.py

## Tożsamość
- **id_karty:** `REPO-AST_HELPERS-F0BE`
- **ścieżka:** `.python_packages/mypyc/irbuild/ast_helpers.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.308`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/ast_helpers.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.308 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
IRBuilder AST transform helpers shared between expressions and statements.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `process_conditional`, `maybe_process_conditional_comparison`, `is_borrow_friendly_expr`

## Opis
IRBuilder AST transform helpers shared between expressions and statements.

Shared code that is tightly coupled to mypy ASTs can be put here instead of
making mypyc.irbuild.builder larger.
