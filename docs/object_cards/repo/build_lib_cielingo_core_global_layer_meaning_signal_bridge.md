# meaning_signal_bridge.py — build/lib/cielingo_core/global_layer/meaning_signal_bridge.py

## Tożsamość
- **id_karty:** `REPO-MEANING_SIGNAL_BRIDG-63AF`
- **ścieżka:** `build/lib/cielingo_core/global_layer/meaning_signal_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.687`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/meaning_signal_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.687 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


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
