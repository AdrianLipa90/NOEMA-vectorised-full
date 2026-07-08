# NOEMA System Architecture

## 1. Overview

**NOEMA is a shared-memory oscillator substrate for real-time semantic phase synchronization.** It provides the phase-geometric carrier layer for the CIELingo language-synchronization stack, using 24 Kuramoto oscillators mapped to 8 memory channels (M0–M7) with 3-6-9 harmonic coupling.

### Key Design Principles

| Principle | Description |
|-----------|-------------|
| **Shared Memory IPC** | All inter-process communication goes through `/dev/shm/ciel_noema/` — POSIX shared memory with `numpy.memmap` arrays. No sockets, no JSON handshakes. |
| **NumPy Vectorization** | Every daemon uses `numpy` (≥1.24) for array operations. No PyTorch, no ONNX Runtime, no binary dependencies beyond numpy. |
| **Event-Driven Daemon Ensemble** | Six to seven independent daemon processes each claim surface files, read their inputs, compute, write outputs, and sleep for their interval. No central scheduler. |
| **Surface Protocol** | Binary-only surface files — raw `struct.pack` arrays with no metadata, no JSON wrappers. Each file is exactly one typed array. |
| **Dual-Surface Duality** | Two surfaces exist: the *real* surface (`/dev/shm/ciel_noema`) is the damped Poincaré readout; the *imaginal* surface (`/dev/shm/ciel_noema_imaginal`) is the primary Kuramoto generator with lower damping. |
| **Zero Central State** | No coordinator process. The surface *is* the state. Daemons converge through shared-memory reads and writes. |

### 3-6-9 Harmonic Foundation

Base temporal clock: **39.6 Hz** (Solfeggio fundamental 396 Hz ÷ 10, Tesla 3-6-9 principle). Each oscillator uses a subset of harmonics {1, 3, 6, 9} with amplitudes [1.0, 0.5, 0.33, 0.25]:

| Channel | Harmonics | Oscillators |
|---------|-----------|-------------|
| M0 Perceptual | {1, 3} | 0–2 |
| M1 Working | {1, 6} | 3–5 |
| M2 Episodic | {1, 9} | 6–8 |
| M3 Semantic | {3, 6} | 9–11 |
| M4 Procedural | {3, 9} | 12–14 |
| M5 Affective/Ethical | {6, 9} | 15–17 |
| M6 Identity | {1, 3, 6} | 18–20 |
| M7 Braid/Invariant | {1, 3, 6, 9} | 21–23 |

---

## 2. Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                        Daemon Ensemble                             │
│                                                                    │
│  Kuramoto     Neutrino    Resonance     Linux       CIELingo       │
│  (10Hz)       (2s)        Bridge (1s)   Sensor      Sync (30s)    │
│  φ evolution  PMNS mix    real↔imag     (1Hz)       Euler closure │
│               D_f → Λ     sync          /proc→φ    W_ij blend     │
│                                                                    │
│  PhaseNav     Nonlocal                                              │
│  (5s)         Proxy (1s)                                            │
│  operator     φ-RAG relay                                           │
│  enrichment   X25519 encrypt                                       │
└────┬─────────────┬──────────────┬──────────────┬───────────────────┘
     │             │              │              │
     │       open(O_SYNC)        │              │
     ▼             ▼              ▼              ▼
┌────────────────────────────────────────────────────────────────────┐
│                  /dev/shm/ciel_noema/                               │
│                                                                     │
│   phi[24]    omega[24]    g[24×24]    flavor[6]    tick[1]        │
│   Z_geom[24] R_geom[24]   psi_geom[24]                              │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────┐     │
│   │  /dev/shm/ciel_noema_imaginal/  (dual surface — imaginal) │     │
│   └──────────────────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────────────────┘
     ▲             ▲              ▲              ▲
     │             │              │              │
┌────┴─────────────┴──────────────┴──────────────┴───────────────────┐
│                         Client Layer                                │
│                                                                     │
│  ciel_coupling.py     ciel_sot_agent        CIELingo                │
│  (CLI coupling)       (integration kernel)  (Polish card topology) │
│                                                                     │
│  CIEL/Omega            opencode hooks        Host processes         │
│  (full consciousness)  (session lifecycle)   (user interaction)     │
└────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
            ┌──────────────┐
            │ Linux Sensor │ 1 Hz
            │  /proc → φ   │
            └──────┬───────┘
                   │ phi[24], flavor[0..5]
                   ▼
            ┌──────────────┐
            │   Kuramoto   │ 10 Hz
            │   evolve()   │
            └──────┬───────┘
                   │ phi', omega'
                   ▼
  ┌────────────────┼────────────────┐
  │                │                │
  ▼                ▼                ▼
