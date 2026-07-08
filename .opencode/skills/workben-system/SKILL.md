---
name: workben-system
priority: 1
description: >
  NOEMA core — surface mmap, daemony, registry, euler, synchronizacja, systemd, config, teleusing
---
# Workben SYSTEM

NOEMA core — surface mmap, daemony, registry, euler, synchronizacja, systemd, config, teleusing

## Źródła

Ten workben konsoliduje 16 źródłowych skilli:

- **Surface Mmap Protocol** (`SYS/surface-mmap-protocol`)
- **Daemon Pattern** (`SYS/daemon-pattern`)
- **NOEMA System Architecture** (`SYS/noema-system`)
- **Systemd Target** (`SYS/noema-systemd-target`)
- **CIELingo Sync Daemon** (`SYS/synchronize`)
- **Unified Config** (`SYS/noema-unified-config`)
- **noema_daemon — Unified Daemon** (`SYS/noema-daemon-hook`)
- **Inject Coupling** (`SYS/noema-inject-coupling`)
- **Settings Sync** (`SYS/noema-settings-sync`)
- **Subconscious** (`SYS/subconscious`)
- **CIEL Canon CLI** (`SYS/noema-canon`)
- **Teleusing** (`SYS/teleusing`)
- **Kuramoto Euler Sync** (`COMP/kuramoto-euler-sync`)
- **Euler Propagation** (`COMP/noema-euler-propagation`)
- **Kuramoto Substrate (C)** (`COMP/noema-kuramoto-substrate`)
- **Hybrid Runner** (`COMP/noema-hybrid-runner`)

## Kluczowe wzorce

### Surface Mmap Protocol

- | Plik | dtype | shape | bajty | Writer |
- |------|-------|-------|-------|--------|
- | `phi` | float64 | (36,) | 288 | Kuramoto daemon |

### Daemon Pattern

- Dtype: 512B/slot = 8KB total
- Automatyka: register → co interval heartbeat + opcjonalnie cpu (psutil, co 5s) → unregister na SIGTERM/SIGINT.
- | Daemon | Interwał | Używa Registry | Uwagi |

### NOEMA System Architecture

- | Warstwa | Opis | Komponenty |
- |---------|------|------------|
- | L0: Surface | 24 oscillator MMAP | `/dev/shm/ciel_noema/{phi,omega,g,flavor,tick,gravity}` |

### Systemd Target

- | Serwis | Skrypt | Interwał |
- |--------|--------|----------|
- | `noema-kuramoto.service` | `ciel_noema_kuramoto_daemon.py` | 0.1s (10 Hz) |

### CIELingo Sync Daemon

- `scripts/ciel_noema_cielingo_sync.py` (484 lines)

### Unified Config

- `noema_config.json` (w katalogu projektu)
- **Env override**: `export NOEMA_CONFIG=/path/to/config.json`
- - `noema_config.json` — w repo

### noema_daemon — Unified Daemon

- - `ciel_noema_kuramoto_daemon.py`
- - `ciel_noema_linux_sensor_daemon.py`
- - `noema_agent_lock.py`

### Inject Coupling

- `couplings_wij_optimized.json` — blend (2-12%) między base coupling a PMNS-boosted g.

### Settings Sync

- - `noema_config.json` (w repo)
- - `src/ciel_geometry/noema_config.py` (loader)
- - `.config/systemd/user/noema-*.service` (ExecStart args)

### Subconscious

- Równanie:
- Sygnał konsolidacji z:
- - memory aging (jak stara pamięć)

### CIEL Canon CLI

- `CIEL_CANON.py` (root projektowy)

### Teleusing

- | Plik | Zawartość | Klucz |
- |------|-----------|-------|
- | `*NAME_MASS.noema.jsonl` | Normalized names + geometric_phase_rad | normalized |

### Kuramoto Euler Sync

- | Parametr | Wartość |
- |----------|---------|
- | Daemon | `ciel_noema_kuramoto_daemon.py` |

### Euler Propagation

- | Skrypt | Funkcja |
- |--------|---------|
- | `propagate_holonomy.py` | Propagate Berry phase przez surface |

### Kuramoto Substrate (C)

- | Wersja | Język | Throughput |
- |--------|-------|-----------|
- | Python (numpy) | Python | 1× |

## Jak używać

```python
skill("workben-system")
```

Ładuje wiedzę ze wszystkich 16 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
