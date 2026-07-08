# cielingo_canonization_pipeline.py — scripts/cielingo_canonization_pipeline.py

## Tożsamość
- **id_karty:** `REPO-CIELINGO_CANONIZATIO-7F94`
- **ścieżka:** `scripts/cielingo_canonization_pipeline.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.075`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/cielingo_canonization_pipeline.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.075 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
CIELingo Canonization Pipeline — automatyczna kanonizacja kart z internetu + knowledge.db.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** KnowledgeEvidence, WebEvidence, GrammarEvidence, CanonizationEngine
- **funkcje:** `utc_now`, `normalize_word`, `stable_id`, `bounded`, `sha256_json`, `load_candidate_cards`, `main`, `lookup`, `close`, `lookup`, `close`, `validate`, `_load_existing_decisions`, `canonize_card`, `save_decisions`, `_write_report`, `close`, `print_summary`

## Opis
CIELingo Canonization Pipeline — automatyczna kanonizacja kart z internetu + knowledge.db.

Algorytm:
1.  Ładuje karty kandydujące z data/cielingo/debt_word_cards/*.jsonl
2.  Dla każdego lematu zbiera dowody:
    a) knowledge.db — TF-IDF, frekwencja w korpusie (602 docs, 54508 termów)
    b) Web fetch — Wiktionary, dictionary API (SJP, WordNet, itp.)
    c) Walidacja gramatyczna — suffix rules, PO
