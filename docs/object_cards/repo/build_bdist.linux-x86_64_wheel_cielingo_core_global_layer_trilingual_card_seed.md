# trilingual_card_seed.py — build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/trilingual_card_seed.py

## Tożsamość
- **id_karty:** `REPO-TRILINGUAL_CARD_SEED-639F`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/trilingual_card_seed.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.703`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/global_layer/trilingual_card_seed.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.703 |
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
Trilingual runtime-card seed for CIELingo v0.3b.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TrilingualAlignmentRecord
- **funkcje:** `generate_trilingual_runtime_cards`, `validate_trilingual_runtime_cards`, `to_dict`

## Opis
Trilingual runtime-card seed for CIELingo v0.3b.

Produces aligned PL/EN/JA cards over shared global slot_id values.

Important:
- alignment is slot correspondence, not semantic identity;
- Japanese entries remain draft / native-review candidates;
- NOEMA holonomic markers are public-safe commitments, not writeback;
- SOURCE and canon are never default.
