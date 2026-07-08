# typestate.py — .python_packages/mypy/typestate.py

## Tożsamość
- **id_karty:** `REPO-TYPESTATE-F1D1`
- **ścieżka:** `.python_packages/mypy/typestate.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.579`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/typestate.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.579 |
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
A shared state for all TypeInfos that holds global cache and dependency information,

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypeState
- **funkcje:** `reset_global_state`, `is_assumed_subtype`, `is_assumed_proper_subtype`, `get_assumptions`, `reset_all_subtype_caches`, `reset_subtype_caches_for`, `reset_all_subtype_caches_for`, `is_cached_subtype_check`, `is_cached_negative_subtype_check`, `record_subtype_cache_entry`, `record_negative_subtype_cache_entry`, `reset_protocol_deps`, `record_protocol_subtype_check`, `_snapshot_protocol_deps`, `update_protocol_deps`, `add_all_protocol_deps`

## Opis
A shared state for all TypeInfos that holds global cache and dependency information,
and potentially other mutable TypeInfo state. This module contains mutable global state.
