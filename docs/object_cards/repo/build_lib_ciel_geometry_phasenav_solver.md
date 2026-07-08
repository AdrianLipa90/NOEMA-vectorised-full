# solver.py — build/lib/ciel_geometry/phasenav/solver.py

## Tożsamość
- **id_karty:** `REPO-SOLVER-706B`
- **ścieżka:** `build/lib/ciel_geometry/phasenav/solver.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.311`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/phasenav/solver.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.311 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
PhaseNav solver — find operator paths between concepts through phase space.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TeleusingStep, TeleusingTrace, TeleusingSolver
- **funkcje:** `load`, `get_phase`, `get_orbit`, `get_operator_vector`, `best_edge_from`, `trace`, `_step_between`

## Opis
PhaseNav solver — find operator paths between concepts through phase space.

Maps concept → phase → operator edge → next concept via 33×24D algebra.
