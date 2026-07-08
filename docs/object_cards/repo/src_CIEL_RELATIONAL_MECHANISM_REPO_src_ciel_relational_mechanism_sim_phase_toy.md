# phase_toy.py — src/CIEL_RELATIONAL_MECHANISM_REPO/src/ciel_relational_mechanism/sim/phase_toy.py

## Tożsamość
- **id_karty:** `REPO-PHASE_TOY-32D0`
- **ścieżka:** `src/CIEL_RELATIONAL_MECHANISM_REPO/src/ciel_relational_mechanism/sim/phase_toy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.942`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/CIEL_RELATIONAL_MECHANISM_REPO/src/ciel_relational_mechanism/sim/phase_toy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.942 |
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
