# orchestrator_types.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/orchestrator_types.py

## Tożsamość
- **id_karty:** `REPO-ORCHESTRATOR_TYPES-D61E`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/orchestrator_types.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `4.333`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/orchestrator_types.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 4.333 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Types for HolonomicMemoryOrchestrator.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** ConsolidationEvents, EBAEvaluation, OrchestratorCycleResult, OrchestratorSnapshot
- **funkcje:** —

## Opis
Types for HolonomicMemoryOrchestrator.

Conservative runtime glue for the implemented CIEL/Ω memory channels.
