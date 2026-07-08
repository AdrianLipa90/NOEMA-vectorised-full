# global_algorithm_v02.py — src/cielingo_core/global_layer/global_algorithm_v02.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_ALGORITHM_V02-6461`
- **ścieżka:** `src/cielingo_core/global_layer/global_algorithm_v02.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.238`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/global_algorithm_v02.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.238 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


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
