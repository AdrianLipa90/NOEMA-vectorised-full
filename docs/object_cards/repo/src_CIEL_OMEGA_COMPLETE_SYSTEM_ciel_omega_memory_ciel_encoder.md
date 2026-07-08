# ciel_encoder.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/ciel_encoder.py

## Tożsamość
- **id_karty:** `REPO-CIEL_ENCODER-4D97`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/ciel_encoder.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `2.707`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/ciel_encoder.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 2.707 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
CIEL Semantic Phase Encoder.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** EncoderResult, CIELEncoder
- **funkcje:** `_get_channel_weights`, `_hash_embedding`, `_hash_phase`, `_load_texts_from_jsonl`, `get_encoder`, `encode`, `retrain_from_corpus`, `_embed`, `_embed_batch`, `_get_model`, `_phase_projection`, `_blend_htri`, `_blend_nonlocal`, `_get_nonlocal_phase`, `_get_htri_phase`, `_sector_distribution`, `_local_coherence`, `_update_context`, `_load_or_init_weights`, `_fit_weights`, `_random_weights`, `_save_weights`

## Opis
CIEL Semantic Phase Encoder.

Replaces SHA-256 hash phase with a real semantic embedding projected onto S¹.
Architecture: sentence-transformer → PCA phase projection → sector softmax.

Outputs per text:
    phase   float  [0, 2π)  — semantic position on circle
    sector  ndarray(10,)    — soft assignment to orbital sectors
    coherence float [0,1]   — cosine similarity to recent context window
