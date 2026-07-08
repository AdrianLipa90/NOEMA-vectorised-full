# lns_language_cards.py — src/cielingo/lns_language_cards.py

## Tożsamość
- **id_karty:** `REPO-LNS_LANGUAGE_CARDS-8C03`
- **ścieżka:** `src/cielingo/lns_language_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.323`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/lns_language_cards.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.323 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


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
