# identity_types.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/identity_types.py

## Tożsamość
- **id_karty:** `REPO-IDENTITY_TYPES-33E7`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/identity_types.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `5.822`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/identity_types.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 5.822 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

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
CIEL/Ω Memory Architecture - Identity Memory Types

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** IdentityTrace, IdentityAnchorCandidate, IdentityMemorySnapshot, IdentityConsolidationScore
- **funkcje:** `is_detected`, `is_mature`, `compute_total`

## Opis
CIEL/Ω Memory Architecture - Identity Memory Types

Data structures for M6 IdentityMemory channel. This channel stores
historical traces of identity stabilization, not the current identity
attractor (which remains IdentityField).

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
