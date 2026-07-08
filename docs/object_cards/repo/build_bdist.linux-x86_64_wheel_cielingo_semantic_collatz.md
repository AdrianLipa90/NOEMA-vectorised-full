# semantic_collatz.py — build/bdist.linux-x86_64/wheel/cielingo/semantic_collatz.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_COLLATZ-2DC7`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo/semantic_collatz.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.155`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo/semantic_collatz.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.155 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


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
