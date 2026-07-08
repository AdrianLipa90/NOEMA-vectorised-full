# grammar_parts.py — src/cielingo_core/language_spaces/pl/grammar_parts.py

## Tożsamość
- **id_karty:** `REPO-GRAMMAR_PARTS-54FA`
- **ścieżka:** `src/cielingo_core/language_spaces/pl/grammar_parts.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.005`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/language_spaces/pl/grammar_parts.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.005 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
