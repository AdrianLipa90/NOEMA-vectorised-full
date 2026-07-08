# __init__.py — .python_packages/pathspec/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-6824`
- **ścieżka:** `.python_packages/pathspec/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.062`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/pathspec/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.062 |
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
The *pathspec* package provides pattern matching for file paths. So far this

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
The *pathspec* package provides pattern matching for file paths. So far this
only includes Git's *gitignore* patterns.

The following classes are imported and made available from the root of the
`pathspec` package:

-       :class:`pathspec.gitignore.GitIgnoreSpec`

-       :class:`pathspec.pathspec.PathSpec`

-       :class:`pathspec.pattern.Pattern`

-       :class:`pathspec.pattern.RegexPattern
