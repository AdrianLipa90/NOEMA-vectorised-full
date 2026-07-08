# meaning_action.py — build/lib/cielingo_core/global_layer/meaning_action.py

## Tożsamość
- **id_karty:** `REPO-MEANING_ACTION-A8AC`
- **ścieżka:** `build/lib/cielingo_core/global_layer/meaning_action.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.334`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/meaning_action.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.334 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


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
