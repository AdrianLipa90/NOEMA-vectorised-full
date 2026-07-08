# semantic_encoder.py — build/bdist.linux-x86_64/wheel/cielingo/semantic_encoder.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_ENCODER-CC1E`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo/semantic_encoder.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.087`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo/semantic_encoder.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.087 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
CIELingo Semantic Encoder — twój TRANSFORMEM, wektoryzowany.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** EncoderResult, CIELingoSemanticEncoder
- **funkcje:** `_spec_dim`, `_total_spec_dim`, `_feature_dim`, `_build_axes`, `_vowel_ratio`, `_word_length_bins`, `_affect_bias`, `_semantic_mass`, `_operator_incidence`, `_build_feature_vector`, `_tokenize`, `_fallback`, `_normalize_pl`, `_resolve_oscillator`, `get_encoder`, `encode`, `_set`, `encode`, `_phase`, `_sectors`, `_coherence`, `_empty`

## Opis
CIELingo Semantic Encoder — twój TRANSFORMEM, wektoryzowany.

Używa transformer_features.FeatureToken + encode_feature_token() jako
warstwy ekstrakcji cech. Żadnych zewnętrznych zależności — tylko numpy.
