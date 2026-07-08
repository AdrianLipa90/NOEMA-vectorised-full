# phase_toy.py — build/lib/integration/Orbital/main/src/ciel_relational_mechanism/sim/phase_toy.py

## Tożsamość
- **id_karty:** `REPO-PHASE_TOY-FD88`
- **ścieżka:** `build/lib/integration/Orbital/main/src/ciel_relational_mechanism/sim/phase_toy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.279`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/integration/Orbital/main/src/ciel_relational_mechanism/sim/phase_toy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.279 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


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
