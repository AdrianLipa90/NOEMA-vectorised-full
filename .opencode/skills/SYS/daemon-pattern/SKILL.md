---
name: daemon-pattern
priority: 1
description: >
  >
---
# Daemon Pattern

## Registry — 16 slotów, mmap, /dev/shm/ciel_noema/daemon_registry

Dtype: 512B/slot = 8KB total
```
pid(int4), tick(int8), start_time(float8), last_heartbeat(float8),
status(str32), name(str48), cpu(float4), _pad(368B)
```

## Registry API (zrodlo)

```python
reg = Registry()
reg.register("name", tick=0, cpu=0.0)    # find free slot → int slot
reg.heartbeat(tick=42, cpu=0.0)           # update tick + timestamp
reg.set_status("running|paused|error")    # update status field
reg.unregister()                           # clear slot (pid=0, status="")
reg.scan(stale_seconds=6.0) → list[DaemonInfo]  # jesli heartbeat > 6s → alive=False
```

### DaemonInfo
```
DaemonInfo(slot, name, pid, tick, uptime, last_heartbeat, status, cpu, alive)
```

## daemon_main_loop() — gotowiec

```python
from ciel_geometry.daemon_registry import daemon_main_loop

def tick_fn(): return surface["tick"][0]
def on_tick(tick): evolve_surface(surface)

daemon_main_loop("my-daemon", tick_fn, interval=0.2, on_tick=on_tick)
```

Automatyka: register → co interval heartbeat + opcjonalnie cpu (psutil, co 5s) → unregister na SIGTERM/SIGINT.

## Konwencja daemonów

| Daemon | Interwał | Używa Registry | Uwagi |
|--------|----------|----------------|-------|
| kuramoto | 0.1s (10Hz) | tak | evolve_surface, agent_attractor |
| linux-sensor | 1s (1Hz) | tak | map /proc → flavor+phi |
| neutrino | 1s (1Hz) | tak | PMNS → D_f→Λ→g_boost |
| resonance-bridge | 1s | tak | dual_surface_step+agent log |
| cielingo-sync | 60s | tak | closure+W_ij blend+orchestrator |
| phasenav-hot | 1s | tak | analog bus: phi_hot |
| phasenav-cold | 30s | tak | analog bus: phi_cold |
| analog-blend | 1s | tak | blend hot+cold → surface phi |
| nonlocal-proxy | 5s (idle stretch) | tak | channel broadcast |
| sonic | 10s | nie | diagnostyka, bez registry |
| archiver | 50 ticków | tak | HDF5 surface snapshots |
| consolidator | 60s | tak | MemoryLog → state_db.m8_audit |

## Registry context manager

```python
with Registry() as reg:
    reg.register("my-daemon")
    # automatyczny unregister() przy wyjsciu
```

## Systemd

Plik: `.config/systemd/user/noema-<name>.service`

```ini
[Unit]
Description=NOEMA <name>
After=noema.target
PartOf=noema.target

[Service]
ExecStart=/home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/.venv/bin/python3 /home/adrian/Pulpit/CIEL_PROJECT_CANON/NOEMA/scripts/noema_<name>.py
Restart=on-failure
RestartSec=2
Type=simple

[Install]
WantedBy=noema.target
```

## Signal handling

Daemon musi handlerowac SIGTERM/SIGINT dla graceful shutdown (unregister).
Standard: signal.signal(signal.SIGTERM, _stop); signal.signal(signal.SIGINT, _stop)
Obsluga wewnatrz daemon_main_loop() — wbudowana.
