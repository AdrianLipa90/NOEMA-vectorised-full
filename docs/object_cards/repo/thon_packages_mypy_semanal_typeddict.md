# semanal_typeddict.py — .python_packages/mypy/semanal_typeddict.py

## Tożsamość
- **id_karty:** `REPO-SEMANAL_TYPEDDICT-2CDD`
- **ścieżka:** `.python_packages/mypy/semanal_typeddict.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.654`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/semanal_typeddict.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.654 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Semantic analysis of TypedDict definitions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypedDictAnalyzer
- **funkcje:** `analyze_typeddict_classdef`, `add_keys_and_types_from_base`, `_parse_typeddict_base`, `analyze_base_args`, `map_items_to_base`, `analyze_typeddict_classdef_fields`, `extract_meta_info`, `check_typeddict`, `parse_typeddict_args`, `parse_typeddict_fields_with_types`, `fail_typeddict_arg`, `build_typeddict_typeinfo`, `is_typeddict`, `fail`, `note`

## Opis
Semantic analysis of TypedDict definitions.
