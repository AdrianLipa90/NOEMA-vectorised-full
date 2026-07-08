# solver.py — src/ciel_geometry/phasenav/solver.py

## Tożsamość
- **id_karty:** `REPO-SOLVER-2AFD`
- **ścieżka:** `src/ciel_geometry/phasenav/solver.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `3.836`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/phasenav/solver.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 3.836 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

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
PhaseNav solver — find operator paths between concepts through phase space.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** PhaseNavStep, PhaseNavTrace, PhaseNavSolver
- **funkcje:** `load`, `get_phase`, `get_orbit`, `get_operator_vector`, `best_edge_from`, `trace`, `_step_between`

## Opis
PhaseNav solver — find operator paths between concepts through phase space.

Maps concept → phase → operator edge → next concept via 33×24D algebra.
