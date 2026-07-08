# common_functional_frame.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/common_functional_frame.py

## Tożsamość
- **id_karty:** `REPO-COMMON_FUNCTIONAL_FR-1CFA`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/common_functional_frame.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.952`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/common_functional_frame.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.952 |
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
CommonFunctionalFrame v1.1C.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FunctionalRole, FunctionalOperator, FunctionalSlot, ContextFrame, CommonFunctionalFrame
- **funkcje:** `_operators_for_token`, `_role_for_token`, `build_common_functional_frame`, `validate`, `operator_risk`, `to_dict`, `validate`, `to_dict`, `validate`, `semantic_mass`, `operator_risk`, `functional_entropy`, `closure_pressure`, `calculations`, `to_dict`, `stable_hash`

## Opis
CommonFunctionalFrame v1.1C.

GLOBAL common roles are language-independent functional classes. REGIONAL
layers later decide local parts of speech, sentence parts and morphology.
