# negation_scope.py — src/cielingo_core/language_spaces/pl/negation_scope.py

## Tożsamość
- **id_karty:** `REPO-NEGATION_SCOPE-B480`
- **ścieżka:** `src/cielingo_core/language_spaces/pl/negation_scope.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.946`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/language_spaces/pl/negation_scope.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.946 |
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
Polish negation scope candidates v0.2.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NegationScopeCandidate
- **funkcje:** `detect_negation_scope`, `negation_scope_to_notes`, `to_dict`

## Opis
Polish negation scope candidates v0.2.

Detects surface negation candidates only; it is not a complete logical scope parser.
