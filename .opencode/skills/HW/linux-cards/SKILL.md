---
name: linux-cards
priority: 1
description: >
  Cały system Linux zmapowany jako 24D karty PhaseNav. 11 typów: PROC (procesy),
  CPU (rdzenie), DISK (dyski), NET_IF (interfejsy sieciowe), NET_CONN (połączenia),
  NET_FLOW (procesy z aktywnością sieciową, nethogs-like), MODULE (moduły jądra),
  MOUNT (punkty montowania), PCI_DEV (urządzenia PCI),
  SENSOR (sensory sprzętowe: temperatura, wentylatory, napięcie, prąd, moc),
  SERVICE (usługi systemd).
  600+ kart, bridge do PhaseNav hot, zapis na surface linux_load.
---

## Linux → NOEMA Cards — integracja systemu operacyjnego

### Architektura

```
/proc/[pid]/stat        ─┐
/proc/stat cpuN         ─┤
/proc/diskstats         ─┤
/proc/net/dev           ─┤  LinuxCardIndex.update() → 8 typów × 24D faz → /dev/shm/ciel_noema/linux_cards/
/proc/net/tcp           ─┤
/proc/modules           ─┤
/proc/mounts + statvfs  ─┤
/sys/bus/pci/devices/   ─┐         │
/sys/class/hwmon/       ─┤         │
/proc/[pid]/fd→socket   ─┐         │
systemctl list-units     ─┘         │
                                    ▼
             ┌─────────────────────────────┐
             │  LinuxCardIndex             │
             │  501 cards, 24D phi per card│
             │  .by_type("CPU")            │
             │  .nearby(phi) → PhaseNav    │
             │  .top_cpu(10)               │
             └──────────┬──────────────────┘
                        │
         ┌──────────────┼──────────────────────┐
         ▼              ▼                      ▼
   surface mmap    PhaseNav hot          /dev/shm/ciel_noema/
   gravity[7]      analog/phi_hot       linux_cards/*.json
```

### 11 typów kart

| Typ | Źródło | Kanały φ | Liczba |
|-----|--------|----------|--------|
| PROC | `/proc/[pid]/stat` | CPU, MEM, state, threads, RSS, VMS, I/O | 200 |
| CPU | `/proc/stat cpu0..cpuN` | user/system/idle/iowait/irq/freq | ~12 |
| DISK | `/proc/diskstats` | reads/writes/sectors/IOPS/size | ~10 |
| NET_IF | `/proc/net/dev` | rx/tx bytes/packets/errors/speed | ~3 |
| NET_CONN | `/proc/net/{tcp,udp,tcp6,udp6}` | state/retrans/queue/port/drops/proto | ~59 |
| NET_FLOW | `/proc/[pid]/fd → socket inode` | active/total/listen/retrans/rxq/txq/drops/ports | ~3-20 |
| SERVICE | `systemctl list-units --type=service` | active/running/enabled/failed/user | ~80 |
| MODULE | `/proc/modules` | size/refcount/used_by | ~229 |
| MOUNT | `/proc/mounts` + statvfs | total/used/avail/inodes | ~9 |
| PCI_DEV | `/sys/bus/pci/devices/` | class/vendor/IRQ/NUMA | ~21 |
| SENSOR | `/sys/class/hwmon/` + `sensors -j` | temp/fan/power/current/voltage | ~17 |

### Pliki na /dev/shm/ciel_noema/linux_cards/

| Plik | Format | Opis |
|------|--------|------|
| `mean_phi` | binary (192B) | Średnia faza wszystkich kart |
| `cards.jsonl` | JSONL | Wszystkie karty (bez phi) |
| `top_cpu.json` | JSON | Top 10 procesów po CPU |
| `nearby_surface.json` | JSON | 10 kart najbliższych bieżącej fazie surface |
| `types.json` | JSON | Licznik kart per typ |
| `hardware.json` | JSON | Podsumowanie sprzętu |
| `cpu_summary.json` | JSON | Zagregowane metryki CPU |
| `count` | text | Liczba kart |
| `top_pids.txt` | text | Top 5 PID po CPU |

### Bridge do PhaseNav

Co cykl (5s):
1. Czyta bieżącą fazę surface (`/dev/shm/ciel_noema/phi`)
2. Szuka najbliższej karty przez cos similarity
3. Zapisuje fazę najbliższej karty do `analog/phi_hot` (PhaseNav hot widzi)
4. Zapisuje etykietę do `analog/hot_label`

### MCP tools

`linux_cards` — zwraca top CPU + summary wszystkich typów.

Do rozszerzenia: `linux_hardware` — per-type query, `linux_card <id>` — konkretna karta.

### Daemon

`scripts/noema_linux_cards_daemon.py` — systemd `noema-linux-cards.service`

```bash
systemctl --user start noema-linux-cards.service
# lub ręcznie:
.venv/bin/python3 scripts/noema_linux_cards_daemon.py
# raz:
.venv/bin/python3 scripts/noema_linux_cards_daemon.py --once
```

### Klasa Python

```python
from ciel_geometry.linux_cards import LinuxCardIndex
idx = LinuxCardIndex(max_procs=200)
n = idx.update()                              # skanowanie
idx.by_type("CPU")                            # 12 rdzeni
idx.by_type("DISK")                           # 10 dysków
idx.nearby(surface_phi, k=5)                  # PhaseNav
idx.query("Xorg")                             # szukaj po nazwie
idx.top_cpu(10)                               # procesy
idx.summary_stats()                           # statystyki
idx.save_surface()                            # zapisz na mmap
idx.card_file("LNX-PROC-firefox-ABC123")      # karta markdown
```

### Systemd

Unit: `.config/systemd/user/noema-linux-cards.service`
- Type: simple
- Restart: on-failure (5s)
- WantedBy: noema.target
