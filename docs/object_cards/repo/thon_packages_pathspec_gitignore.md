# gitignore.py — .python_packages/pathspec/gitignore.py

## Tożsamość
- **id_karty:** `REPO-GITIGNORE-B106`
- **ścieżka:** `.python_packages/pathspec/gitignore.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.578`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/pathspec/gitignore.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.578 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
This module provides :class:`.GitIgnoreSpec` which replicates *.gitignore*

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GitIgnoreSpec
- **funkcje:** `from_lines`, `from_lines`, `from_lines`, `_make_backend`

## Opis
This module provides :class:`.GitIgnoreSpec` which replicates *.gitignore*
behavior, and handles edge-cases where Git's behavior differs from what's
documented. Git allows including files from excluded directories which directly
contradicts the documentation. This uses :class:`.GitIgnoreSpecPattern` to fully
replicate Git's handling.
