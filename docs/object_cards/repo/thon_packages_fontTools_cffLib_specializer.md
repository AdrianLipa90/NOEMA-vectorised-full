# specializer.py — .python_packages/fontTools/cffLib/specializer.py

## Tożsamość
- **id_karty:** `REPO-SPECIALIZER-3F45`
- **ścieżka:** `.python_packages/fontTools/cffLib/specializer.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.370`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/cffLib/specializer.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.370 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
T2CharString operator specializer and generalizer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _GeneralizerDecombinerCommandsMap
- **funkcje:** `stringToProgram`, `programToString`, `programToCommands`, `_flattenBlendArgs`, `commandsToProgram`, `_everyN`, `_convertBlendOpToArgs`, `generalizeCommands`, `generalizeProgram`, `_categorizeVector`, `_mergeCategories`, `_negateCategory`, `_convertToBlendCmds`, `_addArgs`, `_argsStackUse`, `specializeCommands`, `specializeProgram`, `rmoveto`, `hmoveto`, `vmoveto`, `rlineto`, `hlineto`, `vlineto`, `rrcurveto`, `hhcurveto`, `vvcurveto`, `hvcurveto`, `vhcurveto`, `rcurveline`, `rlinecurve`

## Opis
T2CharString operator specializer and generalizer.

PostScript glyph drawing operations can be expressed in multiple different
ways. For example, as well as the ``lineto`` operator, there is also a
``hlineto`` operator which draws a horizontal line, removing the need to
specify a ``dx`` coordinate, and a ``vlineto`` operator which draws a
vertical line, removing the need to specify a ``dy`` coordi
