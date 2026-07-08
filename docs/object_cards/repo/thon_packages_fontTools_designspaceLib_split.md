# split.py — .python_packages/fontTools/designspaceLib/split.py

## Tożsamość
- **id_karty:** `REPO-SPLIT-F5B1`
- **ścieżka:** `.python_packages/fontTools/designspaceLib/split.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.470`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/designspaceLib/split.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.470 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Allows building all the variable fonts of a DesignSpace version 5 by

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `defaultMakeInstanceFilename`, `splitInterpolable`, `splitVariableFonts`, `convert5to4`, `_extractSubSpace`, `_conditionSetFrom`, `_subsetRulesBasedOnConditions`, `_filterLocation`, `maybeExpandDesignLocation`

## Opis
Allows building all the variable fonts of a DesignSpace version 5 by
splitting the document into interpolable sub-space, then into each VF.
