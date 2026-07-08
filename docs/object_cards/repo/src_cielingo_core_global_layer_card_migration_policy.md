# card_migration_policy.py — src/cielingo_core/global_layer/card_migration_policy.py

## Tożsamość
- **id_karty:** `REPO-CARD_MIGRATION_POLIC-8310`
- **ścieżka:** `src/cielingo_core/global_layer/card_migration_policy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.937`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/card_migration_policy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.937 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
Card migration policy for CIELingo GLOBAL v0.2.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CardMigrationDecision
- **funkcje:** `recommend_card_migration`, `to_dict`

## Opis
Card migration policy for CIELingo GLOBAL v0.2.

Existing cards do not need to be destroyed. They need an additive runtime
extension so a word/card can act as a semantic operator, not only a lexical
entry.
