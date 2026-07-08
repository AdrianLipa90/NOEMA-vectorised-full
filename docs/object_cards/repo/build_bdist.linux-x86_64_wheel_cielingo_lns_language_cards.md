# lns_language_cards.py — build/bdist.linux-x86_64/wheel/cielingo/lns_language_cards.py

## Tożsamość
- **id_karty:** `REPO-LNS_LANGUAGE_CARDS-74B4`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo/lns_language_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.485`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo/lns_language_cards.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.485 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
NOEMA/LNS-backed language-card loader for CIELingo.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LNSLanguageCard
- **funkcje:** `_read_json`, `_repo_root`, `_data_root`, `_labels_from_concept`, `_labels_from_operator`, `_source_path_str`, `_phase_from_id`, `load_lns_concept_cards`, `load_lns_operator_cards`, `load_noema_index_language_cards`, `load_all_language_cards`, `language_card_inventory`, `search_language_cards`, `as_dict`

## Opis
NOEMA/LNS-backed language-card loader for CIELingo.

This module treats the embedded ``ciel_lingophysics_lns_repo_v2_3`` data as the
local NOEMA language-card surface.  It does not import external dictionaries and
it does not promote draft seed cards to canon.  It only exposes deterministic
inventory/search structures that runtime modules can consume.
