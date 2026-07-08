# __init__.py — .python_packages/fontTools/varLib/instancer/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-7E29`
- **ścieżka:** `.python_packages/fontTools/varLib/instancer/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.096`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/varLib/instancer/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.096 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Partially instantiate a variable font.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AxisTriple, NormalizedAxisTriple, NormalizedAxisTripleAndDistances, _BaseAxisLimits, AxisLimits, NormalizedAxisLimits, OverlapMode, _TupleVarStoreAdapter
- **funkcje:** `AxisRange`, `NormalizedAxisRange`, `instantiateVARC`, `instantiateTupleVariationStore`, `changeTupleVariationsAxisLimits`, `changeTupleVariationAxisLimit`, `instantiateCFF2`, `_instantiateGvarGlyph`, `instantiateGvarGlyph`, `instantiateGvar`, `setCvarDeltas`, `instantiateCvar`, `setMvarDeltas`, `verticalMetricsKeptInSync`, `instantiateMVAR`, `_remapVarIdxMap`, `_instantiateVHVAR`, `instantiateHVAR`, `instantiateVVAR`, `instantiateItemVariationStore`, `instantiateOTL`, `_isValidAvarSegmentMap`, `downgradeCFF2ToCFF`, `instantiateAvar`, `isInstanceWithinAxisRanges`, `instantiateFvar`, `instantiateSTAT`, `axisValuesFromAxisLimits`, `setMacOverlapFlags`, `normalize`

## Opis
Partially instantiate a variable font.

The module exports an `instantiateVariableFont` function and CLI that allow to
create full instances (i.e. static fonts) from variable fonts, as well as "partial"
variable fonts that only contain a subset of the original variation space.

For example, if you wish to pin the width axis to a given location while also
restricting the weight axis to 400..700 ran
