# stage0_radical_cards.py — build/bdist.linux-x86_64/wheel/cielingo/stage0_radical_cards.py

## Tożsamość
- **id_karty:** `REPO-STAGE0_RADICAL_CARDS-B5B9`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo/stage0_radical_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.047`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo/stage0_radical_cards.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.047 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


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