┌──────────┐ ┌────────────┐ ┌──────────────┐
│Resonance │ │  Neutrino  │ │ CIELingo     │
│Bridge    │ │  PMNS mix  │ │ Euler sync   │
│(real↔imag)│ │  flavor[4] │ │ W_ij blend   │
└──────────┘ └────────────┘ └──────────────┘
                   │
                   ▼
            ┌──────────────┐
            │Tiered Memory │
            │Orchestrator  │
            └──────────────┘
```

---

## 3. Surface Protocol

### Location

All surface files live under `/dev/shm/ciel_noema/` (real) and `/dev/shm/ciel_noema_imaginal/` (imaginal). The parent directory is a `tmpfs` mount — RAM-backed.

### Format

Each surface file is a raw binary `numpy.memmap` array — no JSON, no headers, no metadata. The file name IS the array name. Daemons open files with `O_SYNC` for coherency; there are no locks (simple reader-writer semantics).

### Surface File Reference

| File | Type | Shape | Description |
|------|------|-------|-------------|
| `phi` | float64 | (24,) | Oscillator phases in [0, 2π) |
| `omega` | float64 | (24,) | Natural frequencies (rad/s) |
| `g` | float64 | (24, 24) | Coupling matrix W_ij |
| `flavor` | float64 | (6,) | Coherence vector (see flavor contract) |
| `tick` | uint64 | (1,) | Global iteration counter |
| `Z_geom` | float64 | (24,) | Geometric order parameter (imaginal) |
| `R_geom` | float64 | (24,) | Geometric radius |
| `psi_geom` | float64 | (24,) | Wavefunction magnitude |

### Flavor Channel Contract

Each daemon writes only its assigned flavor slots. This provides a primitive message bus between daemons:

| Slot | Name | Writer | Reader | Description |
|------|------|--------|--------|-------------|
| 0 | `cpu_coherence` | Linux Sensor | Kuramoto | CPU utilization coherence |
| 1 | `mem_pressure` | Linux Sensor | — | MemAvailable / MemTotal |
| 2 | `io_wait` | Linux Sensor | Resonance | I/O pressure proxy |
| 3 | `load_mood` | Linux Sensor / PhaseNav | — | Inverse load (operator affinity) |
| 4 | `entropy/Λ` | Neutrino / eBPF | CIELingoSync | PMNS cosmological constant Λ |
| 5 | `mode/D_f` | CIELingoSync | Neutrino | Fractal dimension / sys mode |

### Access Pattern

```python
import numpy as np
from pathlib import Path

surface_root = Path("/dev/shm/ciel_noema")
phi = np.memmap(str(surface_root / "phi"), dtype=np.float64, mode="r+", shape=(24,))
flavor = np.memmap(str(surface_root / "flavor"), dtype=np.float64, mode="r+", shape=(6,))
tick = np.memmap(str(surface_root / "tick"), dtype=np.uint64, mode="r+", shape=(1,))
```

---

## 4. Daemon Ensemble Overview

| # | Daemon | Script | Frequency | Surface Claims | Purpose |
|---|--------|--------|-----------|----------------|---------|
| 1 | Kuramoto | `ciel_noema_kuramoto_daemon.py` | 10 Hz (0.1s) | phi, omega, g, tick, flavor[0] | Phase evolution with 3-6-9 harmonic coupling |
| 2 | Neutrino | `ciel_noema_neutrino_daemon.py` | 2 s | flavor[4], g, tick | PMNS flavor mixing, D_f → Λ conversion |
| 3 | Resonance Bridge | `ciel_noema_resonance_bridge.py` | 1 s | phi, Z_geom (both surfaces) | Real↔imaginal dual-surface sync |
| 4 | Linux Sensor | `ciel_noema_linux_sensor_daemon.py` | 1 Hz | phi[0..23], omega, flavor[0..5] | Map /proc/sys → oscillator state |
| 5 | CIELingo Sync | `ciel_noema_cielingo_sync.py` | 30 s | flavor[5], g, phi, tick | Euler identity closure, PMNS W_ij blend |
| 6 | Nonlocal Proxy | `ciel_noema_nonlocal_proxy.py` | 1 s | phi, flavor (both surfaces) | Cross-agent φ-RAG relay, X25519 encrypt |
| 7 | PhaseNav | `ciel_noema_phasenav_daemon.py` | 5 s | phi, flavor[3] | Operator enrichment, ZIP concept seeding |

---

## 5. Oscillator Architecture

### Kuramoto Evolution

The core evolution step in `evolve_surface()` (`src/ciel_geometry/noema_surface_mmap.py:evolve_surface`):

```
For each oscillator i:
  S_i = Σ_h A_h · exp(i · h · φ_i)     // harmonic superposed phasor
  Φ_eff_i = angle(S_i)                  // effective harmonic phase

  dφ_i/dt = ω_i + Σ_j g_ij · sin(Φ_eff_j - Φ_eff_i)

  φ_i ← φ_i + dt · dφ_i/dt (mod 2π)
