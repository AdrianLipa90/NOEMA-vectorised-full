# noema_registry.py — src/ciel_geometry/noema_registry.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_REGISTRY-72C4`
- **ścieżka:** `src/ciel_geometry/noema_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `2.578`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/noema_registry.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 2.578 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
NOEMA Registry — token-based daemon registration for /dev/shm/ciel_noema.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** NoemaRegistry
- **funkcje:** `_ciel_binding_check`, `register`, `heartbeat`, `unregister`, `list_active`, `check_access`, `cleanup`, `get`, `_path`, `_write`, `_read`

## Opis
NOEMA Registry — token-based daemon registration for /dev/shm/ciel_noema.

Usage:
    from ciel_geometry.noema_registry import registry
    token = registry.register("kuramoto")
    registry.heartbeat(token)
    registry.unregister(token)
    active = registry.list_active(timeout=30)
    ok = registry.check_access(token, "phi")
