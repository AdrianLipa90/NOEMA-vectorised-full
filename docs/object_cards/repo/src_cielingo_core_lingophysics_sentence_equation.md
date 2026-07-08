# sentence_equation.py — src/cielingo_core/lingophysics/sentence_equation.py

## Tożsamość
- **id_karty:** `REPO-SENTENCE_EQUATION-480D`
- **ścieżka:** `src/cielingo_core/lingophysics/sentence_equation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.628`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/lingophysics/sentence_equation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.628 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


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
