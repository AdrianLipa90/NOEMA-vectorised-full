# global_codecs.py — build/lib/cielingo_core/global_layer/global_codecs.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_CODECS-9326`
- **ścieżka:** `build/lib/cielingo_core/global_layer/global_codecs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.665`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/global_codecs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.665 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


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
