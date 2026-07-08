# Kuramoto — pełna synchronizacja i harmonia

Oba skille Kuramoto zmergowane: Euler sync + harmonics 3-6-9

---

## Importy

Ten skill agreguje poniższe skille źródłowe:

- `kuramoto-euler-sync` → [`.opencode/skills/kuramoto-euler-sync/SKILL.md`](.opencode/skills/kuramoto-euler-sync/SKILL.md) (29 linii)
- `kuramoto-harmonics` → [`.opencode/skills/kuramoto-harmonics/SKILL.md`](.opencode/skills/kuramoto-harmonics/SKILL.md) (177 linii)

---

## 1. kuramoto-euler-sync

*Źródło: [`.opencode/skills/kuramoto-euler-sync/SKILL.md`](.opencode/skills/kuramoto-euler-sync/SKILL.md)*

---
name: kuramoto-euler-sync
priority: 1
description: >
  >
---

## Euler constraint

```python
R = |Σ e^{iφ_i}|
target: R = 0 → Σ e^{iφ_i} = 0
φ_target_i = angle(-Σ_{j≠i} e^{iφ_j})
```

## Live system

| Parametr | Wartość |
|----------|---------|
| Daemon | `ciel_noema_kuramoto_daemon.py` |
| Interval | 10Hz (0.1s) |
| N | 24 (HTRI) |
| harmonics | {1, 3, 6, 9} per oscillator |
| Euler residual R | 3-4 (target: 0) |
| τ̄ | 0.35-0.55 |

Euler feedback: `τ_i += 0.05 * R * cos(φ_target - φ_i) - 0.02 * (τ - 0.353)`


---

## 2. kuramoto-harmonics

*Źródło: [`.opencode/skills/kuramoto-harmonics/SKILL.md`](.opencode/skills/kuramoto-harmonics/SKILL.md)*

---
name: kuramoto-harmonics
priority: 1
description: >
  >
---

## Signatura

```python
def evolve_surface(surface, dt=0.01, *, flush=True, continuous=True, cont_every=10) -> float:
```

## Harmonic composite phase (Phi_eff)

```python
S = np.zeros(24, dtype=complex)
for h_idx in range(4):  # {1, 3, 6, 9}
    mask = HARMONIC_MASK[:, h_idx]
    if mask.any():
        h = HARMONIC_VALUES[h_idx]
        S[mask] += HARMONIC_AMPS[h_idx] * np.exp(1j * h * phi[mask])
Phi_eff = angle(S)
```

Harmonic amplitudes: `[1.0, 0.5, 0.33, 0.25]` — dekadentne, wyższe harmoniczne słabiej.

## Euler step

```python
diff = Phi_eff[:, None] - Phi_eff[None, :]
coupling = sum(g * sin(diff), axis=1) / 24

# flavor-modulated omega
mood_mod = (flavor[3] - 0.5) * OI * 50
closure_mod = (1.0 - flavor[4]) * OI * 30
coherence_damping = flavor[0] * OI * 10
effective_omega = omega * (1 + mood_mod + closure_mod - coherence_damping)

phi_new = (phi + dt * (effective_omega + coupling)) % 2π
```

## Hebbian plasticity

```python
activity = (flavor[2]*1.0 + flavor[4]*0.5 + (1-flavor[3])*0.3) / 1.8  # [0,1]
dg = 0.01*dt*10 * (activity - 0.5) * cos(diff) - 0.001*dt*10 * (g - I*0.1)
g += dg
clip(g, -1.0, 1.0)
```

## Gravity update

```python
dphi = angle(exp(1j * (phi_new - phi_old)))
semantic_density = min(10, mean(|dphi|) / dt)

gravity[0] = semantic_density          # kg·m²/s
gravity[1] = 1 + tanh(density*0.5)*9   # γ ∈ [1, 10]
gravity[2] = 0.99*mass + 0.01*density  # EMA mass
gravity[3] = mean(dω²)                 # Unruh power

if unruh_power > 1e-6:                 # WARP_DRIFT
    ramp = linspace(0, warp*2π, 24)
    warp_bias = 0.05 * warp * sin(ramp - phi)
    phi += dt * warp_bias
```

## sync_surface_geometry

```python
z = exp(1j * phi)
surface["Z_geom"] = Re(z)          # cos(φ) per osc
surface["R_geom"] = |mean(z)|      # global order parameter
surface["psi_geom"] = angle(mean(z))  # global mean phase
```