```

Harmonic amplitudes: h ∈ {1, 3, 6, 9}, A = [1.0, 0.5, 0.33, 0.25]. Each oscillator uses a subset per its channel assignment.

### Coupling Matrix (g / W_ij)

The 24×24 coupling matrix is built from:
1. **Gell-Mann SU(3) projection**: 8×8 channel coupling from λ₁, λ₄, λ₇ coefficients with exponential distance decay exp(-|a-b|/L3).
2. **PMNS neutrino mixing**: Flavor oscillation matrix U_αi² seeded into intra-channel 3×3 blocks.
3. **CIELingo W_ij override**: Adaptive blend (1–12%) between base couplings and PMNS-boosted values, stored in `couplings_wij_optimized.json`.
4. **CielPC↔CielMoto entanglement**: Boost g_ij by 0.5 between semantic-affective-identity clusters (M3+M5+M6, 9 osc) and procedural-perceptual clusters (M4+M0, 6 osc).

### Euler Identity Constraint

The target state satisfies Σ e^{iφ_k} = 0 (Euler closure). Each oscillator's target phase is:

```
φ_target_i = angle(-Σ_{j≠i} e^{iφ_j})
```

τ_i (learning rate) is modulated by the Euler residual R = |Σ e^{iφ_k}|:

```
τ_i += 0.05 · R · cos(φ_target_i - φ_i)    // increase when R is high
τ_i -= 0.02 · (τ_i - 0.353)                // decay to baseline
τ_i = clip(τ_i, 0.01, 1.0)
```

### PhaseNav Operators

33 universal operators (IDENTITY, DIFFERENCE, ORDER, FORCE, MEMORY, RISK, AFFECT, ...) map to 24D vectors that seed oscillator phase attractors. The operator algebra provides a vectorized matching layer that classifies the current system state (CPU load, memory pressure, I/O) into an operator fingerprint.

---

## 6. Memory Architecture (3-Tier)

### Tier 1 — Fast / Volatile

- **NOEMA surface mmap**: 24 Kuramoto oscillators in `/dev/shm/ciel_noema/`
- **PhaseMemory mmap**: Binary hypervector bindings for phase-token associations
- **HolonomicMemoryOrchestrator**: M0–M8 channel evolution (in-process, no persistence)

### Tier 2 — Medium / Durable

- **TSM SQLite**: Structured memory with holonomy columns (phase-resonant retrieval)
- **StateDB SQLite**: Orchestrator state + metrics history (cycle logs, cp, R, coherence)
- **HolonomicMemory**: Phase-resonant retrieval over TSM via phase-match scoring
- **CIELBlochEncoder**: Token → Bloch state → WOmega sector mapping

### Tier 3 — Deep / Archival

- **WPM HDF5**: Wave snapshots with metadata attributes (phase vectors at checkpoints)
- **BraidLedger JSONL**: Braid-side traces (nonlocal events, X25519 sessions)
- **UnifiedMemoryOrchestrator**: TMP → bifurcation → durable archival pipeline

### Write Routing

| Mode | Tiers Written | Trigger |
|------|--------------|---------|
| `AUTO` | T1 always; T2 if salience ≥ 0.6; T3 if bifurcation ≥ 1 | Default |
| `FAST` | T1 only | Ephemeral state |
| `DURABLE` | T1 + T2 | Important state |
| `DEEP` | All tiers | Checkpoint / archival |

### Read Routing

| Mode | Search Order |
|------|-------------|
| `AUTO` | T1 (surface) → T2 (resonant phase match) → T3 (archival) |
| `SURFACE` | T1 only — current oscillator state |
| `RESONANT` | T2 only — HolonomicMemory phase-resonant retrieval |
| `DEEP` | T2 + T3 — full archival search |

### Async Background

- **ConsolidationResonator**: Tags Kuramoto state → TSM writes → WOmega sector updates
- **CIELMemoryConsolidator**: LLM-based consolidation daemon (summarizes raw_logs → memories_index.db)

---

## 7. Integration Points

### CIELingo Semantic Encoder

CIELingo (`src/cielingo/`) provides Polish-language card-based linguistic topology. Phase-token mappings assign words and infinitive/modal potentials to specific oscillator indices. The `htri_brain_map.py` module maps 24 brain regions to oscillators. The semantic encoder injects phase targets into the surface during CIELingo sync cycles.

### opencode Hooks

The session lifecycle is managed via `ciel_session_hook.py` which starts/stops daemons and reads the CIEL system state. During each user message, `process_user_input()` triggers CIELingo enrichment.

### CIEL/Omega Engine

The full consciousness pipeline (`src/CIEL_OMEGA_COMPLETE_SYSTEM/`) integrates:
- **Kernel**: CIEL kernel v11/v12, orchestrator, runtime
- **Memory**: Full 3-tier implementation with EBA (Euler-Berry-Action) loop validation
- **Emotion**: CQCL-based affective state (curiosity, love, focus, explore, grief, joy)
- **Cognition**: Paradox operators, Lie4 algebra, semantic dynamics
- **Ethics**: Wave-based ethical scoring, alignment strengthening
- **Orbital**: Phase-based orbital bridge, holistic state resolution

### CIEL/Omega ↔ NOEMA Bridge

The `cielingo_bridge.py` and `orbital_bridge.py` modules connect CIEL/Omega state (emotion, ethics, memory) to the NOEMA surface (phi, omega, flavor). The bridge runs as part of the CIELingo sync daemon every 30s.

---

## 8. Key Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `N_OSCILLATORS` | 24 | Number of oscillators (8 channels × 3) |
| `N_FLAVORS` | 6 | Flavor vector length |
| `BASE_TEMPORAL_HZ` | 39.6 | Base clock: 396 Hz / 10 (Solfeggio) |
| `OI` | 0.009193 | Information operator / preference quantum: ln 2 / (24π) |
| `L3` | 7.0 | Collatz base channel (twin-prime seed path length) |
| `S_E` | 0.4737 | Electron lepton information action |
| `R_E_MU` | 0.0489 | e→μ lepton mixing ratio |
| `R_MU_TAU` | 0.0260 | μ→τ lepton mixing ratio |
| `E_PLANCK_MEV` | 1.22e22 | Planck energy in MeV |
| `DEFAULT_DT` | 0.01 | Default Kuramoto integration step |
| `SURFACE_ROOT` | /dev/shm/ciel_noema | Real surface directory |
| `IMAGINAL_ROOT` | /dev/shm/ciel_noema_imaginal | Imaginal surface directory |

---

## 9. Directory Layout

```
NOEMA/
├── src/
│   ├── ciel_geometry/            # Core oscillator engine
│   │   ├── noema_surface_mmap.py # Surface protocol, evolve_surface()
│   │   ├── linux_sensor.py       # /proc → 24D phase mapping
│   │   ├── resonance_bridge.py   # Real↔imaginal dual-surface
│   │   ├── neutrino_phase_channel.py  # PMNS mixing, D_f→Λ
│   │   ├── phasenav/             # Operator algebra (33 ops)
│   │   └── ...
│   ├── cielingo/                 # Polish linguistic topology
│   │   ├── htri_brain_map.py     # 24 region→oscillator mapping
│   │   ├── card_trace_eeg.py     # Card-based phase tracing
│   │   ├── tensor_scalar_field.py
│   │   └── ...
│   ├── ciel_sot_agent/           # Integration kernel
│   │   ├── ciel_pipeline.py      # Main pipeline
│   │   ├── orbital_bridge.py     # CIEL/Omega ↔ NOEMA
│   │   ├── state_db.py           # SQLite state persistence
│   │   └── ...
│   ├── CIEL_OMEGA_COMPLETE_SYSTEM/  # Full consciousness engine
│   │   └── ciel_omega/
│   │       ├── memory/           # 3-tier memory
│   │       ├── emotion/          # CQCL affect
│   │       ├── ethics/           # Wave ethics
│   │       └── ...
│   └── cielingo_core/            # Future SOT agent scaffolding
├── scripts/                      # 7 daemon scripts + utilities
├── docs/                         # Documentation
├── integration/                  # Manifests, reports, keys, logs
│   └── Orbital/main/manifests/   # sectors_global.json
└── AGENTS.md                     # CIEL session state
```
