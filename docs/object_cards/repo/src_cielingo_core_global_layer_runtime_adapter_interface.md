# runtime_adapter_interface.py — src/cielingo_core/global_layer/runtime_adapter_interface.py

## Tożsamość
- **id_karty:** `REPO-RUNTIME_ADAPTER_INTE-0F25`
- **ścieżka:** `src/cielingo_core/global_layer/runtime_adapter_interface.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.651`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/runtime_adapter_interface.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.651 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


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
