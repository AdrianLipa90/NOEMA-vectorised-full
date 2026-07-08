# _gcutils.py — .python_packages/scipy/_lib/_gcutils.py

## Tożsamość
- **id_karty:** `REPO-_GCUTILS-437D`
- **ścieżka:** `.python_packages/scipy/_lib/_gcutils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.227`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/_lib/_gcutils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.227 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Module for testing automatic garbage collection of objects

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ReferenceError
- **funkcje:** `set_gc_state`, `gc_state`, `assert_deallocated`

## Opis
Module for testing automatic garbage collection of objects

.. autosummary::
   :toctree: generated/

   set_gc_state - enable or disable garbage collection
   gc_state - context manager for given state of garbage collector
   assert_deallocated - context manager to check for circular references on object
