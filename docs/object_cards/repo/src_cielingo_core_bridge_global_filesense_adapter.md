# global_filesense_adapter.py — src/cielingo_core/bridge/global_filesense_adapter.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_FILESENSE_ADA-2657`
- **ścieżka:** `src/cielingo_core/bridge/global_filesense_adapter.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.103`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/bridge/global_filesense_adapter.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.103 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


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
