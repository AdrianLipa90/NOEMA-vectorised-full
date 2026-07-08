# cache.py — .python_packages/mypy/cache.py

## Tożsamość
- **id_karty:** `REPO-CACHE-B064`
- **ścieżka:** `.python_packages/mypy/cache.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.516`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/cache.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.516 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
This module contains high-level logic for fixed format serialization.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CacheMeta, CacheMetaEx
- **funkcje:** `read_literal`, `write_literal`, `read_int`, `write_int`, `read_str`, `write_str`, `read_bytes`, `write_bytes`, `read_int_opt`, `write_int_opt`, `read_str_opt`, `write_str_opt`, `read_int_list`, `write_int_list`, `read_str_list`, `write_str_list`, `read_bytes_list`, `write_bytes_list`, `read_str_opt_list`, `write_str_opt_list`, `read_json_value`, `write_json_value`, `read_json`, `write_json`, `write_errors`, `read_errors`, `serialize`, `deserialize`, `write`, `read`

## Opis
This module contains high-level logic for fixed format serialization.

Lower-level parts are implemented in C in mypyc/lib-rt/internal/librt_internal.c
Short summary of low-level functionality:
* integers are automatically serialized as 1, 2, or 4 bytes, or arbitrary length.
* str/bytes are serialized as size (1, 2, or 4 bytes) followed by bytes buffer.
* floats are serialized as C doubles.

At hi
