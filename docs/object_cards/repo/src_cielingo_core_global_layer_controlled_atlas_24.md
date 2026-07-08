# controlled_atlas_24.py — src/cielingo_core/global_layer/controlled_atlas_24.py

## Tożsamość
- **id_karty:** `REPO-CONTROLLED_ATLAS_24-06FB`
- **ścieżka:** `src/cielingo_core/global_layer/controlled_atlas_24.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.628`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/controlled_atlas_24.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.628 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Controlled 24-slot PL/EN/JA atlas for Phase 0.5E.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AtlasAlignmentRecord
- **funkcje:** `build_taxonomy_records`, `generate_controlled_atlas_cards`, `validate_controlled_atlas`, `to_dict`

## Opis
Controlled 24-slot PL/EN/JA atlas for Phase 0.5E.

This is a constrained atlas build:
- 24 GLOBAL slots,
- PL/EN/JA cards where safe,
- explicit native-review caution for JA,
- no SOURCE default,
- no canon default,
- no semantic identity claim across languages,
- no NOEMA writeback or CURRENT update.

It is not a regional parser and does not perform morphology.
