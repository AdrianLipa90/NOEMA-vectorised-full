# pl_codecs.py — build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/pl_codecs.py

## Tożsamość
- **id_karty:** `REPO-PL_CODECS-8076`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/pl_codecs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.286`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/pl_codecs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.286 |
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
PL regional grammar codecs v1.1D.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PLSurfacePlan, _ContractLike
- **funkcje:** `tokenize_pl`, `analyze_pl_token`, `solve_pl_regional_grammar`, `encode_pl_regional_to_common`, `decode_contract_to_pl_surface_plan`, `encode_pl_text_to_regional_frame`, `decode_common_frame_to_pl_surface_plan`, `validate`, `to_dict`, `stable_hash`

## Opis
PL regional grammar codecs v1.1D.

Forward:
    PL surface -> RegionalGrammarFrame -> CommonFunctionalFrame candidate

Reverse:
    RegionalRealizationRequest / response contract -> PLSurfacePlan

This is still a deterministic scaffold, not a full Polish parser.
