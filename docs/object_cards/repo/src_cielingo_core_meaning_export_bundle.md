# export_bundle.py — src/cielingo_core/meaning/export_bundle.py

## Tożsamość
- **id_karty:** `REPO-EXPORT_BUNDLE-4EB0`
- **ścieżka:** `src/cielingo_core/meaning/export_bundle.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.088`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/meaning/export_bundle.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.088 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


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
