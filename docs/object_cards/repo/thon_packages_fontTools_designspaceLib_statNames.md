# statNames.py — .python_packages/fontTools/designspaceLib/statNames.py

## Tożsamość
- **id_karty:** `REPO-STATNAMES-9E8F`
- **ścieżka:** `.python_packages/fontTools/designspaceLib/statNames.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.740`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/designspaceLib/statNames.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.740 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
Compute name information for a given location in user-space coordinates

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** StatNames
- **funkcje:** `getStatNames`, `_getSortedAxisLabels`, `_getAxisLabelsForUserLocation`, `_getRibbiStyle`

## Opis
Compute name information for a given location in user-space coordinates
using STAT data. This can be used to fill-in automatically the names of an
instance:

.. code:: python

    instance = doc.instances[0]
    names = getStatNames(doc, instance.getFullUserLocation(doc))
    print(names.styleNames)
