# linux_sensor.py — src/ciel_geometry/linux_sensor.py

## Tożsamość
- **id_karty:** `REPO-LINUX_SENSOR-2879`
- **ścieżka:** `src/ciel_geometry/linux_sensor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `3.727`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/linux_sensor.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 3.727 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
NOEMA Linux Sensor — mapuje system operacyjny na powierzchnię 3-6-9.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** LinuxSensorSnapshot, LinuxSensor
- **funkcje:** `_ensure_op_matrix`, `_stat_read`, `_read_cpu_phi`, `_read_mem_phi`, `_read_io_phi`, `_read_load_phi`, `_read_float`, `top_processes`, `_read_rss`, `snapshot`, `write_surface`, `process_phasenav`

## Opis
NOEMA Linux Sensor — mapuje system operacyjny na powierzchnię 3-6-9.

Sensor NIE zastępuje Kuramoto — zasila powierzchnię REALNYMI danymi
z /proc i /sys, na których Kuramoto wykonuje ewolucję.
