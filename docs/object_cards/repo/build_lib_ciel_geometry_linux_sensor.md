# linux_sensor.py — build/lib/ciel_geometry/linux_sensor.py

## Tożsamość
- **id_karty:** `REPO-LINUX_SENSOR-BA49`
- **ścieżka:** `build/lib/ciel_geometry/linux_sensor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.686`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/linux_sensor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.686 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
NOEMA Linux Sensor — mapuje system operacyjny na powierzchnię 3-6-9.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LinuxSensorSnapshot, LinuxSensor
- **funkcje:** `_ensure_op_matrix`, `_stat_read`, `_read_cpu_phi`, `_read_mem_phi`, `_read_load_phi`, `_read_float`, `top_processes`, `_read_rss`, `snapshot`, `write_surface`, `process_phasenav`

## Opis
NOEMA Linux Sensor — mapuje system operacyjny na powierzchnię 3-6-9.

Sensor NIE zastępuje Kuramoto — zasila powierzchnię REALNYMI danymi
z /proc i /sys, na których Kuramoto wykonuje ewolucję.
