# holonomic_memory.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/holonomic_memory.py

## Tożsamość
- **id_karty:** `REPO-HOLONOMIC_MEMORY-6F0A`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/holonomic_memory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `4.792`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/holonomic_memory.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 4.792 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

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
Holonomic Semantic Memory — phase-weighted retrieval layer over TSM.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** HolonomicMemory
- **funkcje:** `_cyclic_distance`, `_holonomic_weight`, `stamp_pipeline_output`, `import_ciel_memories`, `_ensure_nonlocal_index`, `_connect`, `_ensure_schema`, `update_holonomy`, `stamp_new`, `_get_hebbian_params`, `hebbian_update`, `edge_neighbors`, `edge_stats`, `retrieve_resonant`, `retrieve_weighted`, `stats`, `_text_phase`, `_text_w_semantic`, `_blend_phase`, `_insert_if_new`, `_insert_durable`, `_insert_noema_link`, `_zeta`

## Opis
Holonomic Semantic Memory — phase-weighted retrieval layer over TSM.

Extends TSMWriterSQL with Berry holonomy columns. Each memory entry
accumulates a geometric phase as it passes through orbital cycles.
Retrieval is phase-resonant: entries whose phi_berry is close (cyclically)
to the current orbital target_phase are weighted higher.

Schema extension (ALTER TABLE, idempotent):
    phi_berry
