# types_utils.py — .python_packages/mypy/types_utils.py

## Tożsamość
- **id_karty:** `REPO-TYPES_UTILS-E1FD`
- **ścieżka:** `.python_packages/mypy/types_utils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.360`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/types_utils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.360 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
This module is for (more basic) type operations that should not depend on is_subtype(),

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `flatten_types`, `strip_type`, `is_invalid_recursive_alias`, `get_bad_type_type_item`, `is_union_with_any`, `is_generic_instance`, `is_overlapping_none`, `remove_optional`, `is_self_type_like`, `store_argument_type`

## Opis
This module is for (more basic) type operations that should not depend on is_subtype(),
meet_types(), join_types() etc. We don't want to keep them in mypy/types.py for two reasons:
* Reduce the size of that module.
* Reduce use of get_proper_type() in types.py to avoid cyclic imports
  expand_type <-> types, if we move get_proper_type() to the former.
