# linux_cards.py — src/ciel_geometry/linux_cards.py

## Tożsamość
- **id_karty:** `REPO-LINUX_CARDS-7F93`
- **ścieżka:** `src/ciel_geometry/linux_cards.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `5.488`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/linux_cards.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 5.488 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
Linux → NOEMA karty — cały system operacyjny zmapowany jako karty PhaseNav.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

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
