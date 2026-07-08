# solver.py — build/lib/cielingo_core/language_spaces/pl/solver.py

## Tożsamość
- **id_karty:** `REPO-SOLVER-D7CF`
- **ścieżka:** `build/lib/cielingo_core/language_spaces/pl/solver.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.058`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/language_spaces/pl/solver.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.058 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
Adapted Polish regional solver for CIELingo 0.5O.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PolishRegionalSolver
- **funkcje:** `_pl_v02_diagnostics`, `segment`, `solve`

## Opis
Adapted Polish regional solver for CIELingo 0.5O.

Adds Polish v0.2 regional diagnostics:
- case_hint candidates, not full cases;
- role_candidate objects, not final semantic roles;
- negation-scope candidates, not complete logical scope;
- imperative/action-force candidates, not runtime authorization;
- source_required candidates, not SOURCE;
- canon_attempt/canon_block candidates, not canon;
- b
