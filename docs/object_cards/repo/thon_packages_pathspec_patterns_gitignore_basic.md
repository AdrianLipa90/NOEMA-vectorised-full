# basic.py — .python_packages/pathspec/patterns/gitignore/basic.py

## Tożsamość
- **id_karty:** `REPO-BASIC-7E5D`
- **ścieżka:** `.python_packages/pathspec/patterns/gitignore/basic.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.738`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/pathspec/patterns/gitignore/basic.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.738 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
This module provides :class:`GitIgnoreBasicPattern` which implements Git's

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GitIgnoreBasicPattern
- **funkcje:** `pattern_to_regex`

## Opis
This module provides :class:`GitIgnoreBasicPattern` which implements Git's
`gitignore`_ patterns as documented. This differs from how Git actually behaves
when including files in excluded directories.

.. _`gitignore`: https://git-scm.com/docs/gitignore
