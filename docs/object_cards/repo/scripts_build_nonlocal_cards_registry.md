# build_nonlocal_cards_registry.py — scripts/build_nonlocal_cards_registry.py

## Tożsamość
- **id_karty:** `REPO-BUILD_NONLOCAL_CARDS-B7F1`
- **ścieżka:** `scripts/build_nonlocal_cards_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.025`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/build_nonlocal_cards_registry.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.025 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Build nonlocal_cards_registry.json + .csv from docs/object_cards/nonlocal/*.md.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_strip`, `_parse_card`, `main`

## Opis
Build nonlocal_cards_registry.json + .csv from docs/object_cards/nonlocal/*.md.

Single source of truth: the .md files.
The script parses each NL-*.md and extracts card_id, name, class,
active_status, anchors, role, input_from, output_to, authority_rule,
horizon_relation.  Fields missing from a card get empty-string defaults.
