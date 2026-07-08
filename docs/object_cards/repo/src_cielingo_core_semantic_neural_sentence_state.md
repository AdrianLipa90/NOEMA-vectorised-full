# sentence_state.py — src/cielingo_core/semantic_neural/sentence_state.py

## Tożsamość
- **id_karty:** `REPO-SENTENCE_STATE-301A`
- **ścieżka:** `src/cielingo_core/semantic_neural/sentence_state.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.798`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/semantic_neural/sentence_state.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.798 |
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
Semantic-neural sentence state scaffold v0.5P.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CardOscillatorState, JVectorState, SentenceStateSnapshot
- **funkcje:** `clamp01`, `_slot_ids_for_token`, `build_sentence_state_snapshot`, `validate`, `to_dict`, `validate`, `to_dict`, `validate`, `to_dict`, `stable_hash`

## Opis
Semantic-neural sentence state scaffold v0.5P.

This module creates explicit sentence-state snapshots from SentenceEquation
objects. It is a scaffold for card/slot/J/residue dynamics, not a full neural
runtime or consciousness claim.

Boundaries:
- no SOURCE promotion;
- no canon promotion;
- no external NOEMA writeback;
- no CURRENT update;
- no physical Kuramoto measurement;
- no runtime cogniti
