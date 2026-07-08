# procedural_memory.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/procedural_memory.py

## Tożsamość
- **id_karty:** `REPO-PROCEDURAL_MEMORY-2E13`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/procedural_memory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `5.927`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/procedural_memory.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 5.927 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
CIEL/Ω Memory Architecture - M4 Procedural Memory

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** ProceduralMemory
- **funkcje:** `_wrap`, `normalize_text`, `_extract_goal_action`, `_procedure_key`, `_episode_id`, `_compute_identity_alignment`, `_extract_success`, `_similarity`, `compute_input_force`, `observe_episode`, `_existing_contradiction_penalty`, `_traces_for_key`, `_goal_level_contradiction`, `compute_consolidation_score`, `check_candidate_creation`, `consolidate_candidate`, `retrieve`, `snapshot`, `retrieve_raw`, `store`

## Opis
CIEL/Ω Memory Architecture - M4 Procedural Memory

Conservative procedural memory channel. Consolidates reusable procedures from
repeated successful episodes for the same goal while blocking contradictions.
