# filenames.py — .python_packages/fontTools/misc/filenames.py

## Tożsamość
- **id_karty:** `REPO-FILENAMES-6BDA`
- **ścieżka:** `.python_packages/fontTools/misc/filenames.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.930`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/misc/filenames.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.930 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
This module implements the algorithm for converting between a "user name" -

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NameTranslationError
- **funkcje:** `userNameToFileName`, `handleClash1`, `handleClash2`

## Opis
This module implements the algorithm for converting between a "user name" -
something that a user can choose arbitrarily inside a font editor - and a file
name suitable for use in a wide range of operating systems and filesystems.

The `UFO 3 specification <http://unifiedfontobject.org/versions/ufo3/conventions/>`_
provides an example of an algorithm for such conversion, which avoids illegal
chara
