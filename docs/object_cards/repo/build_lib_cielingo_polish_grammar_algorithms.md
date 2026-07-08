# grammar_algorithms.py — build/lib/cielingo/polish/grammar_algorithms.py

## Tożsamość
- **id_karty:** `REPO-GRAMMAR_ALGORITHMS-EE4A`
- **ścieżka:** `build/lib/cielingo/polish/grammar_algorithms.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.860`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/polish/grammar_algorithms.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.860 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Algorithmized Polish grammar surface for CIELingo.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TokenAnalysis
- **funkcje:** `tokenize_polish`, `_sentence_part_for`, `analyze_tokens`, `_find_predicate`, `validate_valency`, `analyze_polish_sentence`, `as_dict`

## Opis
Algorithmized Polish grammar surface for CIELingo.

The goal is not a complete parser. It is a deterministic grammar-control layer:
parts of speech, sentence functions, case hints, valency roles, punctuation
operators and unresolved states instead of guessing.
