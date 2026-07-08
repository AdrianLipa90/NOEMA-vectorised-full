# export_bundle.py — build/lib/cielingo_core/meaning/export_bundle.py

## Tożsamość
- **id_karty:** `REPO-EXPORT_BUNDLE-2A80`
- **ścieżka:** `build/lib/cielingo_core/meaning/export_bundle.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.941`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/meaning/export_bundle.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.941 |
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
MeaningLoop / Repair export bundle v0.7C.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MeaningLoopRepairExportBundle
- **funkcje:** `build_meaning_loop_repair_export_bundle`, `validate`, `to_dict`, `stable_hash`, `write_json`

## Opis
MeaningLoop / Repair export bundle v0.7C.

Exports loop + repair routing diagnostics into portable JSON objects.

Boundary:
- export is local artifact bundle, not NOEMA writeback;
- export does not update CURRENT;
- export does not canonize or promote SOURCE.
