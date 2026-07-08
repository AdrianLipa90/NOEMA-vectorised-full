# util.py — .python_packages/pathspec/util.py

## Tożsamość
- **id_karty:** `REPO-UTIL-265B`
- **ścieżka:** `.python_packages/pathspec/util.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.654`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/pathspec/util.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.654 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
This module provides utility methods for dealing with path-specs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AlreadyRegisteredError, RecursionError, CheckResult, MatchDetail, TreeEntry
- **funkcje:** `append_dir_sep`, `check_match_file`, `detailed_match_files`, `_filter_check_patterns`, `_is_iterable`, `iter_tree`, `iter_tree_entries`, `_iter_tree_entries_next`, `iter_tree_files`, `_iter_tree_files_next`, `lookup_pattern`, `match_file`, `match_files`, `normalize_file`, `normalize_files`, `register_pattern`, `message`, `name`, `pattern_factory`, `first_path`, `message`, `real_path`, `second_path`, `is_dir`, `is_file`, `is_symlink`, `stat`

## Opis
This module provides utility methods for dealing with path-specs.
