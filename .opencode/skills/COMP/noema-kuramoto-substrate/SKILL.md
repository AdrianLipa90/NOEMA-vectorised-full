---
name: noema-kuramoto-substrate
priority: 1
description: >
  >
---
# Kuramoto Substrate (C)

## Build

```bash
cd scripts/kuramoto_substrate && make
```

## Use

```c
// Minimal C Kuramoto: evolve N oscillators, single step
```

## Compared to Python

| Wersja | Język | Throughput |
|--------|-------|-----------|
| Python (numpy) | Python | 1× |
| Substrate | C | ~50× |
| GPU (cupy) | CUDA | ~200× |

## Plik

`scripts/kuramoto_substrate/`
