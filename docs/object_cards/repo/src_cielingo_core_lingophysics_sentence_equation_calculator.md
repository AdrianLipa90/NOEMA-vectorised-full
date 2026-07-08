# sentence_equation_calculator.py — src/cielingo_core/lingophysics/sentence_equation_calculator.py

## Tożsamość
- **id_karty:** `REPO-SENTENCE_EQUATION_CA-9875`
- **ścieżka:** `src/cielingo_core/lingophysics/sentence_equation_calculator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.326`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/lingophysics/sentence_equation_calculator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.326 |
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
Deprecated thin router for sentence equations.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `solve_sentence_equation`

## Opis
Deprecated thin router for sentence equations.

Architecture rule:
- canonical regional paths live in language_spaces/{pl,en,ja}/sentence_equation.py
- this module is kept only for CLI/backward-compatible tests
- it must not contain grammar, solver logic, regional J logic, or mixed-language state
