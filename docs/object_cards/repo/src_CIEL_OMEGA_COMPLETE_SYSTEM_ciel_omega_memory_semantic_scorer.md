# semantic_scorer.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/semantic_scorer.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_SCORER-8C5E`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/semantic_scorer.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `5.346`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/semantic_scorer.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 5.346 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
CIEL Semantic Scorer — MemoryScorer + NOEMAObserver + SemanticExtractor + NonlocalGraphBuilder.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** _Card, _NonlocalLink, _NOEMAObs
- **funkcje:** `_extract`, `_score_card`, `_observe`, `_build_links`, `score_with_noema`, `build_nonlocal_index`

## Opis
CIEL Semantic Scorer — MemoryScorer + NOEMAObserver + SemanticExtractor + NonlocalGraphBuilder.

Inline port from ciel_algo_repo (no hard dependency on external path).
Provides semantic scoring, NOEMA observation metrics, and nonlocal graph construction
for CIEL holonomic memory entries.

Public API:
    score_with_noema(text, phase_metadata) → dict
    build_nonlocal_index(cards)            → dic
