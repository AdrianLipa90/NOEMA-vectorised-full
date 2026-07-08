# perceptual_memory.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/perceptual_memory.py

## Tożsamość
- **id_karty:** `REPO-PERCEPTUAL_MEMORY-8166`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/perceptual_memory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `1.232`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/perceptual_memory.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 1.232 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
CIEL/Ω Memory Architecture - M0 Perceptual Memory

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** PerceptualMemory
- **funkcje:** `normalize_text`, `_compute_identity_alignment`, `_infer_novelty`, `_source_id`, `compute_input_force`, `store`, `observe`, `decay`, `retrieve`, `active_items`, `snapshot`, `evict_decayed`

## Opis
CIEL/Ω Memory Architecture - M0 Perceptual Memory

Conservative perceptual ingress buffer. M0 is a fast first-order channel with
strong decay, high plasticity, and no direct write path into IdentityField or M6.
It stores raw percepts transiently and supports salience-ranked retrieval.
