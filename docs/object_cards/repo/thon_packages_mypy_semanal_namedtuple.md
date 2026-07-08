# semanal_namedtuple.py — .python_packages/mypy/semanal_namedtuple.py

## Tożsamość
- **id_karty:** `REPO-SEMANAL_NAMEDTUPLE-7E8B`
- **ścieżka:** `.python_packages/mypy/semanal_namedtuple.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.580`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/semanal_namedtuple.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.580 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
Semantic analysis of named tuple definitions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NamedTupleAnalyzer
- **funkcje:** `analyze_namedtuple_classdef`, `check_namedtuple_classdef`, `check_namedtuple`, `store_namedtuple_info`, `parse_namedtuple_args`, `parse_namedtuple_fields_with_types`, `build_namedtuple_typeinfo`, `save_namedtuple_body`, `check_namedtuple_field_name`, `fail`, `add_field`, `add_method`, `make_init_arg`

## Opis
Semantic analysis of named tuple definitions.

This is conceptually part of mypy.semanal.
