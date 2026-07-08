# trilingual_card_seed.py — src/cielingo_core/global_layer/trilingual_card_seed.py

## Tożsamość
- **id_karty:** `REPO-TRILINGUAL_CARD_SEED-27C5`
- **ścieżka:** `src/cielingo_core/global_layer/trilingual_card_seed.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.127`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/trilingual_card_seed.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.127 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


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
