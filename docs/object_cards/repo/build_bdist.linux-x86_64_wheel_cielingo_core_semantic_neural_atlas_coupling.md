# atlas_coupling.py — build/bdist.linux-x86_64/wheel/cielingo_core/semantic_neural/atlas_coupling.py

## Tożsamość
- **id_karty:** `REPO-ATLAS_COUPLING-2308`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/semantic_neural/atlas_coupling.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.973`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/semantic_neural/atlas_coupling.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.973 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


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
