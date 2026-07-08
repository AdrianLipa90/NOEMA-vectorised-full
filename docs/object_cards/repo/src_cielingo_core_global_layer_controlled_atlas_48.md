# controlled_atlas_48.py — src/cielingo_core/global_layer/controlled_atlas_48.py

## Tożsamość
- **id_karty:** `REPO-CONTROLLED_ATLAS_48-8BBD`
- **ścieżka:** `src/cielingo_core/global_layer/controlled_atlas_48.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.531`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/controlled_atlas_48.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.531 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
Controlled 48-slot PL/EN/JA atlas for Phase 0.6A.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `build_taxonomy_records_48`, `generate_controlled_atlas_48_cards`, `validate_controlled_atlas_48`

## Opis
Controlled 48-slot PL/EN/JA atlas for Phase 0.6A.

This extends the 0.5E 24-slot atlas additively:
- 48 GLOBAL slots total,
- PL/EN/JA cards for every slot,
- explicit native-review caution for JA,
- no SOURCE default,
- no canon default,
- no semantic identity claim across languages,
- no NOEMA writeback or CURRENT update.

This is not a regional parser, not a morphology engine, and not a transla
