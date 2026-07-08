# cielingo_train.py — src/ciel_geometry/cielingo_train.py

## Tożsamość
- **id_karty:** `REPO-CIELINGO_TRAIN-0E2C`
- **ścieżka:** `src/ciel_geometry/cielingo_train.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `3.327`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/cielingo_train.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 3.327 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

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
CIELingo Training Pipeline — trenuj asocjacyjną pamięć fazową na Knowledge DB + linux cards.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_theme_to_group`, `train_from_knowledge_db`, `train_from_texts`, `_build_enriched_text`, `train_from_knowledge_db`

## Opis
CIELingo Training Pipeline — trenuj asocjacyjną pamięć fazową na Knowledge DB + linux cards.

Strategia treningu:
1. Knowledge DB (545 docs): TF-IDF → tematy → 36D fazy
2. Linux cards (613 kart): 36D phi bezpośrednio z indeksu
3. CIELingo coupling: text → build_lingo_frame → 36D fazy (full encoder)

Tryby enkodowania:
- fast: TF-IDF + themes → 36D (szybki, ~0.01s/doc)
- full: build_lingo_frame → 3
