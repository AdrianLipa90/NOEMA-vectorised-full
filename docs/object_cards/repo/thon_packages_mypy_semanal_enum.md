# semanal_enum.py — .python_packages/mypy/semanal_enum.py

## Tożsamość
- **id_karty:** `REPO-SEMANAL_ENUM-E9EC`
- **ścieżka:** `.python_packages/mypy/semanal_enum.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.606`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/semanal_enum.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.606 |
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
Semantic analysis of call-based Enum definitions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** EnumCallAnalyzer
- **funkcje:** `process_enum_call`, `check_enum_call`, `build_enum_call_typeinfo`, `parse_enum_call_args`, `fail_enum_call_arg`, `fail`

## Opis
Semantic analysis of call-based Enum definitions.

This is conceptually part of mypy.semanal (semantic analyzer pass 2).
