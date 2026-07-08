# noema_linux_cards_daemon.py — scripts/noema_linux_cards_daemon.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_LINUX_CARDS_DA-2F85`
- **ścieżka:** `scripts/noema_linux_cards_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.899`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_linux_cards_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.899 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
Linux Cards Daemon — mapuje cały system Linux na karty NOEMA.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `log`, `read_surface_phi`, `write_gravity`, `write_cards_dir`, `_bridge_to_phasenav`, `cycle`, `signal_handler`, `main`

## Opis
Linux Cards Daemon — mapuje cały system Linux na karty NOEMA.

Co robi:
1. Skanuje /proc (przez psutil) + /sys dla:
   - PROC: wszystkie procesy (200)
   - CPU: każdy rdzeń CPU (z /proc/stat)
   - DISK: urządzenia blokowe (z /proc/diskstats)
   - NET_IF: interfejsy sieciowe (z /proc/net/dev)
    - NET_CONN: aktywne połączenia (z /proc/net/tcp)
    - NET_FLOW: procesy z aktywnością sieciową (nethog
