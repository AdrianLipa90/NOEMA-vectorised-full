# working_memory.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/working_memory.py

## Tożsamość
- **id_karty:** `REPO-WORKING_MEMORY-E4B7`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/working_memory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `6.010`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/working_memory.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 6.010 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
CIEL/Ω Memory Architecture - M1 Working Memory

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** WorkingMemory
- **funkcje:** `normalize_text`, `_compute_identity_alignment`, `_episode_id`, `compute_input_force`, `store`, `observe`, `decay`, `reinforce`, `retrieve`, `active_items`, `snapshot`, `retrieve_raw`, `evict_decayed`

## Opis
CIEL/Ω Memory Architecture - M1 Working Memory

Conservative active operational field between perception and consolidation.
Working memory is short-lived, decays without reinforcement, and does not
write directly to IdentityField or M6.
