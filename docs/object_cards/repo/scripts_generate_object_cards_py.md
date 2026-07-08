# generate_object_cards_py.py — scripts/generate_object_cards_py.py

## Tożsamość
- **id_karty:** `REPO-GENERATE_OBJECT_CARD-D6A2`
- **ścieżka:** `scripts/generate_object_cards_py.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.065`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/generate_object_cards_py.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.065 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
Natywny generator kart obiektow PhaseNav dla plikow .py.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_folder_class`, `_phi_from_path`, `_parse_py`, `_slug`, `_card_path`, `_card_id`, `build_card`, `_should_update`, `_iter_py_files`, `run`

## Opis
Natywny generator kart obiektow PhaseNav dla plikow .py.

For each .py file (filtered by path), the script parses AST, extracts
classes/functions, assigns orbital_level/theta/horizon_class from folder
rules, links the file to the correct attractor sector, and writes or updates
docs/object_cards/repo/<slug>.md.

Usage:
    python scripts/generate_object_cards_py.py [--all] [--path SRC_PATH]
    --a
