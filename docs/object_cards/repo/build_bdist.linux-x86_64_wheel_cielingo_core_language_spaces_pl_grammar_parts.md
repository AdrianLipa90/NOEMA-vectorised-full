# grammar_parts.py — build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/grammar_parts.py

## Tożsamość
- **id_karty:** `REPO-GRAMMAR_PARTS-907A`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/grammar_parts.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.128`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/grammar_parts.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.128 |
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
Polish regional grammar parts v1.1D.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PartOfSpeech, SentencePart, MorphologyFeature, SemanticOperatorRole
- **funkcje:** `is_part_of_speech`, `is_sentence_part`, `is_morphology_feature`, `classify_pl_token_part_of_speech`, `classify_pl_semantic_operator_role`, `sentence_part_from_pos_and_operator`

## Opis
Polish regional grammar parts v1.1D.

This module intentionally separates:
- PartOfSpeech: what a token is locally.
- SentencePart: what role it plays in Polish syntax.
- MorphologyFeature: inflectional/morphological descriptors.
- SemanticOperatorRole: bridge roles toward GLOBAL, not identical to POS.
