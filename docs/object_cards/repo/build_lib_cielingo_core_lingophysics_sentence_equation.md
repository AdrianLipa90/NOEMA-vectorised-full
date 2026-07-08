# sentence_equation.py — build/lib/cielingo_core/lingophysics/sentence_equation.py

## Tożsamość
- **id_karty:** `REPO-SENTENCE_EQUATION-FAFB`
- **ścieżka:** `build/lib/cielingo_core/lingophysics/sentence_equation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.572`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/lingophysics/sentence_equation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.572 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


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
