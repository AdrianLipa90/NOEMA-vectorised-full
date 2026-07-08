# noema_registry.py — build/bdist.linux-x86_64/wheel/ciel_geometry/noema_registry.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_REGISTRY-F88F`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.255`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_registry.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.255 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


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
