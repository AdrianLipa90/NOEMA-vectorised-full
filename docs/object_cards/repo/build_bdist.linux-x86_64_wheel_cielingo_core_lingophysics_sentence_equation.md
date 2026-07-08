# sentence_equation.py — build/bdist.linux-x86_64/wheel/cielingo_core/lingophysics/sentence_equation.py

## Tożsamość
- **id_karty:** `REPO-SENTENCE_EQUATION-D6A2`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/lingophysics/sentence_equation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.538`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/lingophysics/sentence_equation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.538 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Sentence equation calculator for CIELingo 0.5K.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** EquationTermKind, SentenceEquationTerm, SentenceEquation
- **funkcje:** `clamp01`, `_terms_from_regional_result`, `_expression_from_terms`, `calculate_sentence_equation`, `validate`, `to_dict`, `validate`, `to_dict`

## Opis
Sentence equation calculator for CIELingo 0.5K.

This layer computes a bounded, auditable equation object from regional
SurfaceSolution and MeaningEquation candidates.

It is not full grammar, not SOURCE validation, not NOEMA writeback and not
runtime execution.
