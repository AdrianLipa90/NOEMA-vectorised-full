# global_algorithm_v02.py — build/lib/cielingo_core/global_layer/global_algorithm_v02.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_ALGORITHM_V02-E0FE`
- **ścieżka:** `build/lib/cielingo_core/global_layer/global_algorithm_v02.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.503`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/global_algorithm_v02.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.503 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
CIELingo GLOBAL v0.2 algorithm.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GlobalAlgorithmV02Result
- **funkcje:** `extract_operator_ids`, `build_actions_from_equation`, `detect_scars`, `build_immune_signal`, `run_global_algorithm_v02`, `validate`, `to_dict`

## Opis
CIELingo GLOBAL v0.2 algorithm.

Pipeline:
  MeaningEquation
  -> operator extraction
  -> MeaningAction[]
  -> MeaningBlockAction
  -> SemanticScar[]
  -> MeaningLoop
  -> SemanticImmuneSignal
  -> enriched algorithm result

This algorithm still does not parse regional grammar.
