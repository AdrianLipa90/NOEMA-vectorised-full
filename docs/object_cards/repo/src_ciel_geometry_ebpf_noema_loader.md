# ebpf_noema_loader.py — src/ciel_geometry/ebpf_noema_loader.py

## Tożsamość
- **id_karty:** `REPO-EBPF_NOEMA_LOADER-7C28`
- **ścieżka:** `src/ciel_geometry/ebpf_noema_loader.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `0.962`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/ebpf_noema_loader.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 0.962 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
eBPF → NOEMA bridge: ładuje eBPF program, mapuje perf counters na 36φ.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** EBPFSensor
- **funkcje:** `main_loop`, `start`, `stop`, `read_counters`, `_rates`, `snapshot`, `write_surface`, `_read_mem_fallback`, `_mem_pressure`, `_handler`

## Opis
eBPF → NOEMA bridge: ładuje eBPF program, mapuje perf counters na 36φ.

Usage:
    sudo python3 -c "
    from ciel_geometry.ebpf_noema_loader import EBPFSensor
    sensor = EBPFSensor()
    sensor.start()
    while True:
        snap = sensor.read()
        print(snap)
        time.sleep(1)
    "
