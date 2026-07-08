# agl.py — .python_packages/fontTools/agl.py

## Tożsamość
- **id_karty:** `REPO-AGL-EF51`
- **ścieżka:** `.python_packages/fontTools/agl.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.850`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/agl.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.850 |
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
Interface to the Adobe Glyph List

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AGLError
- **funkcje:** `_builddicts`, `toUnicode`, `_glyphComponentToUnicode`, `_zapfDingbatsToUnicode`, `_uniToUnicode`, `_uToUnicode`

## Opis
Interface to the Adobe Glyph List

This module exists to convert glyph names from the Adobe Glyph List
to their Unicode equivalents. Example usage:

        >>> from fontTools.agl import toUnicode
        >>> toUnicode("nahiragana")
        'な'

It also contains two dictionaries, ``UV2AGL`` and ``AGL2UV``, which map from
Unicode codepoints to AGL names and vice versa:

        >>> import fontTools
