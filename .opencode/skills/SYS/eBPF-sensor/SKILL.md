---
name: eBPF-sensor
priority: 1
description: >
  >
---
# eBPF Sensor

## Metrics

| Metryka | Źródło | Flavor |
|---------|--------|--------|
| I/O pressure | openat rate (proc stat) | flavor[2] |
| CPU rates | user/nice/sys/iowait/irq | omega modulation |
| Memory | MemAvailable/MemTotal | flavor[1] (linux-sensor) |

## Snapshot

```python
sensor = EBPFSensor()
snap = sensor.snapshot()  # rates + flavors + omega
sensor.write_surface(surface, snap)
```

## Plik

`src/ciel_geometry/ebpf_noema_loader.py`
