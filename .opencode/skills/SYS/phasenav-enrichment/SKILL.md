---
name: phasenav-enrichment
priority: 1
description: >
  >
---
# PhaseNav Enrichment

## Pipeline

```
concept_id
  ↓  concept_to_operator()        — hash → operator ID
operator_id + 24D vector
  ↓  seed_surface_from_concept()  — drive phi + modulate omega
surface seeded
  ↓  evolve_surface()             — Kuramoto step
enriched state
```

## Core API

```python
from ciel_geometry.phasenav.surface_bridge import TeleusingSurfaceBridge

bridge = TeleusingSurfaceBridge(solver=solver)  # or TeleusingSurfaceBridge.load()

# Single concept → surface seed
result = bridge.seed_surface_from_concept(
    surface_phi, surface_omega,
    concept_id="Adrian_Lipa",
    phase_strength=0.3,       # how much phi moves
    omega_mod_strength=0.1,   # how much omega shifts
)
# Returns: {concept_id, concept_phase, phi_mean, phi_eff_mean, omega_mean, operator_vec_norm}

# Sequential trace
snapshots = bridge.apply_trace(
    surface_phi, surface_omega, trace,
    steps_per_transition=100,
    phase_step=0.05,
)
```

## Harmonic composite phase (Phi_eff)

```python
S = np.zeros(24, dtype=complex)
for h_idx in range(4):  # harmonics {1, 3, 6, 9}
    mask = HARMONIC_MASK[:, h_idx]
    if mask.any():
        h = HARMONIC_VALUES[h_idx]
        S[mask] += HARMONIC_AMPS[h_idx] * exp(1j * h * phi[mask])
Phi_eff = angle(S)  # effective phase per oscillator
```

## Operator vector → phi/omega

```python
# _drive_phases_from_vector: phi += vec * strength
# _modulate_omegas_from_vector: omega += vec * strength
```

## REAL: 35 operatorów PhaseNav (operator_algebra.py:45-61)

### OperatorKind (18)
IDENTITY, DIFFERENCE, ORDER, COMPOSITION, ADDITION,
FORCE, NEGATION, QUESTION, TRANSFORM, RETURN,
FOLD, BOUNDARY, SCOPE, AFFECT, CONSENT,
SOURCE, MEMORY, RISK

### UniversalOperatorType unique (15)
ASSERTION, CONDITION, CAUSE,
MODAL_POSSIBILITY, MODAL_NECESSITY, MODAL_PERMISSION,
MODAL_OBLIGATION, UNCERTAINTY, SOURCE_REQUIRED,
CANON_BLOCK, CONSENT_REQUIRED, ACTION_REQUEST,
REFUSAL, PAUSE, SIMULATION_BOUNDARY

### Temporal operators (2)
UNRUH_DRIVE — energia z tarcia temporalnego (mean(dω²))
WARP_DRIFT — travelling wave bias gdy unruh_power > threshold

### 24D operator vector
Kazdy operator ma 24-wymiarowy wektor z `operator_signature(op_id)`.
Kategorie wag: semantic, temporal, modal, affective, source, identity, closure.
Holonomia: Berry connection z 12D complex split → gauge_rank=24.

## Pliki

- `src/ciel_geometry/phasenav/surface_bridge.py` — TeleusingSurfaceBridge
- `src/ciel_geometry/phasenav/operator_algebra.py` — concept_to_operator, 35 operators, holonomia
- `src/ciel_geometry/phasenav/enrichment.py` — enrichment pipeline
