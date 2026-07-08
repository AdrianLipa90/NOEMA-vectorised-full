# affective_lexicon.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/affective_lexicon.py

## Tożsamość
- **id_karty:** `REPO-AFFECTIVE_LEXICON-E0CF`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/affective_lexicon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `6.271`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/affective_lexicon.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 6.271 |
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
CIEL Affective-Semantic Lexicon — VAD model with holonomic phase geometry.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** LexiconEntry, AffectiveLexicon, _PatchedLex
- **funkcje:** `_vad_to_phase`, `_vad_distance`, `_cyclic_distance`, `get_lexicon`, `annotate`, `phi_affective`, `memorise_id`, `as_tsm_row`, `_rebuild_index`, `add`, `get`, `query_text`, `query_vad`, `query_resonant`, `annotate_text`, `stats`, `import_to_holonomic`, `import_to_holonomic`

## Opis
CIEL Affective-Semantic Lexicon — VAD model with holonomic phase geometry.

Three-dimensional affect space:
    V  — Valence     [-1, +1]  (negative ↔ positive)
    A  — Arousal     [ 0,  1]  (calm ↔ excited)
    D  — Dominance   [-1, +1]  (submissive ↔ dominant)

Phase encoding:
    phi_V = 2π * (V + 1) / 2          → [0, 2π]
    phi_A = 2π * A                     → [0, 2π]
    phi_D = 2π * (D +
