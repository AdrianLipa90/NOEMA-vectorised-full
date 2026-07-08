# stage0_radical_cards.py — build/lib/cielingo/stage0_radical_cards.py

## Tożsamość
- **id_karty:** `REPO-STAGE0_RADICAL_CARDS-7D8A`
- **ścieżka:** `build/lib/cielingo/stage0_radical_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.418`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/stage0_radical_cards.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.418 |
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