## sync_surface_holonomy

```python
H[0] = mean|A_ij|       # operator Berry connection (cached)
H[1] = gauge_rank       # operator gauge rank (cached)
H[2] = closure_score    # 0-1 (cached)
H[3] = surface_gamma    # φ Berry phase (live)
H[4] = max|A_ij|        # max connection (cached)
H[5] = winding          # integer (live)
H[6] = mean_curvature   # (cached)
```

## HTRI batch system (768 oscillators)

```python
N_CORE_OSC = 12                              # core linguistic oscillators
N_HTRI_BATCHES = 32                          # HTRI batches
N_HTRI_OSC = N_HTRI_BATCHES * N_OSCILLATORS # 32 × 24 = 768
N_HTRI_TOTAL = N_CORE_OSC + N_HTRI_OSC      # 780 total
```

- `init_htri_batch_system()` — init with modulated frequencies
- `evolve_htri_batch_system()` — Kuramoto on all 780
- `feed_htri_to_surface()` — aggregate 768→down to 24 surface phi

## Imaginal surface

```python
def evolve_imaginal_surface(imaginal, phi_real, g_real, omega_real, dt=0.01):
    """Evolve imaginal surface coupled to real surface state."""
    # Uses real g/omega as attractors, PLL-style sync

def project_imaginal_to_real(imaginal_phi):
    """Project imaginal phase back to real surface (phase blend)."""
```

## Coupling lifecycle

```python
initialize_coupling_from_memory_channels()  # M0-M7 → W_ij base
update_coupling_from_concepts(concept_ids)  # concept-driven modulation
update_coupling_hebbian(activity, W_ij)     # Hebbian: dW ∝ cos(Δφ)(a-0.5)
update_coupling_weight(W_ij, alpha=0.1)     # weighted blend
```

## Zero-point energy

```python
def compute_zpe(phi, g, omega) -> float:
    """Zero-point energy from phase gradients + coupling."""
```

## Continuous (Zeta-Schrödinger) hybrid

Co `cont_every` (default 10) ticków → zamiast Euler:
```python
phi_new = evolve_continuous(phi, dt=dt*10, hbar=0.1, coupling=coupling, omega_eff=effective_omega)
```
C² spline na 24 knotach → 512-point dense grid → kinetic + ζ-potential + drive → project back.

## AGENT attractor (po evolve_surface)

Aplikowany w kuramoto daemon, nie w evolve_surface:
```python
apply_agent_attractor(phi, g, omega)        # π/4 lock, coupling reinforce, ω[3] damp
# M2 boost: g[6-8, 0-2]=0.12, g[6-8, 3-5]=0.15, g[6-8, 6-8]=0.08
```

## REAL: 24-oscillator harmonic map (noema_surface_mmap.py:107-134)

BASE_TEMPORAL_HZ = 39.6 (Solfeggio 396/10)

HARMONIC_VALUES = [1, 3, 6, 9]
HARMONIC_AMPS = [1.0, 0.5, 0.33, 0.25]

M0 Perceptual (0-2):   {1,3}    → synchronizacja na 39.6 Hz i 118.8 Hz
M1 Working (3-5):      {1,6}    → 39.6 Hz i 237.6 Hz
M2 Episodic (6-8):     {1,9}    → 39.6 Hz i 356.4 Hz
M3 Semantic (9-11):    {3,6}    → 118.8 Hz i 237.6 Hz
M4 Procedural (12-14): {3,9}    → 118.8 Hz i 356.4 Hz
M5 Affective (15-17):  {6,9}    → 237.6 Hz i 356.4 Hz
M6 Identity (18-20):   {1,3,6}  → 39.6, 118.8, 237.6 Hz
M7 Braid (21-23):      {1,3,6,9} → full spectrum

Kazdy kanal synchronizuje sie na INNEJ harmonicznej → naturalny multiplekser.
M7 Braid ma pelne spektrum → hub cross-harmoniczny.

Implementacja w evolve_surface():
  S_i = sum(A_h * exp(1j * h * phi_i))
  Phi_eff = angle(S)
  coupling przez sin(Phi_eff_j - Phi_eff_i)

HEBB_LR = 0.00919 (OI)
HEBB_DECAY = 8.45e-5 (OI^2)

## Plik

`src/ciel_geometry/noema_surface_mmap.py` (1658 lines)


---
