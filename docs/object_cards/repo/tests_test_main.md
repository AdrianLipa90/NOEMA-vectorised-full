# test_main.py — tests/test_main.py

## Tożsamość
- **id_karty:** `REPO-TEST_MAIN-3E51`
- **ścieżka:** `tests/test_main.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `5.054`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_main.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 5.054 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Tests for the ``python -m ciel_sot_agent`` entry point (__main__.py).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_run`, `test_main_no_args_shows_help`, `test_main_help_flag`, `test_main_unknown_command`, `test_main_lists_all_commands`

## Opis
Tests for the ``python -m ciel_sot_agent`` entry point (__main__.py).
