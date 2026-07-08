# grammar_algorithms.py — src/cielingo/polish/grammar_algorithms.py

## Tożsamość
- **id_karty:** `REPO-GRAMMAR_ALGORITHMS-122D`
- **ścieżka:** `src/cielingo/polish/grammar_algorithms.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.211`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/polish/grammar_algorithms.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.211 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


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
