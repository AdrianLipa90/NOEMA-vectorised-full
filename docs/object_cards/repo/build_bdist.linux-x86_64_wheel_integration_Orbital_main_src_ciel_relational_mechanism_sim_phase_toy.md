# phase_toy.py — build/bdist.linux-x86_64/wheel/integration/Orbital/main/src/ciel_relational_mechanism/sim/phase_toy.py

## Tożsamość
- **id_karty:** `REPO-PHASE_TOY-636D`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/integration/Orbital/main/src/ciel_relational_mechanism/sim/phase_toy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.476`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/integration/Orbital/main/src/ciel_relational_mechanism/sim/phase_toy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.476 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Minimal dimensionless relational phase toy simulator.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
