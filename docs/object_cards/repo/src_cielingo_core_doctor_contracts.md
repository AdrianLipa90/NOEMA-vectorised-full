# contracts.py — src/cielingo_core/doctor/contracts.py

## Tożsamość
- **id_karty:** `REPO-CONTRACTS-DB10`
- **ścieżka:** `src/cielingo_core/doctor/contracts.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.102`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/doctor/contracts.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.102 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


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
