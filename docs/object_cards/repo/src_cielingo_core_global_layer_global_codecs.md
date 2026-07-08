# global_codecs.py — src/cielingo_core/global_layer/global_codecs.py

## Tożsamość
- **id_karty:** `REPO-GLOBAL_CODECS-AAD7`
- **ścieżka:** `src/cielingo_core/global_layer/global_codecs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.436`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/global_codecs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.436 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


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
