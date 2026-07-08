# global_filesense_adapter.py — build/bdist.linux-x86_64/wheel/cielingo_core/bridge/global_filesense_adapter.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_FILESENSE_ADA-2A4B`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/bridge/global_filesense_adapter.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.461`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/bridge/global_filesense_adapter.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.461 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


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
