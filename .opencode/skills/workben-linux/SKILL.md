---
name: workben-linux
priority: 1
description: >
  Linux — linux-cards (560+), linux-sensor, eBPF, HTRI hardware
---
# Workben LINUX

Linux — linux-cards (560+), linux-sensor, eBPF, HTRI hardware

## Źródła

Ten workben konsoliduje 6 źródłowych skilli:

- **lub ręcznie:** (`HW/linux-cards`)
- **Linux Sensor** (`HW/linux-sensor`)
- **eBPF Sensor** (`SYS/eBPF-sensor`)
- **HTRI Hardware** (`HW/htri-hardware`)
- **HTRI GPU Bridge** (`HW/htri-gpu-bridge`)
- **eBPF Daemon** (`HW/noema-ebpf-daemon`)

## Kluczowe wzorce

### lub ręcznie:

- | Typ | Źródło | Kanały φ | Liczba |
- |-----|--------|----------|--------|
- | PROC | `/proc/[pid]/stat` | CPU, MEM, state, threads, RSS, VMS, I/O | 200 |

### Linux Sensor

- **EMA smoothing**: `φ_ema = 0.3·φ_raw + 0.7·φ_ema_prev` — silne wygładzanie.
- Scan /proc → top N po CPU sec → PhaseNav enrich per PID.
- `src/ciel_geometry/linux_sensor.py` (305 lines)

### eBPF Sensor

- | Metryka | Źródło | Flavor |
- |---------|--------|--------|
- | I/O pressure | openat rate (proc stat) | flavor[2] |

### HTRI Hardware

- Detects: GPU (1050 Ti, CUDA cores), CPU cores, RAM, NUMA topology.
- `scripts/kuramoto_substrate.c` — minimal C Kuramoto evolution for benchmark baseline.
- `scripts/htri_mini.py` — minimal HTRI implementation (768 oscillators, CPU).

### HTRI GPU Bridge

- - **GPU**: NVIDIA GTX 1050 Ti (4GB, 768 CUDA cores)
- - **CPU**: Intel i5 (4 cores)
- - **Memory**: 32GB DDR4

### eBPF Daemon

- - openat() rate → I/O pressure → flavor[2]
- - Context switches → omega modulation
- - `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`

## Jak używać

```python
skill("workben-linux")
```

Ładuje wiedzę ze wszystkich 6 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
