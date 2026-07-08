# intention_action_scaling.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/intention_action_scaling.py

## Tożsamość
- **id_karty:** `REPO-INTENTION_ACTION_SCA-92ED`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/intention_action_scaling.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.312`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/intention_action_scaling.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.312 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
GLOBAL 0.5C intention-to-action scaling scaffold.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** IntentionActionScaling
- **funkcje:** `_bounded01`, `scale_meaning_action`, `validate`, `below_ethical_bound`, `to_dict`

## Opis
GLOBAL 0.5C intention-to-action scaling scaffold.

Intention may scale semantic deltas. It never executes runtime actions,
never writes NOEMA, and never claims physical manifestation.
