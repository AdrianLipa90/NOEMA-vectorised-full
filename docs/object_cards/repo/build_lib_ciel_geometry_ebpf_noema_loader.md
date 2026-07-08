# ebpf_noema_loader.py — build/lib/ciel_geometry/ebpf_noema_loader.py

## Tożsamość
- **id_karty:** `REPO-EBPF_NOEMA_LOADER-F28C`
- **ścieżka:** `build/lib/ciel_geometry/ebpf_noema_loader.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.367`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/ebpf_noema_loader.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.367 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
eBPF → NOEMA bridge: ładuje eBPF program, mapuje perf counters na 24φ.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** EBPFSensor
- **funkcje:** `main_loop`, `start`, `stop`, `read_counters`, `_rates`, `snapshot`, `write_surface`, `_read_mem_fallback`, `_mem_pressure`, `_handler`

## Opis
eBPF → NOEMA bridge: ładuje eBPF program, mapuje perf counters na 24φ.

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
