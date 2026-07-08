# otTables.py — .python_packages/fontTools/ttLib/tables/otTables.py

## Tożsamość
- **id_karty:** `REPO-OTTABLES-8617`
- **ścieżka:** `.python_packages/fontTools/ttLib/tables/otTables.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.374`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/ttLib/tables/otTables.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.374 |
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
fontTools.ttLib.tables.otTables -- A collection of classes representing the various

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** VarComponentFlags, VarComponent, VarCompositeGlyph, AATStateTable, AATState, AATAction, RearrangementMorphAction, ContextualMorphAction, LigAction, LigatureMorphAction, InsertionMorphAction, FeatureParams, FeatureParamsSize, FeatureParamsStylisticSet, FeatureParamsCharacterVariants, Coverage, DeltaSetIndexMap, VarIdxMap, VarRegionList, SingleSubst
- **funkcje:** `_read_uint32var`, `_write_uint32var`, `fixLookupOverFlows`, `splitMultipleSubst`, `splitAlternateSubst`, `splitLigatureSubst`, `splitPairPos`, `splitMarkBasePos`, `fixSubTableOverFlows`, `_buildClasses`, `_getGlyphsFromCoverageTable`, `populateDefaults`, `decompile`, `compile`, `toXML`, `fromXML`, `applyTransformDeltas`, `decompile`, `compile`, `toXML`, `fromXML`, `compileActions`, `_writeFlagsToXML`, `_setFlag`, `compile`, `decompile`, `toXML`, `fromXML`, `compile`, `decompile`

## Opis
fontTools.ttLib.tables.otTables -- A collection of classes representing the various
OpenType subtables.

Most are constructed upon import from data in otData.py, all are populated with
converter objects from otConverters.py.
