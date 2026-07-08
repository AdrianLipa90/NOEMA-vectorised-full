# memoryutils.py — .python_packages/numba/misc/memoryutils.py

## Tożsamość
- **id_karty:** `REPO-MEMORYUTILS-AD66`
- **ścieżka:** `.python_packages/numba/misc/memoryutils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.124`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/misc/memoryutils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.124 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Memory monitoring utilities for measuring memory usage.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MemoryTracker
- **funkcje:** `get_available_memory`, `get_memory_usage`, `monitor`, `get_summary`, `format_bytes`

## Opis
Memory monitoring utilities for measuring memory usage.

Example usage:
    tracker = MemoryTracker("my_function")
    with tracker.monitor():
        my_function()
    # Access data: tracker.rss_delta, tracker.duration, etc.
    # Get formatted string: tracker.get_summary()
