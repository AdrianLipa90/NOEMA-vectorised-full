# episodic.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/episodic.py

## Tożsamość
- **id_karty:** `REPO-EPISODIC-7067`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/episodic.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `5.684`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/episodic.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 5.684 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
CIEL/Ω Memory Architecture - M2: Episodic Memory

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** Episode, EpisodicMemory
- **funkcje:** `to_dict`, `compute_input_force`, `store`, `retrieve`, `_context_matches`, `_should_consolidate`, `compute_consolidation_score`, `get_consolidation_candidates`, `mark_consolidated`, `_save_to_disk`, `_load_from_disk`, `get_statistics`

## Opis
CIEL/Ω Memory Architecture - M2: Episodic Memory

Memory of events and sequences. Records what happened, when, in what context,
and with what result. Medium timescale, good temporal localization.

τ=12, r=0.55, g=0.45, δ_max=0.16π

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
