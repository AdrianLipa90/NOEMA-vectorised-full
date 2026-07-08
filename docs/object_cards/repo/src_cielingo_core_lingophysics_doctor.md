# doctor.py — src/cielingo_core/lingophysics/doctor.py

## Tożsamość
- **id_karty:** `REPO-DOCTOR-3999`
- **ścieżka:** `src/cielingo_core/lingophysics/doctor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.044`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/lingophysics/doctor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.044 |
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
Lingophysics Doctor for CIELingo.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SurfaceSolutionDoctor, SentenceEquationDoctor, LocalJDoctor, RegionalSeparationDoctor, MeaningDebtDoctor, JCoherenceDoctor, SemanticNeuralStateDoctor, CrossLanguageAlignmentDoctor, ControlledAtlasDoctor, SentenceCardCouplingDoctor, CouplingAwareAlignmentDoctor, MeaningLoopDoctor, MeaningRepairRoutingDoctor, MeaningExportAndSignalDoctor, RuntimeBridgeDryRunDoctor, SelfFeedAuditDoctor, RuntimeAdapterReferenceDoctor, RuntimeAdapterExportDoctor, LingophysicsDoctor
- **funkcje:** `_is_number`, `_finding`, `diagnose`, `diagnose`, `diagnose`, `diagnose_repo`, `diagnose_text`, `diagnose`, `diagnose_snapshot`, `diagnose_candidate`, `diagnose_report`, `diagnose_validation_result`, `diagnose_card_rows`, `diagnose_alignment_rows`, `diagnose_report`, `diagnose_candidate`, `diagnose_report`, `diagnose_loop`, `diagnose_report`, `diagnose`, `diagnose`, `diagnose`, `diagnose`, `diagnose`, `diagnose_sentence_equation`, `diagnose_surface_solution`, `diagnose_local_j`, `diagnose_regional_separation`, `diagnose_meaning_debt_text`, `diagnose_j_coherence`

## Opis
Lingophysics Doctor for CIELingo.

This module diagnoses lingophysics objects. It does not parse Polish grammar,
does not promote SOURCE/canon, does not write NOEMA, and does not become runtime
authority.

Primary target:
    language / lingophysics / semantic-neural diagnostics.

No-hidden-debt rule:
    stubs, limitations, risks and debt must be explicit DoctorFinding objects.
