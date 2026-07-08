# unknown_word_audit.py — src/cielingo/unknown_word_audit.py

## Tożsamość
- **id_karty:** `REPO-UNKNOWN_WORD_AUDIT-21D2`
- **ścieżka:** `src/cielingo/unknown_word_audit.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.052`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/unknown_word_audit.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.052 |
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
CIELingo unknown-word audit surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UnknownWordAuditEntry, UnknownCluster, UnknownWordAuditReport
- **funkcje:** `utc_now`, `normalize_word`, `has_polish_signal`, `read_jsonl`, `write_json`, `write_jsonl`, `_card_semantic`, `_candidate_surface`, `_source_record`, `classify_unknown_word`, `collatz_learning_cycle`, `audit_entry_from_card`, `load_unknown_candidate_cards`, `count_by`, `build_unknown_clusters`, `source_lookup_record`, `candidate_0_5_record`, `review_batches`, `audit_unknown_words`

## Opis
CIELingo unknown-word audit surface.

The audit turns productive failure into a structured learning queue.  It reads
``unknown_word_candidate`` cards generated from the meaning-debt bundle and
classifies the reason why each word is unknown without promoting any word to
canon.

Rules:
* unknown is a valid state, not a failure terminal;
* sequence/card ordinals are provenance only and never semantic
