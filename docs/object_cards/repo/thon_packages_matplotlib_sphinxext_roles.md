# roles.py — .python_packages/matplotlib/sphinxext/roles.py

## Tożsamość
- **id_karty:** `REPO-ROLES-AB50`
- **ścieżka:** `.python_packages/matplotlib/sphinxext/roles.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.684`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/sphinxext/roles.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.684 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Custom roles for the Matplotlib documentation.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _QueryReference
- **funkcje:** `_visit_query_reference_node`, `_depart_query_reference_node`, `_rcparam_role`, `_mpltype_role`, `setup`, `to_query_string`

## Opis
Custom roles for the Matplotlib documentation.

.. warning::

    These roles are considered semi-public. They are only intended to be used in
    the Matplotlib documentation.

However, it can happen that downstream packages end up pulling these roles into
their documentation, which will result in documentation build errors. The following
describes the exact mechanism and how to fix the errors.
