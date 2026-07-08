# query_generation.py — build/lib/cielingo_core/global_layer/query_generation.py

## Tożsamość
- **id_karty:** `REPO-QUERY_GENERATION-8FC9`
- **ścieżka:** `build/lib/cielingo_core/global_layer/query_generation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.331`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/query_generation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.331 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
Query understanding and text generation dry-run v1.1A.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** QueryIntention, QueryUnderstandingResult, DraftAnswerCandidate, QueryGenerationDryRunReport
- **funkcje:** `understand_query`, `_compose_draft`, `run_query_generation_dry_run`, `validate`, `to_dict`, `stable_hash`, `validate`, `to_dict`, `stable_hash`, `validate`, `to_dict`, `stable_hash`

## Opis
Query understanding and text generation dry-run v1.1A.

This layer creates draft answer candidates from query-understanding diagnostics.

Boundary:
- QueryUnderstandingResult is a heuristic classification, not full understanding.
- DraftAnswerCandidate is generated text, not SOURCE/canon/truth proof.
- No runtime execution, NOEMA writeback, or CURRENT update.
