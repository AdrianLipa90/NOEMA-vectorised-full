# spec.py — .python_packages/pathspec/patterns/gitignore/spec.py

## Tożsamość
- **id_karty:** `REPO-SPEC-B602`
- **ścieżka:** `.python_packages/pathspec/patterns/gitignore/spec.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.956`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/pathspec/patterns/gitignore/spec.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.956 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
This module provides :class:`GitIgnoreSpecPattern` which implements Git's

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GitIgnoreSpecPattern
- **funkcje:** `pattern_to_regex`

## Opis
This module provides :class:`GitIgnoreSpecPattern` which implements Git's
`gitignore`_ patterns, and handles edge-cases where Git's behavior differs from
what's documented. Git allows including files from excluded directories which
appears to contradict the documentation. Git discards patterns with invalid
range notation. This is used by :class:`~pathspec.gitignore.GitIgnoreSpec` to
fully replicat
