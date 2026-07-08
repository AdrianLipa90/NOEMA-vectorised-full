---
name: htri-gpu-bridge
priority: 2
description: >
  >
---
# HTRI GPU Bridge

## Hardware

- **GPU**: NVIDIA GTX 1050 Ti (4GB, 768 CUDA cores)
- **CPU**: Intel i5 (4 cores)
- **Memory**: 32GB DDR4

## HTRI jako model

- 768 oscylatorów na GPU
- 24-oscylatorowy surface na CPU (mmap)
- Bridge: scatter/gather między GPU a surface

## GPU acceleration

```python
import cupy as cp
# Kuramoto evolution na GPU
phi_gpu = cp.array(phi)
omega_gpu = cp.array(omega)
# evolve w batch
```

## Benchmark

```bash
python3 scripts/noema_erb_bench.py cpu    # CPU baseline
python3 scripts/noema_erb_bench.py gpu    # GPU accelerated
python3 scripts/noema_erb_bench.py hybrid # both
```

## Pliki

- `src/ciel_geometry/cuda_probe.py` — CUDA detection
- `scripts/noema_erb_bench.py` — benchmark suite
