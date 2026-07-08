# stage0_radical_cards.py — src/cielingo/stage0_radical_cards.py

## Tożsamość
- **id_karty:** `REPO-STAGE0_RADICAL_CARDS-7FA7`
- **ścieżka:** `src/cielingo/stage0_radical_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.937`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/stage0_radical_cards.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.937 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
CIELingo Stage 0 radical cards and EN/JA language-slot entries.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RadicalCard, LanguageSlotEntry, AlignmentRecord
- **funkcje:** `read_jsonl`, `load_radicals`, `load_language_entries`, `load_alignments`, `validate_all`, `from_dict`, `validate`, `from_dict`, `validate`, `from_dict`, `validate`

## Opis
CIELingo Stage 0 radical cards and EN/JA language-slot entries.

This module is intentionally small and dependency-free. It validates the
Stage 0 data contract without pretending that Japanese draft entries have
native-speaker validation.

Core distinction:
- RadicalCard: global semantic radical / invariant axis.
- LanguageSlotEntry: language-local realization of a slot with local holonomy.
- Alig
