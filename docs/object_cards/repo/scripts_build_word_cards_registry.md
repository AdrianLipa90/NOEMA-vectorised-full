# build_word_cards_registry.py — scripts/build_word_cards_registry.py

## Tożsamość
- **id_karty:** `REPO-BUILD_WORD_CARDS_REG-10EC`
- **ścieżka:** `scripts/build_word_cards_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `6.178`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/build_word_cards_registry.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 6.178 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Build word cards registry from docs/object_cards/words/*.md

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `parse_word_card`, `build_edges`, `update_index`, `main`, `get_field`, `get_list_field`, `add_edge`

## Opis
Build word cards registry from docs/object_cards/words/*.md

Generates:
  integration/registries/words/word_cards_registry.json
  integration/registries/words/word_semantic_edges.json
