# runtime_adapter_interface.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/runtime_adapter_interface.py

## Tożsamość
- **id_karty:** `REPO-RUNTIME_ADAPTER_INTE-01A8`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/runtime_adapter_interface.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.709`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/runtime_adapter_interface.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.709 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Controlled runtime adapter interface v0.9A.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RuntimeAdapterAction, RuntimeAdapterReference
- **funkcje:** `adapt_runtime_dry_run_reference`, `validate`, `to_dict`, `stable_hash`

## Opis
Controlled runtime adapter interface v0.9A.

A typed adapter boundary for consuming RuntimeBridgeDryRunResult.

Boundary:
- adapter is dry-run only;
- adapter returns a reference handle, not execution;
- adapter does not write NOEMA;
- adapter does not update CURRENT;
- adapter does not promote SOURCE/canon.
