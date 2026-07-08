# voltToFea.py — .python_packages/fontTools/voltLib/voltToFea.py

## Tożsamość
- **id_karty:** `REPO-VOLTTOFEA-28BF`
- **ścieżka:** `.python_packages/fontTools/voltLib/voltToFea.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.481`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/voltLib/voltToFea.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.481 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
MS VOLT ``.vtp`` to AFDKO ``.fea`` OpenType Layout converter.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Lookup, VoltToFea
- **funkcje:** `_flatten_group`, `sort_groups`, `main`, `_lookupName`, `_className`, `_collectStatements`, `_buildFeatureFile`, `convert`, `_glyphName`, `_groupName`, `_glyphSet`, `_coverage`, `_context`, `_groupDefinition`, `_glyphDefinition`, `_scriptDefinition`, `_settingDefinition`, `_adjustment`, `_anchor`, `_anchorDefinition`, `_gposLookup`, `_gposContextLookup`, `_gsubLookup`, `_gsubContextLookup`, `_lookupDefinition`

## Opis
MS VOLT ``.vtp`` to AFDKO ``.fea`` OpenType Layout converter.

Usage
-----

To convert a VTP project file:


.. code-block:: sh

    $ fonttools voltLib.voltToFea input.vtp output.fea

It is also possible convert font files with `TSIV` table (as saved from Volt),
in this case the glyph names used in the Volt project will be mapped to the
actual glyph names in the font files when written to the fea
