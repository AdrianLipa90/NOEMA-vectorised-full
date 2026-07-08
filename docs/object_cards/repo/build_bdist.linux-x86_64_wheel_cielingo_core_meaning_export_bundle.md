# export_bundle.py — build/bdist.linux-x86_64/wheel/cielingo_core/meaning/export_bundle.py

## Tożsamość
- **id_karty:** `REPO-EXPORT_BUNDLE-200F`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/meaning/export_bundle.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.688`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/meaning/export_bundle.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.688 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


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
