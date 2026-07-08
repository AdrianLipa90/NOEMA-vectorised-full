# affective_memory.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/affective_memory.py

## Tożsamość
- **id_karty:** `REPO-AFFECTIVE_MEMORY-6813`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/affective_memory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `0.345`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/affective_memory.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 0.345 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
CIEL/Ω Memory Architecture - M5 Affective/Ethical Memory

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** AffectiveEthicalMemory
- **funkcje:** `_wrap`, `_normalize_text`, `_parse_affect`, `_episode_id`, `_compute_identity_alignment`, `_similarity`, `_infer_from_episode`, `_existing_contradiction_penalty`, `compute_input_force`, `observe_episode`, `_traces_for_key`, `compute_consolidation_score`, `check_candidate_creation`, `consolidate_candidate`, `retrieve`, `store`, `snapshot`

## Opis
CIEL/Ω Memory Architecture - M5 Affective/Ethical Memory

Conservative affective/ethical memory channel. Consolidates repeated salient
ethical signals from episodic traces and supports basic retrieval.
