# noema_sonic_daemon.py — scripts/noema_sonic_daemon.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SONIC_DAEMON-9AA2`
- **ścieżka:** `scripts/noema_sonic_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.158`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_sonic_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.158 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
Sonic Screwdriver — probe the full NOEMA warp loop at a glance.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `read_surface_summary`, `_check_consolidator_status`, `_scan_daemons`, `sonic_report`, `main`

## Opis
Sonic Screwdriver — probe the full NOEMA warp loop at a glance.

Reads all surface channels and shows:
  - Kuramoto state (phi, omega, g)
  - Semantic gravity (density, γ, mass, unruh)
  - WARP_DRIFT / UNRUH_DRIVE activity
  - Operator chain current state

Usage:
    python scripts/noema_sonic_daemon.py [--watch] [--interval SEC]
