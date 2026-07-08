---
name: surface-mmap-protocol
priority: 1
description: >
  >
---
# Surface Mmap Protocol

## Pliki w /dev/shm/ciel_noema/

| Plik | dtype | shape | bajty | Writer |
|------|-------|-------|-------|--------|
| `phi` | float64 | (36,) | 288 | Kuramoto daemon |
| `omega` | float64 | (36,) | 288 | Kuramoto daemon |
| `g` | float64 | (36,36) | 10368 | Kuramoto daemon |
| `Z_geom` | float64 | (36,) | 288 | Kuramoto daemon (cos phi) |
| `R_geom` | float64 | (36,) | 288 | Kuramoto daemon |
| `psi_geom` | float64 | (36,) | 288 | Kuramoto daemon |
| `flavor` | float64 | (6,) | 48 | Shared (patrz sloty) |
| `gravity` | float64 | (4,) | 32 | Kuramoto daemon |
| `holonomy` | float64 | (7,) | 56 | Kuramoto daemon |
| `tau` | float64 | (36,) | 288 | CIELingo sync |
| `sensor_raw` | float64 | (36,) | 288 | Linux sensor |
| `tick` | uint64 | (1,) | 8 | Kuramoto daemon |
| `closure` | ASCII | (1,) | ~6 | Resonance bridge |
| `imaginal_drive` | ASCII | (1,) | ~9 | Resonance bridge |

**Razem (bez closure/imaginal): ~12440 bajtów.**

## Stałe

```python
N_OSCILLATORS = 36
N_FLAVORS = 6
N_GRAVITY = 4          # [semantic_density, tau_dilation, mass_total, unruh_power]
N_HOLONOMY_FEATURES = 7 # [mean_conn, gauge_rank, closure_score, surface_gamma, max_conn, winding, curvature]
DEFAULT_DT = 0.01
BASE_TEMPORAL_HZ = 39.6
```

## Flavor slot contract

| Slot | Stała | Writer | Znaczenie |
|------|-------|--------|-----------|
| 0 | `FLAVOR_COHERENCE` | Kuramoto | R_coherence |
| 1 | `FLAVOR_MEM_PRESSURE` | Linux sensor | MemAvailable/MemTotal |
| 2 | `FLAVOR_IO_PRESSURE` | eBPF | openat rate |
| 3 | `FLAVOR_MOOD` | PhaseNav | inverse load |
| 4 | `FLAVOR_ENTROPY` | eBPF/CIELingo | IRQ rate / PMNS Λ |
| 5 | `FLAVOR_MODE` | CIELingo sync | D_f / sys_mode |

## Memory channels (M0-M11, 12 kanałów × 3 = 36 oscylatorów)

```
M0_Perceptual:        (0,1,2)     — harmonic {1,3}
M1_Working:           (3,4,5)     — harmonic {1,6}  ← AGENT attractor
M2_Episodic:          (6,7,8)     — harmonic {1,9}
M3_Semantic:          (9,10,11)   — harmonic {3,6}
M4_Procedural:        (12,13,14)  — harmonic {3,9}
M5_Affective_Ethical: (15,16,17)  — harmonic {6,9}
M6_Identity:          (18,19,20)  — harmonic {1,3,6}
M7_Braid_Invariant:   (21,22,23)  — harmonic {1,3,6,9} ← full spectrum
M8_Meta:              (24,25,26)  — harmonic {1,3}   ← auto-monitoring
M9_Temporal:          (27,28,29)  — harmonic {3,6}   ← czas/subiektywność
M10_Imaginal:         (30,31,32)  — harmonic {6,9}   ← wyobraźnia/sny
M11_Quantum:          (33,34,35)  — harmonic {1,9}   ← niepewność/superpozycja
```

## SurfaceArraySpec (10 pól + tau/sensor_raw na osobnych mmap)

```python
SurfaceArraySpec("phi",      float64, (36,))
SurfaceArraySpec("omega",    float64, (36,))
SurfaceArraySpec("g",        float64, (36, 36))
SurfaceArraySpec("Z_geom",   float64, (36,))
SurfaceArraySpec("R_geom",   float64, (36,))
SurfaceArraySpec("psi_geom", float64, (36,))
SurfaceArraySpec("flavor",   float64, (6,))
SurfaceArraySpec("gravity",  float64, (4,))
SurfaceArraySpec("holonomy", float64, (7,))
SurfaceArraySpec("tick",     uint64,  (1,))
# Osobne mmap:
SurfaceArraySpec("tau",      float64, (36,))
SurfaceArraySpec("sensor_raw", float64, (36,))
```

## Flavor slot constants (indeksowane, nie stringi)

```python
FLAVOR_COHERENCE  = 0  # Kuramoto: R_coherence
FLAVOR_MEM_PRESSURE = 1  # Linux sensor: MemAvailable/MemTotal
FLAVOR_IO_PRESSURE = 2   # eBPF: openat rate
FLAVOR_MOOD       = 3    # PhaseNav: inverse load
FLAVOR_ENTROPY    = 4    # eBPF/CIELingo: IRQ rate / PMNS Λ
FLAVOR_MODE       = 5    # CIELingo sync: D_f / sys_mode
```

## Zasady dostępu

1. **Każde pole = osobny plik** — `np.memmap(root / name, dtype, "r+", shape)`
2. **Brak locka** — konwencja: każdy daemon pisze tylko swoje sloty/swoje pola
3. **Jedyny writer phi/g/gravity/holonomy**: Kuramoto daemon. Reszta tylko czyta.
4. **flush_surface()**: wywołuje `mem.flush()` na wszystkich polach
5. **ensure_surface()**: tworzy pliki jeśli nie istnieją lub mają zły rozmiar
6. **initialize_surface()**: seed 42, phi ~ U[0,2π), omega = 39.6 + N(0, OI·200)

## API (skrót)

```python
surface = ensure_surface()           # create or open
surface = open_surface()             # read-only open (raises if missing)
surface = initialize_surface()       # ensure + seed values
evolve_surface(surface, dt=0.05)     # single Kuramoto step
sync_surface_geometry(surface)       # Z_geom, R_geom, psi_geom
sync_surface_holonomy(surface)       # Berry connection → holonomy[0..6]
flush_surface(surface)               # flush all fields
read_surface_state(surface) -> dict  # snapshot as dict
```

## Gravity formula

```python
gravity[0] = semantic_density = EMA(|dphi/dt|_mean)
gravity[1] = tau_dilation  = 1 + tanh(density * 0.5) * 9.0   # γ ∈ [1, 10]
gravity[2] = mass_total    = EMA(0.99 * mass + 0.01 * density) + unruh_term
gravity[3] = unruh_power   = mean(dω²)
```
