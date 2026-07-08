---
name: noema-systemd-target
priority: 1
description: >
  >
---
# Systemd Target

## Serwisy

| Serwis | Skrypt | Interwał |
|--------|--------|----------|
| `noema-kuramoto.service` | `ciel_noema_kuramoto_daemon.py` | 0.1s (10 Hz) |
| `noema-linux-sensor.service` | `ciel_noema_linux_sensor_daemon.py` | 1s |
| `noema-neutrino.service` | `ciel_noema_neutrino_daemon.py` | 1s |
| `noema-resonance-bridge.service` | `ciel_noema_resonance_bridge.py` | 1s |
| `noema-cielingo-sync.service` | `ciel_noema_cielingo_sync.py` | 60s |
| `noema-nonlocal-proxy.service` | `ciel_noema_nonlocal_proxy.py` | 5s |
| `noema-phasenav-hot.service` | `ciel_noema_phasenav_daemon.py --node hot` | 1s |
| `noema-analog-blend.service` | `noema_analog_phase_blend.py` | 1s |
| `noema-archiver.service` | `noema_phase_archiver.py` | 50 ticków |
| `noema-agent-backend.service` | `ciel_agent_backend.py` | HTTP :18520 |
| `noema-consolidator.service` | `ciel_memory_consolidator.py` | 300s |
| `noema-watchdog.service` | `noema_watchdog.py` | 6s |

## Template

```ini
[Unit]
Description=NOEMA <name>
After=noema.target
PartOf=noema.target

[Service]
ExecStart=/path/to/.venv/bin/python3 /path/to/scripts/<script>.py
Restart=on-failure
RestartSec=2
Environment=PYTHONPATH=/path/to/src

[Install]
WantedBy=noema.target
```

## Management

```bash
systemctl --user start noema.target      # start all
systemctl --user stop noema.target       # stop all
systemctl --user restart noema-<name>    # restart one
systemctl --user status noema-*          # check all
journalctl --user -u noema-<name> -f     # follow logs
```

## Lokacja

`~/.config/systemd/user/noema-*.service` + `noema.target`
