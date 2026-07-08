# global_algorithm_v02.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/global_algorithm_v02.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_ALGORITHM_V02-795D`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/global_algorithm_v02.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.172`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/global_algorithm_v02.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.172 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


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
