# meaning_signal_bridge.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/meaning_signal_bridge.py

## Tożsamość
- **id_karty:** `REPO-MEANING_SIGNAL_BRIDG-C02C`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/meaning_signal_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.563`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/meaning_signal_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.563 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
GLOBAL signal bridge integration for MeaningLoop repair routing v0.8A.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GlobalSignalSeverity, GlobalMeaningSignal
- **funkcje:** `build_global_meaning_signal`, `validate`, `to_dict`, `stable_hash`

## Opis
GLOBAL signal bridge integration for MeaningLoop repair routing v0.8A.

Converts MeaningLoop + RepairRouting diagnostics into a safe global signal.

Boundary:
- signal is advisory, not execution;
- no SOURCE/canon promotion;
- no NOEMA writeback;
- no CURRENT update.
