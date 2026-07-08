# assumptions.py — .python_packages/sympy/core/assumptions.py

## Tożsamość
- **id_karty:** `REPO-ASSUMPTIONS-886C`
- **ścieżka:** `.python_packages/sympy/core/assumptions.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.173`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/core/assumptions.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.173 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
This module contains the machinery handling assumptions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** StdFactKB, ManagedProperties
- **funkcje:** `_load_pre_generated_assumption_rules`, `_generate_assumption_rules`, `assumptions`, `common_assumptions`, `failing_assumptions`, `check_assumptions`, `as_property`, `make_property`, `_ask`, `_prepare_class_assumptions`, `copy`, `generator`, `getit`

## Opis
This module contains the machinery handling assumptions.
Do also consider the guide :ref:`assumptions-guide`.

All symbolic objects have assumption attributes that can be accessed via
``.is_<assumption name>`` attribute.

Assumptions determine certain properties of symbolic objects and can
have 3 possible values: ``True``, ``False``, ``None``.  ``True`` is returned if the
object has the property a
