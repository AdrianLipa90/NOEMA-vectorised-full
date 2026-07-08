# case_hints.py — src/cielingo_core/language_spaces/pl/case_hints.py

## Tożsamość
- **id_karty:** `REPO-CASE_HINTS-CA13`
- **ścieżka:** `src/cielingo_core/language_spaces/pl/case_hints.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.311`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/language_spaces/pl/case_hints.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.311 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Polish case hints v0.2.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CaseHint
- **funkcje:** `infer_case_hints`, `case_hints_to_notes`, `to_dict`

## Opis
Polish case hints v0.2.

This module emits case_hint candidates only. It is not a full Polish
morphological analyzer and must not claim final grammatical case recognition.
