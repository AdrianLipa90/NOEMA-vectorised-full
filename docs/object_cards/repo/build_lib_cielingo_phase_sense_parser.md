# phase_sense_parser.py — build/lib/cielingo/phase_sense_parser.py

## Tożsamość
- **id_karty:** `REPO-PHASE_SENSE_PARSER-8AD5`
- **ścieżka:** `build/lib/cielingo/phase_sense_parser.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.590`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/phase_sense_parser.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.590 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
CIELingo phase-sense parser.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PhaseSenseToken, PhaseSenseReport
- **funkcje:** `_norm`, `_stable_unit`, `_phase`, `_digest_payload`, `tokenize_surface`, `_card_index`, `_note_index`, `_best_note`, `_match_token`, `phase_sense_for_token`, `parse_text_to_phase_sense`, `write_phase_sense_report`, `as_dict`, `as_dict`, `mean`

## Opis
CIELingo phase-sense parser.

This layer parses surface words into phase-sense objects before output
inference consumes them.  It is intentionally local and deterministic:

* token -> own CIELingo/NOEMA language-card match;
* matched card -> 24D vector + tensor-scalar context field;
* unknown token -> guarded candidate phase with explicit low confidence;
* every token carries a phase-sense note fo
