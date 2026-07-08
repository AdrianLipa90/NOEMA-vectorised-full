# meaning_debt_word_cards.py — build/lib/cielingo/meaning_debt_word_cards.py

## Tożsamość
- **id_karty:** `REPO-MEANING_DEBT_WORD_CA-0166`
- **ścieżka:** `build/lib/cielingo/meaning_debt_word_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.418`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/meaning_debt_word_cards.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.418 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
CIELingo meaning-debt word-card scaffolder.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DebtWordRecord, DebtCandidateWordCard, DebtWordCardsReport
- **funkcje:** `utc_now`, `normalize_word`, `stable_unit`, `bounded`, `sha256_json`, `card_id_for_word`, `is_single_word`, `has_polish_signal`, `debt_flags`, `lexical_unit_type`, `is_polish_infinitive`, `part_of_speech_candidate`, `sentence_part_candidate`, `grammatical_designation`, `semantic_designation`, `read_debt_index`, `build_candidate_card`, `build_candidate_cards`, `_write_jsonl`, `_counts`, `generate_debt_word_cards`, `from_row`, `as_dict`, `as_dict`, `as_dict`

## Opis
CIELingo meaning-debt word-card scaffolder.

This module converts the previously identified CIEL-POL meaning-debt index into
supervised candidate word cards.  It deliberately does **not** promote the old
scaffolds to canon.  Every emitted word card receives a grammatical designation,
a sentence-function candidate, tensor/scalar semantic placeholders, and an
explicit confidence note.

Core rules:
*
