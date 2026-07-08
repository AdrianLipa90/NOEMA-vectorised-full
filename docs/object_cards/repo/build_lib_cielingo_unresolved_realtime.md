# unresolved_realtime.py — build/lib/cielingo/unresolved_realtime.py

## Tożsamość
- **id_karty:** `REPO-UNRESOLVED_REALTIME-532A`
- **ścieżka:** `build/lib/cielingo/unresolved_realtime.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.026`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/unresolved_realtime.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.026 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
CIELingo real-time unresolved-word protocol.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UnresolvedWordEvent, SourceEvidence, CandidateWordCard, RealtimeUnresolvedReport
- **funkcje:** `utc_now`, `today_utc`, `normalize_word`, `stable_unit`, `sha256_json`, `safe_slug`, `runtime_root`, `evidence_root`, `_jsonl_records`, `load_source_evidence`, `source_candidates_for_word`, `_context_window`, `unresolved_events_from_text`, `_append_jsonl`, `_candidate_card_id`, `_source_summary`, `build_candidate_word_card`, `candidate_path_for_card`, `record_realtime_unresolved`, `daily_unresolved_rollup`, `as_dict`, `as_dict`, `as_dict`, `as_dict`

## Opis
CIELingo real-time unresolved-word protocol.

This module turns unknown phase-sense tokens into an append-only unresolved
stream and, when local source evidence is available, creates supervised
candidate word cards with initial confidence 0.5.

Design constraints:
* no automatic canonization;
* no network access or live external claims;
* card sequence numbers and filenames are technical only;
* e
