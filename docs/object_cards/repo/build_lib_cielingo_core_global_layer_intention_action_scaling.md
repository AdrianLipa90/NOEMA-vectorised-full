# intention_action_scaling.py — build/lib/cielingo_core/global_layer/intention_action_scaling.py

## Tożsamość
- **id_karty:** `REPO-INTENTION_ACTION_SCA-52E1`
- **ścieżka:** `build/lib/cielingo_core/global_layer/intention_action_scaling.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.587`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/intention_action_scaling.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.587 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


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
