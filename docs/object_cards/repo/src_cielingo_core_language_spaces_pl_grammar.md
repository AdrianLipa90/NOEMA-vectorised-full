# grammar.py — src/cielingo_core/language_spaces/pl/grammar.py

## Tożsamość
- **id_karty:** `REPO-GRAMMAR-6BAA`
- **ścieżka:** `src/cielingo_core/language_spaces/pl/grammar.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.596`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/language_spaces/pl/grammar.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.596 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Minimal Polish grammar heuristics for CIELingo 0.5I.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PolishGrammarHint
- **funkcje:** `_norm`, `infer_case_hints`, `analyze_polish_tokens`, `to_dict`

## Opis
Minimal Polish grammar heuristics for CIELingo 0.5I.

This is not a full Polish morphology engine. It is a cautious local layer for:
- negation scope,
- imperative/action force,
- source phrases,
- rough case hints,
- local role hints.

It emits regional hints and residue; GLOBAL remains responsible for operator/action/scar logic.
