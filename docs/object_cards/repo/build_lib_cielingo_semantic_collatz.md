# semantic_collatz.py — build/lib/cielingo/semantic_collatz.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_COLLATZ-B045`
- **ścieżka:** `build/lib/cielingo/semantic_collatz.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.672`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/semantic_collatz.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.672 |
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
Semantic Collatz routing for CIELingo card-trace states.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CollatzSemanticStep
- **funkcje:** `semantic_seed`, `semantic_collatz_route`, `route_summary`

## Opis
Semantic Collatz routing for CIELingo card-trace states.

Even steps reduce toward a stable identity/cluster. Odd steps expand semantic
neighbours before the route folds back toward reduction.
