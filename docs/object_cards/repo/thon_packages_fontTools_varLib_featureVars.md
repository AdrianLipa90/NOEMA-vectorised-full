# featureVars.py — .python_packages/fontTools/varLib/featureVars.py

## Tożsamość
- **id_karty:** `REPO-FEATUREVARS-BA76`
- **ścieżka:** `.python_packages/fontTools/varLib/featureVars.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.481`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/varLib/featureVars.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.481 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Module to build FeatureVariation tables:

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ShifterVisitor
- **funkcje:** `addFeatureVariations`, `_existingVariableFeatures`, `_checkSubstitutionGlyphsExist`, `overlayFeatureVariations`, `overlayBox`, `cleanupBox`, `addFeatureVariationsRaw`, `buildGSUB`, `makeSubstitutionsHashable`, `visit`, `visit`, `buildSubstitutionLookups`, `buildFeatureVariations`, `buildFeatureRecord`, `buildFeatureVariationRecord`, `buildFeatureTableSubstitutionRecord`, `buildConditionTable`, `findFeatureVariationRecord`, `sortFeatureList`, `remapFeatures`, `_remapLangSys`

## Opis
Module to build FeatureVariation tables:
https://docs.microsoft.com/en-us/typography/opentype/spec/chapter2#featurevariations-table

NOTE: The API is experimental and subject to change.
