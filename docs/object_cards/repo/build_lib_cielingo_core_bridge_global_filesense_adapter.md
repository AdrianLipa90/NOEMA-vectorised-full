# global_filesense_adapter.py — build/lib/cielingo_core/bridge/global_filesense_adapter.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_FILESENSE_ADA-DB48`
- **ścieżka:** `build/lib/cielingo_core/bridge/global_filesense_adapter.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.791`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/bridge/global_filesense_adapter.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.791 |
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
GLOBAL execution through FileSense surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FileSenseGlobalResult
- **funkcje:** `operators_from_cards`, `slots_from_cards`, `build_equation_from_filesense`, `run_filesense_global`, `to_dict`

## Opis
GLOBAL execution through FileSense surface.

Pipeline:
  query
  -> FileSense card search
  -> operator extraction from runtime cards
  -> MeaningEquation construction
  -> GLOBAL v0.2 evaluation
  -> FileSenseGlobalResult

This is not regional parsing. It is a fast evidence/card retrieval layer that
feeds GLOBAL candidate evaluation.
