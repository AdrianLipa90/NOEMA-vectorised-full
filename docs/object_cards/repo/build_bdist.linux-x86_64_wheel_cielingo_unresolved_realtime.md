# unresolved_realtime.py — build/bdist.linux-x86_64/wheel/cielingo/unresolved_realtime.py

## Tożsamość
- **id_karty:** `REPO-UNRESOLVED_REALTIME-CAC1`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo/unresolved_realtime.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.168`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo/unresolved_realtime.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.168 |
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
