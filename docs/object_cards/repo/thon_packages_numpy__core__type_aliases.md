# _type_aliases.py — .python_packages/numpy/_core/_type_aliases.py

## Tożsamość
- **id_karty:** `REPO-_TYPE_ALIASES-6114`
- **ścieżka:** `.python_packages/numpy/_core/_type_aliases.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.214`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/_core/_type_aliases.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.214 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
Due to compatibility, numpy has a very large number of different naming

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
Due to compatibility, numpy has a very large number of different naming
conventions for the scalar types (those subclassing from `numpy.generic`).
This file produces a convoluted set of dictionaries mapping names to types,
and sometimes other mappings too.

.. data:: allTypes
    A dictionary of names to types that will be exposed as attributes through
    ``np._core.numerictypes.*``

.. data:: sc
