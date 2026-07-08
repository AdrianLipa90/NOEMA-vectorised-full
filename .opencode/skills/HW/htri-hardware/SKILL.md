---
name: htri-hardware
priority: 2
description: >
  >
---
# HTRI Hardware

## Probe

```bash
python3 scripts/htri_host_probe.py
```

Detects: GPU (1050 Ti, CUDA cores), CPU cores, RAM, NUMA topology.

## Benchmarks

```bash
python3 scripts/htri_bench.py
python3 scripts/noema_erb_bench.py cpu|gpu|hybrid
```

## Kuramoto substrate (C)

`scripts/kuramoto_substrate.c` — minimal C Kuramoto evolution for benchmark baseline.

## Mini

`scripts/htri_mini.py` — minimal HTRI implementation (768 oscillators, CPU).
