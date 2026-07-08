# phase_toy.py — integration/Orbital/main/src/ciel_relational_mechanism/sim/phase_toy.py

## Tożsamość
- **id_karty:** `REPO-PHASE_TOY-DAE1`
- **ścieżka:** `integration/Orbital/main/src/ciel_relational_mechanism/sim/phase_toy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.200`
- **φ (phi):** `3.218`
- **masa_semantyczna:** `0.90`

## Kotwice
- `integration/Orbital/main/src/ciel_relational_mechanism/sim/phase_toy.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.200 |
| φ | 3.218 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
Minimal dimensionless relational phase toy simulator.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** PhaseState, PairKernel, StepRecord, RelationalPhaseToySim
- **funkcje:** `delta_H`, `R_H`, `zero`, `set_symmetric`, `neighbors`, `effective_Aij_drive`, `step`, `run`

## Opis
Minimal dimensionless relational phase toy simulator.

Mechanism only:
- phases on a cycle family
- Euler-Berry closure defect
- effective pair coupling kernel A_ij
- reduction readiness from defect threshold
No metric closure and no physical constants are assumed here.
