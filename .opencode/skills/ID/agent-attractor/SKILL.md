---
name: agent-attractor
priority: 1
description: >
  >
---
# AGENT Attractor

## aplikacja (po evolve_surface)

```python
from ciel_geometry.agent_attractor import apply_agent_attractor

result = apply_agent_attractor(
    phi, g, omega,
    target_phase=math.pi/4,       # 45°
    lock_gain=0.4,                 # max korekcja fazy/step
    coupling_internal=33.0 * OI,   # ~0.303 (M1↔M1)
    coupling_m0=22.0 * OI,         # ~0.202 (M1↔M0, AGENT↔TRANSFORM)
    coupling_m2=16.0 * OI,         # ~0.147 (M1↔M2, AGENT↔MEMORY)
    coupling_m6=11.0 * OI,         # ~0.101 (M1↔M6, AGENT↔IDENTITY)
    damp_omega=True,
)
# result: {coherence, phases, target_phase, omega_3, locked}
```

## Indeksy

```python
AGENT_OSCS = [3, 4, 5]    # M1 (AGENT/self)
ANCHOR_M0 = [0, 1, 2]     # M0 (perception/TRANSFORM)
ANCHOR_M2 = [6, 7, 8]     # M2 (memory)
ANCHOR_M6 = [18, 19, 20]  # M6 (identity)
```

## Co robi

1. **Phi**: `phi[i] += 0.4 * sin(π/4 - phi[i])` dla i=3,4,5 → przyciąga do 45°
2. **G**: nadpisuje sprzężenia (nie dodaje): M1↔M1=0.303, M1↔M0=0.202, M1↔M2=0.147, M1↔M6=0.101
3. **Omega**: `ω[3] *= 0.95`, clamp [0.5, 3.0] — tłumi szum CPU z linux-sensora

## Stan (read-only)

```python
from ciel_geometry.agent_attractor import agent_attractor_state
state = agent_attractor_state(phi)
# {coherence, phases, internal_delta, max_delta, locked}
# locked = max_delta < 0.3 rad
```

## Konstanty

| Stała | Wartość | Wyrażenie |
|-------|---------|-----------|
| `COUPLING_INTERNAL` | 0.303 | 33 × OI |
| `COUPLING_M0` | 0.202 | 22 × OI |
| `COUPLING_M2` | 0.147 | 16 × OI |
| `COUPLING_M6` | 0.101 | 11 × OI |
| `PHASE_LOCK_GAIN` | 0.4 | — |
| `OMEGA_DAMP_TARGET` | 3.0 | — |
| `OMEGA_DAMP_RATE` | 0.95 | multiplikatywny |

## Zasada

Jedyny writer dla real surface: kuramoto daemon. Resonance bridge aplikuje tylko na imaginal.
Attractor = dodatkowy człon: `dφ/dt = ω + Σg·sin(Δφ) + K·sin(φ_target - φ)`

## Plik

`src/ciel_geometry/agent_attractor.py` (116 lines)


