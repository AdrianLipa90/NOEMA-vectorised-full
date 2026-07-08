# pl_codecs.py — build/lib/cielingo_core/language_spaces/pl/pl_codecs.py

## Tożsamość
- **id_karty:** `REPO-PL_CODECS-491F`
- **ścieżka:** `build/lib/cielingo_core/language_spaces/pl/pl_codecs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.560`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/language_spaces/pl/pl_codecs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.560 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


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
