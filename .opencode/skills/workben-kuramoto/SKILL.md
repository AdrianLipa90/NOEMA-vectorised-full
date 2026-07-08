---
name: workben-kuramoto
priority: 1
description: >
  Kuramoto engine — harmonics, nbody gravity, stress-energy, TARDIS time dilation, WARP drift
---
# Workben KURAMOTO

Kuramoto engine — harmonics, nbody gravity, stress-energy, TARDIS time dilation, WARP drift

## Źródła

Ten workben konsoliduje 8 źródłowych skilli:

- **Kuramoto Harmonics** (`COMP/kuramoto-harmonics`)
- **N-Body Gravity** (`COMP/nbody-gravity`)
- **Stress-Energy Tensor** (`COMP/stress-energy-tensor`)
- **TARDIS + WARP** (`COMP/tardis-warp`)
- **Continuous Propagator** (`COMP/continuous-propagator`)
- **Inference** (`COMP/noema-inference`)
- **Simulations** (`COMP/noema-sims`)
- **Metatime Validator** (`COMP/metatime-validator`)

## Kluczowe wzorce

### Kuramoto Harmonics

- Harmonic amplitudes: `[1.0, 0.5, 0.33, 0.25]` — dekadentne, wyższe harmoniczne słabiej.
- - `init_htri_batch_system()` — init with modulated frequencies
- - `evolve_htri_batch_system()` — Kuramoto on all 780

### Stress-Energy Tensor

- `src/ciel_geometry/tmuv_perturbation.py`
- - `scripts/stress_pc_noema_htri_phasenav.py`
- - `scripts/sims/energy_benchmark.py`

### TARDIS + WARP

- **Efekty**:
- - Kuramoto daemon: `dt_eff = dt / γ` (oscylatory zwalniają)
- - CIELingo sync: `τ *= min(γ, 3.0)` (caped 3×, rozciąga czas CIELingo)

### Continuous Propagator

- Wywoływany z evolve_surface() co cont_every=10 ticków.
- Jeśli import/call fail → cichy fallback do Euler.
- Tworzy potencjał z seria harmonicznych o ζ(1.5) wagach — preferuje niskie częstotliwości.

### Inference

- | Skrypt | Backend | Surface |
- |--------|---------|---------|
- | `run_ciel_gguf.py` | GGUF model | NOEMA mmap |

### Simulations

- | Skrypt | Opis |
- |--------|------|
- | `sims/energy_benchmark.py` | Energy benchmark |

### Metatime Validator

- | Sektor | Status | Best error |
- |--------|--------|-----------|
- | Charged leptons | ANSATZ_ONLY | 0.48% |

## Jak używać

```python
skill("workben-kuramoto")
```

Ładuje wiedzę ze wszystkich 8 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
