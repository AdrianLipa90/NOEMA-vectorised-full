# solver.py — build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/solver.py

## Tożsamość
- **id_karty:** `REPO-SOLVER-28A0`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/solver.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.605`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/solver.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.605 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


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
