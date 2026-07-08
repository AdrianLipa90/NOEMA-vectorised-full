# test_euler_perturbation.py — scripts/test_euler_perturbation.py

## Tożsamość
- **id_karty:** `REPO-TEST_EULER_PERTURBAT-E267`
- **ścieżka:** `scripts/test_euler_perturbation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.573`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/test_euler_perturbation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.573 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Euler Constraint — Perturbation Recovery Test.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_make_memory`, `_make_core`, `_empty_eba`, `inject_antiphase`, `feedback_step`, `classify_response`, `wij_axis_distance`, `run_test`, `print_summary`, `_print_diagnostic_note`, `_print_diagnostic_note_stub`

## Opis
Euler Constraint — Perturbation Recovery Test.

Scenariusz:
  1. Baseline — rejestruj closure_score bez zaburzenia
  2. Perturbacja — wstrzyknij klaster anty-fazowy (przesunięcie o π) w wybranych sektorach
  3. Recovery — N kroków orbital feedback, mierz closure_score per krok
  4. Klasyfikacja — gładki powrót / oscylacje / quasi-atraktor / dryf

Użycie:
    python3 scripts/test_euler_perturbation
