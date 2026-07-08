# noema_registry.py — build/lib/ciel_geometry/noema_registry.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_REGISTRY-BB9D`
- **ścieżka:** `build/lib/ciel_geometry/noema_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.879`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/noema_registry.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.879 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
NOEMA Registry — token-based daemon registration for /dev/shm/ciel_noema.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NoemaRegistry
- **funkcje:** `register`, `heartbeat`, `unregister`, `list_active`, `check_access`, `cleanup`, `get`, `_path`, `_write`, `_read`

## Opis
NOEMA Registry — token-based daemon registration for /dev/shm/ciel_noema.

Usage:
    from ciel_geometry.noema_registry import registry
    token = registry.register("kuramoto")
    registry.heartbeat(token)
    registry.unregister(token)
    active = registry.list_active(timeout=30)
    ok = registry.check_access(token, "phi")
