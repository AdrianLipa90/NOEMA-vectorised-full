# meaning_action.py — src/cielingo_core/global_layer/meaning_action.py

## Tożsamość
- **id_karty:** `REPO-MEANING_ACTION-04C6`
- **ścieżka:** `src/cielingo_core/global_layer/meaning_action.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.684`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/meaning_action.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.684 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
MeaningAction and MeaningBlockAction.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MeaningAction, MeaningBlockAction
- **funkcje:** `_bounded_delta`, `action_from_operator`, `validate`, `to_dict`, `total_semantic_mass_delta`, `total_affect_delta`, `total_certainty_delta`, `total_consent_pressure_delta`, `total_source_pressure_delta`, `total_residue_delta`, `validate`, `to_dict`

## Opis
MeaningAction and MeaningBlockAction.

Inspired by the block-action idea: local operators have local effects; a
sequence of operators produces a block-level semantic effect.
