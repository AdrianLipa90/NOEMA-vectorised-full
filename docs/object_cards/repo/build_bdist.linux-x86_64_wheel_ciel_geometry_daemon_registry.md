# daemon_registry.py — build/bdist.linux-x86_64/wheel/ciel_geometry/daemon_registry.py

## Tożsamość
- **id_karty:** `REPO-DAEMON_REGISTRY-8563`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/daemon_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.925`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/daemon_registry.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.925 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Daemon registry — shared mmap heartbeat for all NOEMA daemons.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DaemonInfo, Registry
- **funkcje:** `_ensure_registry`, `daemon_main_loop`, `register`, `heartbeat`, `unregister`, `set_status`, `scan`, `_stop`

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
