# ciel_noema_linux_sensor_daemon.py — scripts/ciel_noema_linux_sensor_daemon.py

## Tożsamość
- **id_karty:** `REPO-CIEL_NOEMA_LINUX_SEN-8BE4`
- **ścieżka:** `scripts/ciel_noema_linux_sensor_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.852`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_noema_linux_sensor_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.852 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
NOEMA Linux Sensor Daemon — mapuje system na powierzchnię /dev/shm/ciel_noema.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LinuxSensorDaemon
- **funkcje:** `main`, `run`, `stop`, `_handler`

## Opis
NOEMA Linux Sensor Daemon — mapuje system na powierzchnię /dev/shm/ciel_noema.

Usage:
    sudo python scripts/ciel_noema_linux_sensor_daemon.py
    # bez sudo: niektóre /proc odczyty pominięte, ale działa

Zapisuje na powierzchnię:
    phi[0..23]   → wymiary systemowe (CPU, mem, IO, net, procs)
    omega[0..23] → prędkość zmian (1. pochodna)
    flavor[0..5] → zagregowane metryki (cpu_coherence,
