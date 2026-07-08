# query_generation.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/query_generation.py

## Tożsamość
- **id_karty:** `REPO-QUERY_GENERATION-A376`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/query_generation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.930`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/query_generation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.930 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


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
