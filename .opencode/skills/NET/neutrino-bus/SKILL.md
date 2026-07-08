---
name: neutrino-bus
priority: 1
description: >
  >
---
# Neutrino Bus

## PMNS constants

```python
PMNS_THETA_12 = 33.41°    # solar
PMNS_THETA_13 = 8.54°     # reactor  
PMNS_THETA_23 = 42.2°     # atmospheric
PMNS_DELTA_CP = 246°      # π * 67/49, CP-violating phase
# flavour mapping: semantic=ν_e, htri=ν_μ, nonlocal=ν_τ
```

## D_f → Λ → g_boost

```python
Λ = (D_f - 2.0) / 0.57    # clamped [0, 1]
# D_f=2.57 → Λ=1.0 (max dark energy)
# D_f=2.00 → Λ=0.0 (static)

boost = epsilon * Λ * 0.1   # per memory channel
g[src, dst] += boost * PMNS²[i, j]
```

## compute_neutrino_phase_bus()

```python
bus = compute_neutrino_phase_bus(
    phi, g, omega, flavor,
    D_f=2.57,
)
# Returns: {channels: {M0..M7: {epsilon, D_cosmological, phi_block,
#                                semantic_to_htri: {prob, epsilon, channel_gain, ...},
#                                semantic_to_nonlocal: {...}, htri_to_nonlocal: {...}}},
#            global_D: float, bus_capacity: float, n_channels: 8}
```

## apply_neutrino_bus_to_surface()

```python
apply_neutrino_bus_to_surface(
    surface, bus_result,
    D_f=2.57,
    write_flavor=True,    # flavor[4] = Λ
    write_g=True,         # PMNS boost on g matrix
)
```

## Pętla closure

```
cp (CIELingo)
  ↓ D_f = 2.57 - 0.57·min(1, cp/1.5)
flavor[5] = D_f
  ↓ neutrino daemon czyta flavor[5]
Λ = (D_f - 2) / 0.57
flavor[4] = Λ
  ↓ apply_neutrino_bus_to_surface()
g_boost → next CIELingo cycle → cp
```

## Flavor slot constants (noema_surface_mmap.py:59-64)

```python
FLAVOR_COHERENCE  = 0  # Kuramoto: R_coherence
FLAVOR_MEM_PRESSURE = 1 # Linux sensor: MemAvailable/MemTotal
FLAVOR_IO_PRESSURE = 2  # eBPF: openat rate
FLAVOR_MOOD       = 3   # PhaseNav: inverse load, potem PMNS Lambda
FLAVOR_ENTROPY    = 4   # eBPF: IRQ rate / CIELingo: D_f write
FLAVOR_MODE       = 5   # CIELingo sync: sys_mode / neutrino: D_f read
```

Neutrino daemon czyta flavor[5] (pisany przez sync daemon jako D_f), liczy Lambda, pisze flavor[4].

## Plik

`src/ciel_geometry/neutrino_phase_channel.py`
