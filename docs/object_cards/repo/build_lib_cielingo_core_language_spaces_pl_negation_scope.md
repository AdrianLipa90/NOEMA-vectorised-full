# negation_scope.py — build/lib/cielingo_core/language_spaces/pl/negation_scope.py

## Tożsamość
- **id_karty:** `REPO-NEGATION_SCOPE-E0C9`
- **ścieżka:** `build/lib/cielingo_core/language_spaces/pl/negation_scope.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.857`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/language_spaces/pl/negation_scope.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.857 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


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
