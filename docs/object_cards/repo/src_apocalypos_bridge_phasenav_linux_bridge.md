# phasenav_linux_bridge.py — src/apocalypos/bridge/phasenav_linux_bridge.py

## Tożsamość
- **id_karty:** `REPO-PHASENAV_LINUX_BRIDG-57FE`
- **ścieżka:** `src/apocalypos/bridge/phasenav_linux_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.394`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/apocalypos/bridge/phasenav_linux_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.394 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
PhaseNav Linux Bridge — eBPF Kuramoto → NOEMA 36D sensor_raw + cgroup.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PhaseNavLinuxBridge
- **funkcje:** `main`, `write_sensor_raw`, `modulate_cgroup`, `run`

## Opis
PhaseNav Linux Bridge — eBPF Kuramoto → NOEMA 36D sensor_raw + cgroup.

Uruchamiany jako daemon (sudo):
    python3 phasenav_linux_bridge.py

Cykl (1 Hz):
    1. Czyta BPF mapy (per-PID phase)
    2. Oblicza global R, Ψ
    3. Zapisuje 36D sensor_raw (float64) na powierzchnię NOEMA
    4. Moduluje cgroup cpu.weight na podstawie R
