# contracts.py — build/bdist.linux-x86_64/wheel/cielingo_core/doctor/contracts.py

## Tożsamość
- **id_karty:** `REPO-CONTRACTS-FD62`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/doctor/contracts.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.092`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/doctor/contracts.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.092 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Doctor contracts for CIELingo.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ImplementationStatus, DoctorSeverity, DoctorLayer, RepairActionKind, RepairCandidate, QuarantineCandidate, DebtEntry, Limitation, RiskFlag, StubMarker, DoctorFinding, DoctorReport
- **funkcje:** `clamp01`, `empty_pass_report`, `validate`, `to_dict`, `validate`, `to_dict`, `validate`, `to_dict`, `validate`, `to_dict`, `validate`, `to_dict`, `validate`, `to_dict`, `validate`, `to_dict`, `validate`, `has_blockers`, `debts`, `stubs`, `limitations`, `risks`, `no_hidden_debt_check`, `to_dict`

## Opis
Doctor contracts for CIELingo.

This module is deliberately contract-only. It does not implement PL grammar,
runtime connectors, external NOEMA writeback, canon promotion, or SOURCE promotion.

Core rule:
    Doctor diagnoses and recommends.
    Doctor does not canonize.
    Doctor does not write external NOEMA SoT.
    Doctor does not become runtime authority.
