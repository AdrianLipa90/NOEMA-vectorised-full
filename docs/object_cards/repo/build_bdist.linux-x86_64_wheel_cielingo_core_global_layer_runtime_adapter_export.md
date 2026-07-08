# runtime_adapter_export.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/runtime_adapter_export.py

## Tożsamość
- **id_karty:** `REPO-RUNTIME_ADAPTER_EXPO-DB1B`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/runtime_adapter_export.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.935`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/runtime_adapter_export.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.935 |
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
Runtime adapter reference export v0.9B.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RuntimeAdapterReferenceExportBundle
- **funkcje:** `build_runtime_adapter_reference_export_bundle`, `validate`, `to_dict`, `stable_hash`, `write_json`

## Opis
Runtime adapter reference export v0.9B.

Exports RuntimeAdapterReference collections and global dry-test references as
local artifact-grounded reference bundles.

Boundary:
- export bundle is not SOURCE;
- export bundle is not canon;
- export bundle does not write NOEMA;
- export bundle does not update CURRENT;
- export bundle does not execute runtime actions.
