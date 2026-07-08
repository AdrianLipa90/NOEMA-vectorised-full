# semantic_memory.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/semantic_memory.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_MEMORY-FB31`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/semantic_memory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `5.891`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/semantic_memory.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 5.891 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
CIEL/Ω Memory Architecture - M3 Semantic Memory

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** SemanticMemory
- **funkcje:** `_normalize_text`, `_stem`, `_extract_concept_key`, `_parse_semantics`, `_wrap`, `_episode_id`, `_compute_identity_alignment`, `_similarity`, `_existing_contradiction_penalty`, `_compute_novelty`, `_semantic_signature`, `_semantic_contradiction_pressure`, `semantic_distance`, `observe_episode`, `_traces_for_key`, `compute_consolidation_score`, `check_semantic_candidate_creation`, `consolidate_candidate`, `retrieve`, `get_statistics`, `snapshot`, `compute_input_force`, `store`, `retrieve_raw`

## Opis
CIEL/Ω Memory Architecture - M3 Semantic Memory

Conservative semantic memory channel. Consolidates repeated meaning from M2,
blocks contradictions, and provides simple retrieval.
