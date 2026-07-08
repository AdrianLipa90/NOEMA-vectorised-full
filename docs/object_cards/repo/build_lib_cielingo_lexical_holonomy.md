# lexical_holonomy.py — build/lib/cielingo/lexical_holonomy.py

## Tożsamość
- **id_karty:** `REPO-LEXICAL_HOLONOMY-EFCF`
- **ścieżka:** `build/lib/cielingo/lexical_holonomy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.390`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/lexical_holonomy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.390 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
CIELingo lexical holonomy surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LexicalUnit, LexicalHolonomyEdge, WordKnowledgeNote, LanguageCardFileRef
- **funkcje:** `_repo_root`, `_data_root`, `_read_json`, `_sha256`, `_norm_surface`, `_lexical_id`, `_angle_delta`, `_bounded`, `_family`, `_relation_weight`, `list_language_card_files`, `read_language_card_file`, `_concept_payload_by_card`, `extract_lexical_units`, `_index_units`, `_edge`, `_vector_distance`, `build_lexical_holonomy_edges`, `build_word_knowledge_notes`, `lexical_holonomy_report`, `write_lexical_holonomy_report`, `as_dict`, `as_dict`, `as_dict`, `as_dict`, `match_text`

## Opis
CIELingo lexical holonomy surface.

This module establishes relations *between words*, not just vectors for cards.
It uses the local NOEMA/LNS language-card files as the primary surface and
keeps all external/open-source lexical resources as provenance descriptors until
an explicit verified dump/API import is provided.

Implemented relation layers:

* card-internal seed relations: near synonyms, a
