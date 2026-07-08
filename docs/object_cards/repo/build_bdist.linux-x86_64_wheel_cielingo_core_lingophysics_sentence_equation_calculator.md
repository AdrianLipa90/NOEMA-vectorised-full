# sentence_equation_calculator.py — build/bdist.linux-x86_64/wheel/cielingo_core/lingophysics/sentence_equation_calculator.py

## Tożsamość
- **id_karty:** `REPO-SENTENCE_EQUATION_CA-67DC`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/lingophysics/sentence_equation_calculator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.489`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/lingophysics/sentence_equation_calculator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.489 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


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
