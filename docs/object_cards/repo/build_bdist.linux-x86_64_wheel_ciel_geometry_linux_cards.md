# linux_cards.py — build/bdist.linux-x86_64/wheel/ciel_geometry/linux_cards.py

## Tożsamość
- **id_karty:** `REPO-LINUX_CARDS-D7D6`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/linux_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.116`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/linux_cards.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.116 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Linux → NOEMA karty — cały system operacyjny zmapowany jako karty PhaseNav.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LinuxCardIndex
- **funkcje:** `_card_id`, `_norm_phi`, `_proc_phi`, `_proc_card`, `_scan_cpu_cores`, `_cpu_phi`, `_scan_disks`, `_disk_phi`, `_scan_net_ifaces`, `_net_phi`, `_parse_net_proc`, `_scan_net_conns`, `_netconn_phi`, `_scan_modules`, `_scan_mounts`, `_scan_pci_devices`, `_scan_sensors`, `_parse_sensor_entry`, `_sensor_phi`, `_scan_net_flows`, `_netflow_phi`, `_scan_services`, `_service_phi`, `_make_card`, `_sysctl`, `_norm`, `update`, `_scan_procs`, `_scan_procfs`, `_rebuild_index`

## Opis
Linux → NOEMA karty — cały system operacyjny zmapowany jako karty PhaseNav.

Każdy proces, rdzeń CPU, dysk, interfejs sieciowy, połączenie, moduł,
punkt montowania, urządzenie PCI → 36D wektor fazowy → karta NOEMA.
Integracja z PhaseNav hot/cold: eksploracja całego systemu jak kart konceptów.

Typy kart:
    PROC     — procesy (/proc/[pid]/stat)
    CPU      — rdzenie CPU (/proc/stat cpu0..cpuN)
