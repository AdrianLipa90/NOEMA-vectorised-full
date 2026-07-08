# global_codecs.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/global_codecs.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_CODECS-526E`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/global_codecs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.620`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/global_codecs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.620 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
GLOBAL codecs v1.1C: forward common-frame encode and reverse regional request.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GlobalEncodeReport, RegionalRealizationRequest
- **funkcje:** `encode_surface_to_common_frame`, `decode_contract_to_regional_request`, `validate`, `to_dict`, `stable_hash`, `validate`, `to_dict`, `stable_hash`

## Opis
GLOBAL codecs v1.1C: forward common-frame encode and reverse regional request.
