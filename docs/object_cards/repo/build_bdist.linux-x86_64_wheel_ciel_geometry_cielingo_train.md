# cielingo_train.py — build/bdist.linux-x86_64/wheel/ciel_geometry/cielingo_train.py

## Tożsamość
- **id_karty:** `REPO-CIELINGO_TRAIN-155E`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/cielingo_train.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.037`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/cielingo_train.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.037 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
CIELingo Training Pipeline — trenuj asocjacyjną pamięć fazową na Knowledge DB + linux cards.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
