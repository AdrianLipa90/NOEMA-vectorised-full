# atlas_coupling.py — build/lib/cielingo_core/semantic_neural/atlas_coupling.py

## Tożsamość
- **id_karty:** `REPO-ATLAS_COUPLING-4638`
- **ścieżka:** `build/lib/cielingo_core/semantic_neural/atlas_coupling.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.803`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/semantic_neural/atlas_coupling.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.803 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
Atlas-driven sentence/card coupling v0.6B.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AtlasCardLink, SentenceCardCouplingReport
- **funkcje:** `clamp01`, `load_atlas_cards_by_language_and_slot`, `load_atlas_cards_by_language_and_surface`, `_make_link`, `build_sentence_card_coupling`, `validate`, `to_dict`, `validate`, `to_dict`, `stable_hash`

## Opis
Atlas-driven sentence/card coupling v0.6B.

Couples SentenceStateSnapshot nodes to controlled atlas cards by slot_id and
language_id.

Boundary:
- coupling_candidate ≠ semantic identity;
- card link ≠ parser proof;
- slot_id = comparison/coupling axis;
- no SOURCE/canon/NOEMA/CURRENT authority;
- no runtime cognition claim.
