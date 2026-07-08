# daemon_registry.py — src/ciel_geometry/daemon_registry.py

## Tożsamość
- **id_karty:** `REPO-DAEMON_REGISTRY-84C8`
- **ścieżka:** `src/ciel_geometry/daemon_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `3.040`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/daemon_registry.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 3.040 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
Daemon registry — shared mmap heartbeat for all NOEMA daemons.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** DaemonInfo, Registry
- **funkcje:** `_ciel_binding_check`, `_ensure_registry`, `daemon_main_loop`, `register`, `heartbeat`, `unregister`, `set_status`, `scan`, `_stop`

## Opis
Daemon registry — shared mmap heartbeat for all NOEMA daemons.

Each daemon writes: name, pid, tick, uptime, last_heartbeat, status, cpu
Registry is a fixed-size mmap at /dev/shm/ciel_noema/registry.

Usage:
    from ciel_geometry.daemon_registry import Registry

    reg = Registry()
    reg.register("kuramoto", tick=42)
    # ... in main loop:
    reg.heartbeat(tick=44)
    # check all daemons:
