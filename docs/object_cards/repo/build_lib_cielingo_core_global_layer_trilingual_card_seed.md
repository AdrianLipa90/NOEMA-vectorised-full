# trilingual_card_seed.py — build/lib/cielingo_core/global_layer/trilingual_card_seed.py

## Tożsamość
- **id_karty:** `REPO-TRILINGUAL_CARD_SEED-5EF9`
- **ścieżka:** `build/lib/cielingo_core/global_layer/trilingual_card_seed.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.167`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/trilingual_card_seed.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.167 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


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
