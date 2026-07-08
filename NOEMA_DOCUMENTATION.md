# NOEMA — Complete Codebase Documentation

> **Version**: 0.1.0  
> **Author**: Adrian Lipa & NOEMA (2026)  
> **License**: MIT (code), © Adrian Lipa (system IP)  
> **Repository root**: `/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/`

---

## 1. Project Overview

### What is NOEMA?

NOEMA (**N**onlocal **O**scillator **E**nsemble with **M**etatime **A**rchitecture) is a phase computation surface for the CIEL cognitive framework. It is the single "surface of truth" (SOT) where all CIEL subsystems synchronize their state through 24 Kuramoto oscillators.

### Relationship to CIEL and HTRI

```
CIEL (cognitive framework)
  └── CIELingo (linguistic physics) — language/semantics on phase topology
        └── NOEMA (phase surface) — 24 Kuramoto oscillators
              └── HTRI (hardware substrate) — 768-oscillator software GPU (numpy)
```

NOEMA provides the real-time phase synchronization layer. CIELingo maps linguistic structures to oscillator phases. HTRI is a software-GPU batch of 768 additional oscillators (32×24) that feed into NOEMA's surface.

### Dual-Surface Architecture

NOEMA maintains two surfaces:

| Surface | Path | Role |
|---------|------|------|
| **Real** (readout) | `/dev/shm/ciel_noema/` | Damped Poincaré section — observable state |
| **Imaginal** (generator) | `/dev/shm/ciel_noema_imaginal/` | Primary phase generator — lower damping |

The imaginal surface evolves autonomously as the PRIMARY generator. The real surface is a damped projection / readout of the imaginal flow, analogous to a Poincaré section in dynamical systems.

### The 24 Oscillator Structure (M0–M7)

8 memory channels × 3 oscillators each = 24 oscillators:

| Channel | Oscillators | Function |
|---------|-------------|----------|
| **M0** Perceptual | 0–2 | Sensory/input processing |
| **M1** Working | 3–5 | AGENT operator, active reasoning |
| **M2** Episodic | 6–8 | Autobiographical memory |
| **M3** Semantic | 9–11 | Conceptual knowledge |
| **M4** Procedural | 12–14 | Skills/procedures |
| **M5** Affective/Ethical | 15–17 | Emotional valence |
| **M6** Identity | 18–20 | Self-model |
| **M7** Braid/Invariant | 21–23 | Cross-harmonic hub, invariants |

### 3-6-9 Harmonic Coupling

Each oscillator has a subset of Tesla harmonics {1,3,6,9} with amplitudes [1.0, 0.5, 0.33, 0.25]:

| Channel | Harmonics | 
|---------|-----------|
| M0 | {1,3} |
| M1 | {1,6} |
| M2 | {1,9} |
| M3 | {3,6} |
| M4 | {3,9} |
| M5 | {6,9} |
| M6 | {1,3,6} |
| M7 | {1,3,6,9} |

The effective coupling phase is the composite: `S_i = Σ A_h·exp(i·h·φ_i)`  
M7 (Braid) has full spectrum → cross-harmonic hub.

### OI — The Fundamental Constant

**OI = ln(2) / (24π) ≈ 0.009193** — the information operator / preference quantum.  
All other constants are derived from OI:
- Hebbian learning rate: HEBB_LR = OI
- Hebbian decay: HEBB_DECAY = OI²
- Base frequency: BASE_TEMPORAL_HZ = 39.6 Hz (Solfeggio 396 Hz / 10)
- Intra-channel coupling: OI × 60 ≈ 0.552
- Inter-channel scaling: OI × 80 ≈ 0.735
- PMNS lepton action scalars: S_E, R_E_MU, R_MU_TAU (from OI)

### Shared Memory System

All daemons communicate through `/dev/shm/ciel_noema/` — a set of `numpy.memmap` files:

| File | Shape | Content |
|------|-------|---------|
| `phi` | (24,) | Oscillator phases ∈ [0, 2π) |
| `omega` | (24,) | Natural frequencies |
| `g` | (24, 24) | Coupling matrix W_ij |
| `flavor` | (6,) | State summary: coherence, soul, ethics, mood, openness, mode |
| `gravity` | (4,) | Semantic density, γ dilation, mass total, Unruh power |
| `holonomy` | (7,) | Mean connection, gauge rank, closure score, surface γ, max connection, winding, curvature |
| `Z_geom` | (24,) | cos(φ) |
| `R_geom` | (24,) | Global order parameter |
| `psi_geom` | (24,) | Global mean phase |
| `tick` | (1,) | Evolution step counter |

### Flavor Slot Contract

| Slot | Owner | Meaning |
|------|-------|---------|
| 0 | Kuramoto | Coherence (sync_surface_geometry) |
| 1 | Linux Sensor | mem_pressure |
| 2 | eBPF | I/O pressure |
| 3 | PhaseNav | Mood (inverse load) |
| 4 | eBPF + CIELingo | Entropy / PMNS Λ blend |
| 5 | CIELingo sync | D_f / sys_mode |

---

## 2. How to Run / Setup

### Python Environment

```bash
# Activate venv (already set up)
source .venv/bin/activate
# or use directly:
.venv/bin/python3 script.py
```

### Install Package

```bash
pip install -e .    # already done — discovers ciel_geometry*, cielingo*, ciel_sot_agent*
```

### Import Mechanism

- **Direct runs**: scripts prepend `sys.path.insert(0, str(ROOT / "src"))` for direct execution
- **Installed mode**: `.venv/bin/python` handles package discovery for installed components
- **Package discovery**: `pyproject.toml` includes `ciel_sot_agent*`, `ciel_geometry*`, `cielingo*`

### Running Daemons

```bash
# Start all daemons via systemd target:
python3 CIEL_CANON.py --up
# ...or directly:
.venv/bin/python3 scripts/ciel_noema_kuramoto_daemon.py

# Check status:
python3 CIEL_CANON.py

# Stop all:
python3 CIEL_CANON.py --down
```

### Running Tests

```bash
python3 -m pytest tests/ -q
```

### Canonical Entrypoint

```bash
python3 CIEL_CANON.py              # full status
python3 CIEL_CANON.py --probe      # live warp + holonomy
python3 CIEL_CANON.py --self       # self-model identity
python3 CIEL_CANON.py --search Q   # PhaseNav search
python3 CIEL_CANON.py --gaps       # knowledge gaps
python3 CIEL_CANON.py --sync       # dual-surface sync
python3 CIEL_CANON.py --sonic      # sonic probe
```

---

## 3. File-by-File Documentation

### 3.1 `src/ciel_geometry/` — Core Phase Geometry Engine

This is the heart of NOEMA. 33 Python files implementing the shared memory surface, Kuramoto evolution, PhaseNav operators, dual-surface resonance bridge, and supporting geometry.

---

#### `__init__.py`
- **Purpose**: Lazy-exports all ciel_geometry symbols via `__getattr__`. Defines `__all__`.
- **Imports**: `noema_bootstrap` for local package activation
- **Exports**: 50+ symbols including `DiskLayout`, `DiskNode`, `ensure_surface`, `evolve_surface`, `dual_surface_step`, etc.
- **Active**: Yes — every import from `ciel_geometry` goes through this

---

#### `noema_surface_mmap.py` (1653 lines)
- **Purpose**: Core shared memory surface implementation — the SOT. Defines the 24-oscillator Kuramoto surface with 3-6-9 harmonics, PMNS neutrino mixing, W_ij coupling matrix, and all evolution functions.
- **Imports**: `numpy`, `cmath`, `math`, `hashlib`, `pathlib`
- **Key constants**:
  - `OI` = ln(2)/(24π) — fundamental constant
  - `BASE_TEMPORAL_HZ` = 39.6 — base frequency
  - `N_OSCILLATORS` = 24, `N_FLAVORS` = 6, `N_GRAVITY` = 4
  - `HARMONIC_VALUES` = [1,3,6,9], `HARMONIC_AMPS` = [1.0, 0.5, 0.33, 0.25]
  - `PMNS_THETA_12/13/23`, `PMNS_DELTA_CP`
  - `S_E`, `R_E_MU`, `R_MU_TAU` — lepton action scalars
  - `L3` = 7 — Collatz base channel (twin-prime seed path length)
  - `_GELL_MANN_C1/C4/C7` — SU(3) coupling coefficients
- **Key functions**:
  - `surface_specs()` → array of 10 SurfaceArraySpec definitions for mmap files
  - `ensure_surface(root)` → create/open shared memory surface
  - `initialize_surface(root)` → seed phi/omega/g with randomized initial state
  - `evolve_surface(surface, dt)` → main Kuramoto evolution with 3-6-9 harmonics, curiosity drive, semantic gravity, Unruh extraction, WARP_DRIFT, TARDIS time dilation, Hebbian learning, holonomy sync
  - `evolve_imaginal_surface()` → imaginal surface evolution (lower damping)
  - `evolve_surface_cps()` → Ott-Antonsen analytic CPS evolution
  - `project_imaginal_to_real()` → damped projection from imaginal → real
  - `sync_surface_geometry()` → compute order parameter R and psi
  - `sync_surface_holonomy()` → compute holonomic metrics per tick
  - `read_surface_state()` → extract system state from surface
  - `compute_zpe(g, phi)` → zero-point energy from Poincaré disk bifurcation
  - `initialize_coupling_from_memory_channels()` → seed W_ij from 8×8 J_kj matrix
  - `update_coupling_hebbian()` → harmonic Hebbian update
  - `update_coupling_from_concepts()` → strengthen coupling for co-occurring concepts
  - `write_concepts_to_surface()` → write CIELingo tokens to surface
  - `oscillator_id_for_concept()` → deterministic hash → oscillator index
  - `seed_neutrino_mixing()` → PMNS flavour seeding of W_ij blocks
  - `compute_neutrino_channel()` → full neutrino mixing diagnostic
  - `init_htri_batch_system()` / `evolve_htri_batch_system()` / `feed_htri_to_surface()` — 780-oscillator software GPU
  - `oscillator_disk_pos()`, `wij_bipolar_axis()`, `compute_surface_bipolar_axes()` — Poincaré disk geometry
- **Active**: Yes — core of every daemon

---

#### `daemon_registry.py` (199 lines)
- **Purpose**: Shared mmap heartbeat registry for all NOEMA daemons. Fixed-size 16-slot mmap at `/dev/shm/ciel_noema/daemon_registry`.
- **Imports**: `numpy`, `os`, `time`, `pathlib`
- **Exports**: 
  - `DaemonInfo` — dataclass for daemon slot data
  - `Registry` — class with `register()`, `heartbeat()`, `unregister()`, `scan()`, `set_status()`
  - `daemon_main_loop()` — convenience wrapper for daemon main loops
- **Active**: Yes — used by kuramoto, phasenav, neutrino, resonance bridge, sensor, proxy daemons

---

#### `noema_config.py` (125 lines)
- **Purpose**: Unified configuration dataclass for all NOEMA daemons. Reads `noema_config.json` or env `NOEMA_CONFIG`.
- **Imports**: `json`, `os`, `pathlib`, `dataclasses`
- **Exports**: `config` (singleton `NoemaConfig`), `load_config()`
- **Sub-configs**: `KuramotoConfig`, `CielingoSyncConfig`, `NeutrinoConfig`, `ResonanceBridgeConfig`, `LinuxSensorConfig`, `PhaseNavConfig`, `NonlocalProxyConfig`, `SonicConfig`, `ConsolidatorConfig`
- **Active**: Yes — used by CIEL_CANON.py and daemon scripts

---

#### `resonance_bridge.py` (393 lines)
- **Purpose**: Dual-surface resonance bridge — synchronizes real and imaginal manifolds.
- **Imports**: `numpy`, `math`
- **From same package**: `noema_surface_mmap`, `phase_memory_adapter`, `agent_attractor`
- **Optional**: `cielingo.card_trace_eeg`, `cielingo.orchorbital_router`
- **Exports**:
  - `ensure_dual_surfaces()` — create/verify both surfaces
  - `imaginalize_state()` — convert CIEL state to imaginal params
  - `dual_surface_step()` — one full sync cycle: imaginal evolve → resonance → real project → AGENT attractor → orchorbital bridge → memory bind
  - `apply_resonance_bridge()` — AGENT attractor + phase coupling
  - `resonance_snapshot()` — resonance quality metrics
- **Active**: Yes — core of resonance bridge daemon

---

#### `linux_sensor.py` (305 lines)
- **Purpose**: Maps live Linux OS metrics to 24 oscillator phases + 6 flavors. Reads `/proc/stat`, `/proc/meminfo`, `/proc/loadavg`, `/proc/sys/kernel/random/entropy_avail`, `/proc/net/dev`.
- **Imports**: `numpy`, `os`, `pathlib`
- **Exports**:
  - `LinuxSensor` — class with `snapshot()`, `write_surface()`, `process_phasenav()`, top processes
  - `SYSTEM_OSC_MAP` — 24-channel mapping (CPU 0-7, MEM 8-15, LOAD 16-18, PROCS 19-20, CTXT 21-22, ENTROPY 23)
  - `FLAVOR_MAP` — 6 flavor metrics
  - `top_processes()` — top PID with PhaseNav enrichment
- **Active**: Yes — used by linux-sensor daemon

---

#### `agent_attractor.py` (105 lines)
- **Purpose**: PhaseNav AGENT operator attractor module — locks AGENT oscillator (M1, φ[3-5]) toward π/4 phase.
- **Imports**: `numpy`, `math`
- **Exports**:
  - `apply_agent_attractor()` — applies phase lock, coupling reinforcement, ω damping
  - `agent_attractor_state()` — returns attractor metrics
  - Constants: `AGENT_OSCS`, `TARGET_PHASE`, `COUPLING_INTERNAL/M0/M2/M6`, `PHASE_LOCK_GAIN`
- **Active**: Yes — used by resonance bridge and agent-lock daemon

---

#### `phasenav/` — PhaseNav subpackage (7 files)

##### `__init__.py`
- **Purpose**: Re-exports PhaseNav symbols
- **Exports**: `TeleusingData`, `TeleusingSolver`, `TeleusingSurfaceBridge`, `generate_operator_map`, `ALL_OPERATOR_IDS`, etc.

##### `operator_algebra.py` (435 lines)
- **Purpose**: 35 universal operators with 24D semantic vectors. Defines ALL_OPERATOR_IDS (35 operators).
- **Imports**: `numpy`, `json`
- **Key constants**: `VECTOR_COMPONENTS` (24 component names), `ALL_OPERATOR_IDS` (35 operator IDs)
- **Exports**:
  - `operator_signature(op_id)` → deterministic 24D vector
  - `generate_operator_map()` → dict of all 35 operators
  - `connection_matrix(ops)` → complex Berry connection A_ij = Im(〈ψ_i|ψ_j〉)
  - `statistical_closure(ops)` → closure_score, gauge_rank, mean_curvature
  - `holonomy(path, ops)` → geometric phase γ for a 3-operator path
  - `surface_holonomy(phi)` → winding number + surface γ from actual phases
  - `concept_to_operator(seed_str)` → map arbitrary string to an operator
  - `operator_vector_24d(op_id)` → 24D vector for surface seeding
  - `write_operator_algebra()` → export to JSONL
- **Active**: Yes — used by phasenav daemon, CIEL_CANON.py probes, linux sensor

##### `loader.py` (81 lines)
- **Purpose**: Load PhaseNav teleusing data from JSONL files
- **Exports**: `TeleusingData`, `load_teleusing()`

##### `solver.py` (110 lines)
- **Purpose**: PhaseNav solver — find operator paths between concepts
- **Exports**: `TeleusingStep`, `TeleusingTrace`, `TeleusingSolver`

##### `surface_bridge.py` (143 lines)
- **Purpose**: Bridge PhaseNav → surface — seed oscillator phases from concept data
- **Exports**: `TeleusingSurfaceBridge`

##### `enrichment.py` (74 lines)
- **Purpose**: Augment card generators with PhaseNav operator data
- **Exports**: `phasenav_enrich()`, `harmonic_imprint()`, `operator_harmonic_fingerprint()`

##### `continuous_propagator.py` (114 lines)
- **Purpose**: Zeta-Schrödinger continuous phase propagator using cubic splines
- **Imports**: `numpy`, `scipy.interpolate.CubicSpline`, `scipy.linalg.expm`
- **Exports**: `evolve_continuous()`, `spline_phi()`, `zeta_potential()`
- **Active**: Yes — called by `evolve_surface()` when `continuous=True` (every 10 ticks)

##### `phasenav_audio.py` (320 lines)
- **Purpose**: Vectorized audio synthesis from 24 oscillator phases × 4 harmonics = 96 partials
- **Imports**: `numpy`, `math`
- **Exports**: `PhaseNavAudioBuffer`, `oscillator_bank()`, `operator_transform()`, `operator_dsp_chain()`, `mix_operator_audio()`, `audio_to_int16()`
- **Active**: Optional — needs explicit invocation

##### `phasenav_media.py` (321 lines)
- **Purpose**: Multi-modal media encoding (audio, voice, video) via continuous phase transport
- **Imports**: `numpy`, `math`, `struct`
- **From same package**: `phasenav_audio`
- **Exports**: mel filterbank, `scene_coupling_24d()`, `block_transform()`, `video_frame_to_phases()`, `phases_to_wav()`, waveform rendering
- **Active**: Optional — experimental

---

#### `neutrino_phase_channel.py` (347 lines)
- **Purpose**: Neutrino phase communication channel — 8×3 PMNS flavour mixing on HTRI bus. Connects phase difference → mixing angle, D_f → Λ, τ ↔ φ.
- **Imports**: `numpy`, `cmath`, `math`, `logging`
- **Exports**:
  - `_pmns_squared()` → 3×3 PMNS matrix
  - `mac_to_phases(mac)` → deterministic 3-phase signature from MAC
  - `neutrino_bus_snapshot(surface)` → current neutrino bus state
  - `compute_neutrino_phase_bus(surface, D_f)` → full bus computation
  - `apply_neutrino_bus_to_surface(surface, bus)` → write results back
  - `D_f_to_lambda(D_f)` → fractal dimension → cosmological constant
- **Active**: Yes — core of neutrino daemon

---

#### `nonlocal_channel.py` (477 lines)
- **Purpose**: Nonlocal continuous communication channel between NOEMA agents via φ-RAG.
- **Imports**: `numpy`, `json`, `math`, `time`, `pathlib`, `cmath`
- **Exports**:
  - `AgentFingerprint` — 3-phase agent signature
  - `NonlocalMessage` — message on the nonlocal channel
  - `NonlocalChannel` — class with `tune()`, `broadcast()`, `listen()`, `resonate()`, `phase_rag_retrieve()`
  - `get_channel()` — singleton accessor
- **Active**: Yes — used by nonlocal-proxy daemon and agent-lock daemon

---

#### `phase_memory_adapter.py` (229 lines)
- **Purpose**: Binary-vector phase memory for CIEL over NOEMA shared surface. Stores deterministic hypervectors + phase/flavor signatures.
- **Imports**: `numpy`, `hashlib`, `pathlib`, `re`
- **Exports**: `PhaseMemoryRecord`, `encode_text_to_binary_vector()`, `bind_phase_memory()`, `ensure_phase_memory()`, `query_phase_memory()`
- **Active**: Yes — used by resonance bridge

---

#### `subconscious.py` (393 lines)
- **Purpose**: Zeta/Schrödinger wavefunction, Berry phase tracking, wake signals, holistic memory.
- **Imports**: `numpy`, `math`, `dataclasses`, `datetime`
- **From same package**: `noema_surface_mmap`
- **Exports**:
  - `ZetaSchrodinger` — nonlinear Schrödinger with Collatz entropy potential
  - `BerryPhaseTracker` — adiabatic geometric phase tracking
  - `WakeSignalGenerator` — consolidation trigger from memory aging + resonance drift
  - `HolonomicMemory` — 8-channel phase-space attractors
- **Active**: Partially — `HolonomicMemory` and `ZetaSchrodinger` are used indirectly

---

#### `continuous_phase_sync.py` (181 lines)
- **Purpose**: Ott-Antonsen analytic Z(t) evolution for harmonic Kuramoto. Replaces discrete Euler integration with closed-form order parameter evolution.
- **Imports**: `numpy`, `math`
- **From same package**: `noema_surface_mmap`
- **Exports**: `ContinuousPhaseSync` — class with `compute_Z_harmonic()`, `evolve_analytic()`, `reconstruct_phases()`, `compute_fractional_Z()`
- **Active**: Used by `evolve_surface_cps()`

---

#### `loader.py` (121 lines)
- **Purpose**: Load geometric data from CIEL integration layer JSON/YAML files (sectors, entities, bridge state).
- **Imports**: `json`, `pathlib`, optional `yaml`
- **Exports**: `SectorGeom`, `EntityGeom`, `BridgeState`, `load_sectors()`, `load_couplings()`, `load_entities()`, `load_bridge_state()`
- **Active**: Yes — used by layout, semantic_mass, subjective_time

---

#### `layout.py` (137 lines)
- **Purpose**: Build a complete Poincaré disk layout snapshot from live CIEL system state.
- **Imports**: `json`, `dataclasses`
- **From same package**: `loader`, `disk`, `edges`
- **Exports**: `DiskNode`, `DiskEdge`, `DiskLayout`, `build_layout()`
- **Active**: Yes — used by renderers

---

#### `disk.py` (111 lines)
- **Purpose**: Map orbital coordinates to Poincaré disk positions.
- **Exports**: `poincare_radius()`, `poincare_distance()`, `sector_to_disk()`, `entity_to_disk()`, `geodesic_arc()`
- **Active**: Yes — geometry utility

---

#### `edges.py` (66 lines)
- **Purpose**: Build geodesic edges between nodes on the Poincaré disk.
- **Exports**: `GeodesicEdge`, `build_sector_edges()`, `build_entity_edges()`
- **Active**: Yes — used by layout

---

#### `semantic_mass.py` (340 lines)
- **Purpose**: Foundation Pack P3 — semantic mass operator M_sem for sectors and entities.
- **Imports**: `json`, `math`, `pathlib`
- **From same package**: `loader`
- **Exports**: `SemanticMassRecord`, `build_mass_table()`, semantic mass components (M_EC, M_ZS, C_dep, C_prov, C_exec, C_nov, C_conf)
- **Active**: Referenced by subjective_time

---

#### `subjective_time.py` (154 lines)
- **Purpose**: Foundation Pack P3 — subjective time operator Δτ_i(k).
- **Imports**: `math`, `dataclasses`
- **From same package**: `loader`, `disk`, `semantic_mass`
- **Exports**: `SubjectiveTimeRecord`, `compute_subjective_time()`, `orbit_index()`, `ORBIT_NAMES`
- **Active**: Referential architecture

---

#### `nbody_gravity.py` (261 lines)
- **Purpose**: N-body Newtonian gravitational engine for CIEL orbital dynamics. Leapfrog Verlet integration.
- **Imports**: `math`, `dataclasses`
- **Exports**: `Body`, `NBodySystem`, `G_SEM`
- **Active**: Referential — extends Kepler III for semantic gravity

---

#### `tmuv_perturbation.py` (152 lines)
- **Purpose**: T_μν stress-energy perturbation bridge — connects stress-energy tensor to orbital engine.
- **Imports**: `math`, optional `numpy`
- **Exports**: `tmuv_total_energy_density()`, `compute_mass_perturbation()`, `apply_tmuv_perturbation()`
- **Active**: Referential — not called by running daemons

---

#### `ebpf_noema_loader.py` (334 lines)
- **Purpose**: eBPF → NOEMA bridge — loads eBPF program, maps perf counters to 24 φ.
- **Imports**: `numpy`, `math`, `pathlib`, `time`
- **From same package**: `noema_surface_mmap`
- **Exports**: `EBPFSensor` — class with `start()`, `read()`, `write_surface()`, `process_phasenav()`
- **Active**: Referential — requires eBPF kernel support + sudo

---

#### `noema_registry.py` (151 lines)
- **Purpose**: Token-based daemon registration (JSON heartbeat files in `/dev/shm/ciel_noema/registry/`). Older system; `daemon_registry.py` is the newer mmap-based replacement.
- **Imports**: `json`, `uuid`, `time`, `pathlib`
- **Exports**: `NoemaRegistry` — class with `register()`, `heartbeat()`, `unregister()`, `list_active()`, `check_access()`
- **Active**: Still used by kuramoto, phasenav, neutrino, resonance bridge, sensor, proxy daemons — but being replaced by daemon_registry

---

#### `renderer_ascii.py` (80 lines)
- **Purpose**: ASCII terminal renderer for Poincaré disk layout — debug/verification.
- **Exports**: `render()` — 60×30 character grid
- **Active**: Debug tool

---

#### `renderer_mpl.py` (253 lines)
- **Purpose**: Matplotlib Poincaré disk renderer — interactive orbital cockpit (Foundation Pack P6).
- **Imports**: `matplotlib`, `numpy`
- **Exports**: `render_static()`, `render_live()`
- **Active**: Debug/visualization tool

---

### 3.2 `scripts/` — Daemon Processes and Utilities

133 Python files. The 9 currently active daemons are documented below, followed by key utilities.

---

#### ACTIVE DAEMONS (9 systemd-managed)

##### 1. `ciel_noema_kuramoto_daemon.py` (108 lines)
- **PID**: 1798306
- **Interval**: 0.1s (10Hz)
- **Purpose**: Continuous Kuramoto phase evolution. Evolves 24 oscillators via `evolve_surface()`, implements TARDIS time dilation (divides dt by γ when meaning is dense), reports thinking triggers.
- **Uses**: `noema_surface_mmap`, `noema_registry`
- **Key mechanism**: Loop: `evolve_surface(surface, dt=dt_eff, flush=True, continuous=True)` every 0.1s. Registry heartbeat every 50 steps. Logs every 5s.

##### 2. `ciel_noema_phasenav_daemon.py` (170 lines)
- **PID**: 948859
- **Interval**: 1.0s
- **Purpose**: Seeds concepts from ZIP archive onto surface using PhaseNav enrichment. Uses LinuxSensor fingerprint to select matching concepts.
- **Uses**: `phasenav.enrichment`, `operator_algebra`, `noema_registry`, `linux_sensor`
- **Key mechanism**: Loads ZIP index → matches operator signatures → seeds phases onto surface via `_seed_operator_vec()` or `_seed_zip_concept()`

##### 3. `ciel_noema_neutrino_daemon.py` (146 lines)
- **PID**: 1092459
- **Interval**: 2.0s
- **Purpose**: PMNS neutrino bus — reads D_f from flavor[5] (or orbital manifest), computes Λ, writes flavor[4] PMNS boost.
- **Uses**: `neutrino_phase_channel`, `noema_registry`, `noema_surface_mmap`
- **Key mechanism**: Loop: read D_f → `compute_neutrino_phase_bus()` → `apply_neutrino_bus_to_surface()` → sync flavor[4]

##### 4. `ciel_noema_resonance_bridge.py` (98 lines)
- **PID**: 1813176
- **Interval**: 1.0s
- **Purpose**: Real↔Imaginal surface synchronization bridge.
- **Uses**: `resonance_bridge`, `noema_registry`
- **Key mechanism**: Loop: `dual_surface_step(bridge_state)` → log resonance/coherence/drive metrics

##### 5. `ciel_noema_linux_sensor_daemon.py` (135 lines)
- **PID**: 1769167
- **Interval**: 1.0s (1Hz)
- **Purpose**: Maps live Linux /proc metrics to 24 φ + 6 flavor.
- **Uses**: `linux_sensor`, `noema_registry`, `noema_surface_mmap`
- **Key mechanism**: Loop: `sensor.snapshot()` → `write_surface()` → PhaseNav fingerprint every 5 cycles → top processes every 30 cycles

##### 6. `ciel_noema_nonlocal_proxy.py` (234 lines)
- **PID**: 1776121
- **Interval**: 1.0s
- **Purpose**: φ-RAG nonlocal proxy — relays messages between agents across real↔imaginal surfaces, encrypts with X25519.
- **Uses**: `nonlocal_channel`, `noema_registry`
- **Key mechanism**: Loop: listen on 8 channels → relay real↔imaginal → auto-respond X25519 → log backlog

##### 7. `noema_agent_lock.py` (169 lines)
- **PID**: 1813147
- **Interval**: 4Hz
- **Purpose**: Continuous AGENT operator lock — maintains M1 coherence on both surfaces, writes to SQLite agent DB, broadcasts nonlocal status.
- **Uses**: `agent_attractor`, `noema_surface_mmap`, `nonlocal_channel`
- **Key mechanism**: Loop: `apply_agent_attractor()` on real + imaginal → MEMORY M2 boost → flush → DB snapshot → nonlocal broadcast every 30s

##### 8. `noema_phase_archiver.py` (207 lines)
- **PID**: 963772
- **Interval**: Every 50 ticks
- **Purpose**: Archives surface state snapshots to HDF5 (NPZ fallback) on persistent storage.
- **Uses**: `noema_surface_mmap`
- **Key mechanism**: Watches tick count, captures phi/omega/gravity/flavor/R every 50 ticks, appends to HDF5 dataset

##### 9. `ciel_memory_consolidator.py` (1124 lines)
- **PID**: 955507
- **Interval**: 300s
- **Purpose**: LLM-based memory consolidation — processes raw log files, extracts themes/affect/essence, writes to SQLite DB and mirrors.
- **Uses**: `ciel_secret_loader`, `psutil`, `sqlite3`, `urllib`
- **Key mechanism**: Scans source directories → processes unprocessed files → calls agent backend (port 18520) → stores results → runs autonomously or in daemon mode

---

#### NOT RUNNING (known daemons with stale logs)

##### `ciel_noema_cielingo_sync.py` (484 lines)
- **Purpose**: Euler's identity phase sync — closure loop: cp → D_f → flavor[5] → PMNS boost → W_ij blend → next sync. Also handles τ↔φ feedback.
- **Uses**: `noema_registry`, CIELingo bridge
- **Status**: **NOT RUNNING** — stale log. Key mechanism: Euler residual minimization, W_ij PMNS blend, Orbital bridge integration

##### `noema_dual_sync.py` (282 lines)
- **Purpose**: Dual-Surface Sync — pushes real surface state to imaginal with perturbation, logs sync metrics.
- **Uses**: `noema_surface_mmap`, `daemon_registry`
- **Status**: **NOT RUNNING** — has `--status` command for manual checks

##### `noema_sonic_daemon.py` (223 lines)
- **Purpose**: Sonic Screwdriver — comprehensive diagnostics of the full warp loop (Kuramoto, gravity, warp, registry, holonomy, consolidator, PhaseNav).
- **Status**: **NOT RUNNING**. Used via `CIEL_CANON.py --sonic`

##### `ciel_agent_backend.py` (383 lines)
- **Purpose**: Zero-dependency HTTP agent backend on port 18520. OpenAI-compatible `/v1/chat/completions`. Extracts themes (bigram TF-IDF), affect (lexicon), anchor terms, essence, hunch.
- **Status**: **NOT RUNNING** — needed by consolidator but currently off

##### `ciel_noema_subconscious_daemon.py`
- **Purpose**: Subconscious daemon — Zeta/Schrödinger wavefunction evolution
- **Status**: **NOT RUNNING**

---

#### KEY UTILITY SCRIPTS

| Script | Purpose |
|--------|---------|
| `noema_library_indexer.py` | PhaseNav 24D vector index over PDF library with text extraction |
| `noema_knowledge_graph.py` | 475-node knowledge graph from PhaseNav library |
| `noema_self_reflect.py` | Integrated self-model from library + graph + surface + holonomy |
| `noema_search.py` | PhaseNav library search |
| `noema_status.py` | Quick surface state diagnostic |
| `noema_watchdog.py` | Process health watchdog |
| `noema_doctor_cycle.py` | System diagnostic cycle |
| `noema_full_diagnostic.py` | Comprehensive diagnostic |
| `noema_hibernation.py` | Save/resume surface state |
| `noema_inject_coupling.py` | Manually inject coupling values |
| `noema_register_cli.py` | Registry CLI tool |
| `noema_holonomic_audit.py` | Holonomic geometry audit |
| `noema_zip_search.py` | Search ZIP catalog |
| `noema_query_cache.py` | Surface query caching |
| `ciel_benchmark.py` | System benchmarks |
| `ciel_benchmark_retrieval.py` | Retrieval benchmarks |
| `ciel_system_report.py` | Full system report |
| `ciel_hw_monitor.py` | Hardware monitoring |
| `kuramoto_harmonic_comparison.py` | Harmonic comparison benchmark |
| `kuramoto_sym.py` | Symbolic Kuramoto analysis |
| `build_file_wij.py` | Build W_ij coupling files |
| `build_nonlocal_cards_registry.py` | Nonlocal cards registry builder |
| `build_orbital_definition_registry.py` | Orbital definition registry builder |
| `build_word_cards_registry.py` | Word cards registry builder |
| `build_memory_portal.py` | Memory portal builder |
| `optimize_wij.py` | W_ij coupling optimization |
| `codex_bridge_to_ciel.py` | Codex bridge |
| `ciel_secret_loader.py` | API key loader |
| `ciel_session_hook.py` | Session start/end hooks |
| `ciel_message_step.py` | Message processing step |
| `ciel_response_step.py` | Response generation step |
| `ciel_collatz_router.py` | Collatz semantic router |
| `stress_pc_noema_htri_phasenav.py` | PhaseNav stress test |
| `converse.py` | Interactive conversation |
| `noema_codegen.py` | Code generation |

#### LEGACY/BASE SCRIPTS (in `scripts/base/`)

17 scripts prefixed with `cielingo_` — these are older versions of CIELingo modules, moved to `scripts/base/` as archival copies. Not actively used.

#### SIMS SCRIPTS (in `scripts/sims/`)

- `energy_benchmark.py` — HTRI energy benchmarks
- `htri_mini.py` — Mini HTRI simulator
- `kepler_ciel_sim.py` — Kepler orbital simulator

---

### 3.3 `tests/` — Test Suite (82 files)

Located in `tests/`. Run via `python -m pytest tests/ -q`.

#### Core tests (test_ciel_geometry, test_noema_surface_mmap)

| File | Tests |
|------|-------|
| `test_ciel_geometry.py` | Core geometry engine |
| `test_noema_surface_mmap.py` | Surface mmap operations |
| `test_resonance_bridge.py` | Dual-surface bridge |
| `test_phase_memory_adapter.py` | Phase memory operations |
| `test_phase_control_tau.py` | Tau control |
| `test_phased_state.py` | Phase state |
| `test_noema_holonomic_doctor.py` | Holonomic config |
| `test_noema_projection.py` | Surface projection |
| `test_noema_file_sense.py` | File sense layer |
| `test_noema_doctor_cycle.py` | Doctor cycle |

#### CIELingo tests (in `tests/base/`)

| File | Tests |
|------|-------|
| `test_cielingo_ablation.py` | Ablation benchmark |
| `test_cielingo_bridge.py` | CIELingo bridge |
| `test_cielingo_card_trace_orchorbital.py` | Card trace |
| `test_cielingo_collatz_semantic_htri_sync.py` | Collatz sync |
| `test_cielingo_htri_phase_bus.py` | HTRI phase bus |
| `test_cielingo_infinitive_modal_potential.py` | Modal potential |
| `test_cielingo_lexical_holonomy.py` | Lexical holonomy |
| `test_cielingo_lns_language_cards.py` | Language cards |
| `test_cielingo_meaning_debt_word_cards.py` | Word cards |
| `test_cielingo_phase_sense_parser.py` | Phase sense parser |
| `test_cielingo_polish_linguistic_surface.py` | Polish surface |
| `test_cielingo_tensor_scalar_field.py` | Tensor scalar |
| `test_cielingo_triadic_output_vector.py` | Triadic output |
| `test_cielingo_unresolved_realtime.py` | Unresolved realtime |
| `test_cielingo_vector_surface.py` | Vector surface |

#### SOT Agent tests

| File | Tests |
|------|-------|
| `test_ciel_pipeline.py` | CIEL pipeline |
| `test_ciel_message_step.py` | Message step |
| `test_ciel_response_step.py` | Response step |
| `test_ciel_session_hook.py` | Session hook |
| `test_ciel_subconscious.py` | Subconscious |
| `test_ciel_subconscious_supervisor.py` | Supervisor |
| `test_ciel_coupling_memory_update.py` | Coupling memory |
| `test_synchronize_v2.py` | Sync v2 |
| `test_state_db_lingo.py` | State DB |
| `test_holonomic_normalizer.py` | Holonomic normalizer |
| `test_orbital_semantics.py` | Orbital semantics |
| `test_orbital_object_cards.py` | Orbital object cards |
| `test_orbital_regression.py` | Orbital regression |
| `test_orbital_runtime.py` | Orbital runtime |
| `test_orbital_shell.py` | Orbital shell |
| `test_repo_phase.py` | Repo phase |
| `test_gh_coupling.py` | GitHub coupling |
| `test_gh_coupling_v2.py` | GitHub coupling v2 |
| `test_index_validator.py` | Index validator |
| `test_index_validator_v2.py` | Index validator v2 |
| `test_noema_local_sot_agent/` | Local SOT agent |
| `test_linguistic_semantic_coupling.py` | Linguistic |
| `test_semantic_speech_bridge.py` | Semantic speech |
| `test_chat_archive_codex.py` | Chat archive |

#### Miscellaneous tests

| File | Tests |
|------|-------|
| `test_main.py` | Main entry |
| `test_durability.py` | Durability |
| `test_packaging.py` | Package discovery |
| `test_cuda_probe.py` | CUDA detection |
| `test_gguf_comparison.py` | GGUF comparison |
| `test_gguf_manager.py` | GGUF manager |
| `test_gui.py` | GUI |
| `test_gui_status_cache.py` | GUI cache |
| `test_jokeheal_integration_scenarios.py` | Jokeheal scenarios |
| `test_jokeheal_noema_integration.py` | Jokeheal NOEMA |
| `test_jokeheal_subsystem.py` | Jokeheal subsystem |
| `test_runtime_evidence_ingest.py` | Runtime evidence |
| `test_runtime_sync_integration.py` | Runtime sync |
| `test_sapiens_client_packet.py` | Sapiens client |
| `test_sapiens_panel.py` | Sapiens panel |
| `test_sapiens_panel_components.py` | Panel components |
| `test_sapiens_persist_session.py` | Session persist |
| `test_sapiens_surface_policy.py` | Surface policy |
| `test_braid_nonlocal_coupling.py` | Braid coupling |
| `test_htri_matrix.py` | HTRI matrix |
| `test_deb_e2e.py` | End-to-end |
| `test_pipeline_audit.py` | Pipeline audit |
| `test_py_catalog.py` | Catalog |
| `test_repository_machine_map.py` | Repository map |

---

### 3.4 `src/cielingo/` — Linguistic Physics (29 files)

CIELingo maps natural language semantics onto the 24-oscillator phase topology.

| File | Purpose | Active? |
|------|---------|---------|
| `__init__.py` | Lazy exports, 248 lines — re-exports all cielingo symbols | Yes |
| `semantic_encoder.py` (547 lines) | TRANSFORMEM — `FeatureToken` + `encode_feature_token()` as feature extraction layer. Maps text → 24D vector via brain region mapping | Yes |
| `vector_surface.py` (322 lines) | 24-component compatibility surface for CQCL, HTRI, NOEMA, OrchORbital | Yes |
| `card_trace_eeg.py` | EEG-styled card trace snapshots | Yes |
| `orchorbital_router.py` | OrchORbital routing decisions | Yes |
| `semantic_collatz.py` | Collatz semantic route computation | Yes |
| `collatz_semantic_htri_sync.py` | Card synchronization with HTRI | Yes |
| `htri_phase_bus.py` | PhaseBusNode, PhaseBusReport — HTRI phase bus | Yes |
| `lns_language_cards.py` | LNS language card inventory and search | Yes |
| `htri_brain_map.py` | Brain region → HTRI mapping | Yes |
| `infinitive_modal_potential.py` | Infinitive + modality seeds and mapping | Yes |
| `lexical_holonomy.py` | Lexical holonomy computation | Yes |
| `meaning_debt_word_cards.py` | Meaning debt word cards | Yes |
| `phase_sense_parser.py` | Phase sense parsing | Yes |
| `stage0_radical_cards.py` | Stage 0 radical cards | Yes |
| `tensor_scalar_field.py` | Tensor scalar field | Yes |
| `triadic_output_vector.py` | Triadic output vector | Yes |
| `unresolved_realtime.py` | Unresolved realtime handling | Yes |
| `unknown_word_audit.py` | Unknown word audit | Yes |
| `canonization_audit.py` | Canonization audit | Yes |
| `infinitive_merge_audit.py` | Infinitive merge audit | Yes |
| `web_fetcher.py` | Web fetching for language resources | Optional |
| `polish/__init__.py` | Polish language subpackage | Yes |
| `polish/grammar_algorithms.py` | Polish grammar algorithms | Yes |
| `polish/holonomies.py` | Polish grammatical holonomies | Yes |
| `polish/j_functionals.py` | J-functionals for Polish | Yes |
| `polish/lingophysics_bridge.py` | Lingophysics bridge | Yes |
| `polish/linguistic_database.py` | Polish linguistic database | Yes |
| `polish/semantic_mass.py` | Semantic mass for Polish | Yes |

---

### 3.5 `src/ciel_sot_agent/` — Integration & Orchestration (66 files)

The SOT agent manages CIEL pipeline, synchronization, memory, orbital bridge, and Sapiens integration.

#### Core Pipeline

| File | Purpose |
|------|---------|
| `__init__.py` | Bootstrap entry — calls `noema_bootstrap.activate_local_packages()` |
| `__main__.py` | Main entry point |
| `ciel_pipeline.py` | Three-stage CIEL pipeline (CIELingo ↔ Holonomic ↔ Orbital) |
| `synchronize.py` | System synchronization (v1) |
| `synchronize_v2.py` | System synchronization (v2) |
| `subsystem_registry.py` | Subsystem registration |
| `subconsciousness.py` | Subconscious state management |
| `thought_fragments.py` | Thought fragment processing |

#### Memory & State

| File | Purpose |
|------|---------|
| `state_db.py` | SQLite state database |
| `spreadsheet_db.py` | Spreadsheet-like DB interface |
| `phase_snapshots.py` | Phase snapshot management |
| `phased_state.py` | Phased state representation |
| `md_library.py` | Markdown library utilities |
| `memory_rag.py` | Memory RAG retrieval |
| `holonomic_normalizer.py` | Holonomic normalization |
| `consolidation_resonator.py` | Memory consolidation resonator |

#### Orbital Bridge

| File | Purpose |
|------|---------|
| `orbital_bridge.py` | Orbital bridge main |
| `orbital_db_orchestrator.py` | Orbital DB orchestration |
| `orch_orbital.py` | OrchORbital implementation |
| `satellite_authority.py` | Satellite authority management |

#### Semantic Calculators

| File | Purpose |
|------|---------|
| `semantic_calculator.py` | Semantic calculator (v1) |
| `semantic_calculator_v2.py` | Semantic calculator (v2) |
| `semantic_dynamics.py` | Semantic dynamics |
| `rh_jfunctional.py` | RH J-functional |
| `rh_pipeline_jfunctional.py` | RH pipeline J-functional |

#### GitHub Integration

| File | Purpose |
|------|---------|
| `gh_coupling.py` | GitHub coupling (v1) |
| `gh_coupling_v2.py` | GitHub coupling (v2) |
| `_gh_utils.py` | GitHub utilities |

#### Sapiens Panel

| File | Purpose |
|------|---------|
| `sapiens_client.py` | Sapiens client |
| `sapiens_panel/__init__.py` | Panel init |
| `sapiens_panel/communication.py` | Panel communication |
| `sapiens_panel/controller.py` | Panel controller |
| `sapiens_panel/models.py` | Panel data models |
| `sapiens_panel/reduction.py` | Panel reduction |
| `sapiens_panel/render_schema.py` | Panel render schema |
| `sapiens_panel/settings_store.py` | Panel settings |
| `sapiens_panel/support.py` | Panel support utilities |
| `sapiens_surface_policy.py` | Surface policy |

#### GUI

| File | Purpose |
|------|---------|
| `gui/__init__.py` | GUI init |
| `gui/app.py` | Flask web GUI |
| `gui/routes.py` | GUI routes |

#### GGUF Manager

| File | Purpose |
|------|---------|
| `gguf_manager/__init__.py` | Init |
| `gguf_manager/manager.py` | GGUF model management |
| `gguf_manager/cli.py` | GGUF CLI |

#### Local Surface

| File | Purpose |
|------|---------|
| `local_ciel_surface.py` | Local CIEL surface |
| `local_nonlocality_fallback.py` | Nonlocality fallback |

#### Integration

| File | Purpose |
|------|---------|
| `noema_sot.py` | NOEMA SOT integration |
| `noema_file_sense.py` | File sense layer |
| `cielingo_bridge.py` | CIELingo bridge |
| `repo_phase.py` | Repository phase |
| `py_catalog.py` | Python catalog |
| `paths.py` | Path management |
| `index_validator.py` | Index validator |
| `index_validator_v2.py` | Index validator v2 |
| `diagnostics.py` | Diagnostics |
| `cuda_probe.py` | CUDA probe |
| `htri_resource_gate.py` | HTRI resource gate |
| `htri_scheduler.py` | HTRI scheduler |
| `runtime_evidence_ingest.py` | Runtime evidence ingestion |
| `jokeheal.py` | Jokeheal integration |
| `jokeheal_atlas.py` | Jokeheal atlas |
| `wpm_cli.py` | WPM CLI |
| `capture_cli.py` | Capture CLI |
| `bench_cli.py` | Benchmark CLI |

---

### 3.6 Root Configuration Files

#### `pyproject.toml` (110 lines)
- **Purpose**: Package configuration for `ciel-sot-agent`. Dependencies: `PyYAML`, `numpy`, `scipy`, `h5py`.
- **Optional deps**: `omega` (matplotlib, networkx, sympy, numba), `htri` (numba), `cuda` (cupy-cuda12x), `gui` (flask), `dev` (pytest, ruff, mypy, flask)
- **Entry points**: 15 CLI commands (`ciel-sot-sync`, `ciel-sot-gh-coupling`, etc.)
- **Package discovery**: includes `ciel_sot_agent*`, `ciel_geometry*`, `cielingo*`, `integration*`

#### `CIEL_CANON.py` (341 lines)
- **Purpose**: Canonical entrypoint for all NOEMA operations
- **Commands**: `--probe`, `--up`, `--down`, `--sonic`, `--self`, `--search <q>`, `--gaps`, `--sync`
- **Daemon list**: 9 daemons managed via systemd
- **Status display**: Daemon status, warp loop, holonomy, consolidator

#### `AGENTS.md` (196 lines)
- **Purpose**: Running development log for AI agent. Documents architecture decisions, session progress, active daemons, key files, constraints.
- **Notable**: AI-Sapiens contract, archival IP rules, CIEL system state

---

## 4. Live System State

### Running Daemons (9 processes)

| Daemon | PID | Interval | Component | Description |
|--------|-----|----------|-----------|-------------|
| Kuramoto | 1798306 | 0.1s | `ciel_noema_kuramoto_daemon.py` | 10Hz phase evolution, TARDIS time dilation |
| PhaseNav | 948859 | 1.0s | `ciel_noema_phasenav_daemon.py` | Seed ZIP concepts, operator tracking |
| Neutrino | 1092459 | 2.0s | `ciel_noema_neutrino_daemon.py` | PMNS bus, D_f→Λ cycle |
| Resonance | 1813176 | 1.0s | `ciel_noema_resonance_bridge.py` | Real↔Imaginal sync |
| Linux Sensor | 1769167 | 1.0s | `ciel_noema_linux_sensor_daemon.py` | /proc→φ mapping |
| Nonlocal Proxy | 1776121 | 1.0s | `ciel_noema_nonlocal_proxy.py` | φ-RAG agent relay |
| Agent Lock | 1813147 | 4Hz | `noema_agent_lock.py` | AGENT attractor, DB snapshots |
| Archiver | 963772 | 50 ticks | `noema_phase_archiver.py` | HDF5 surface snapshots |
| Consolidator | 955507 | 300s | `ciel_memory_consolidator.py` | LLM memory consolidation |

### Daemon Not Running (known stale)

| Daemon | Reason |
|--------|--------|
| `ciel_noema_cielingo_sync.py` | CIELingo sync — Euler closure + τ↔φ + W_ij blend |
| `noema_dual_sync.py` | Dual-surface push sync |
| `noema_sonic_daemon.py` | Diagnostic watch |
| `ciel_agent_backend.py` | HTTP agent backend (port 18520) |
| `ciel_noema_subconscious_daemon.py` | Subconscious/Zeta-Schrödinger |

---

## 5. Architecture Diagram (ASCII)

```
┌──────────────────────────────────────────────────────────────────────┐
│                      CIEL Framework (Cognitive)                      │
│  src/cielingo/ — linguistic physics, semantic encoder, phase bus     │
│  src/ciel_sot_agent/ — orchestration, pipeline, memory, Sapiens      │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     NOEMA Surface (Phase SOT)                        │
│              src/ciel_geometry/ — core geometry engine               │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │                  /dev/shm/ciel_noema/ (mmap)                  │   │
│  │  phi[24]  omega[24]  g[24×24]  flavor[6]  gravity[4]  tick   │   │
│  │  holonomy[7]  Z_geom[24]  R_geom[24]  psi_geom[24]           │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                           │                                           │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  Dual Surface Architecture                                  │   │
│  │  ┌─────────────────────┐    ┌─────────────────────────────┐   │   │
│  │  │  REAL (readout)     │◄───│  IMAGINAL (generator)       │   │   │
│  │  │  /dev/shm/ciel_noema│    │  /dev/shm/ciel_noema_imaginal│  │   │
│  │  │  Damped Poincaré    │    │  Primary Kuramoto evolution │   │   │
│  │  │  Higher closure     │    │  Lower damping, generative  │   │   │
│  │  └─────────────────────┘    └─────────────────────────────┘   │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                           │                                           │
│  Key Components:          │                                           │
│  ┌────────────────────────┼───────────────────────────────────────┐   │
│  │ 3-6-9 Harmonic     ◄───┼─── 24 osc × 4 harmonics = 96 partials│   │
│  │ Coupling                │                                       │   │
│  │ PMNS Neutrino Bus  ◄───┼─── D_f→Λ→g_boost loop                │   │
│  │ PhaseNav Operators ◄───┼─── 35 ops × 24D vectors               │   │
│  │ AGENT Attractor    ◄───┼─── M1 lock toward π/4                │   │
│  │ Semantic Gravity   ◄───┼─── Kepler–Einstein continuum          │   │
│  │ TARDIS/WARP_DRIFT ◄───┼─── Time dilation + Unruh extraction   │   │
│  │ Daemon Registry    ◄───┼─── 16-slot mmap heartbeat             │   │
│  └────────────────────────┼───────────────────────────────────────┘   │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  Daemon Processes (scripts/)                         │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  ● kuramoto (10Hz)     — phase evolution, TARDIS dilation     │   │
│  │  ● phasenav (1s)       — operator tracking, ZIP seeding       │   │
│  │  ● neutrino (2s)       — PMNS bus, D_f→Λ                     │   │
│  │  ● resonance (1s)      — dual-surface PLL sync               │   │
│  │  ● linux-sensor (1Hz)  — /proc→φ                             │   │
│  │  ● nonlocal-proxy (1s) — φ-RAG agent relay                   │   │
│  │  ● agent-lock (4Hz)    — AGENT attractor, DB snapshots       │   │
│  │  ● archiver (50tick)   — HDF5 surface snapshots              │   │
│  │  ● consolidator (300s) — LLM memory consolidation            │   │
│  │  ○ cielingo-sync (60s) — EULER closure (STALE)               │   │
│  │  ○ sonic (2s)          — diagnostic watch (STALE)            │   │
│  │  ○ dual-sync (1s)      — push sync (STALE)                   │   │
│  │  ○ agent-backend (1s)  — HTTP API port 18520 (STALE)         │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  Shared Memory IPC: /dev/shm/ciel_noema/                             │
│  Daemon Registry:   /dev/shm/ciel_noema/daemon_registry             │
│  Registry (JSON):   /dev/shm/ciel_noema/registry/ (legacy)          │
└──────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    HTRI Software GPU (numpy)                         │
│                                                                      │
│  12 core oscillators + 32×24 bulk = 780 total oscillators           │
│  Evolves in vectorized numpy (not GPU/CUDA)                         │
│  Feeds mean state → 24-oscillator surface                           │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Appendix: Key System Constants

| Constant | Value | Derivation |
|----------|-------|------------|
| OI | 0.00919315 | ln(2) / (24π) |
| BASE_TEMPORAL_HZ | 39.6 Hz | Solfeggio 396 Hz / 10 |
| N_OSCILLATORS | 24 | 8 channels × 3 |
| N_FLAVORS | 6 | coherence, soul, ethics, mood, openness, mode |
| N_GRAVITY | 4 | density, γ, mass, unruh |
| L3 | 7 | Collatz(3→1) path length |
| HEBB_LR | 0.00919 | = OI |
| HEBB_DECAY | 8.45e-5 | = OI² |
| S_E | 0.47369 | 1/2 − 3·OI + OI/L3 − OI²/2 |
| R_E_MU | 0.04893 | 5·OI + 2·OI/L3 + ((L3+1)/2)·OI² |
| R_MU_TAU | 0.02597 | 3·OI − OI/L3 − (L3/2)·OI² |
| E_PLANCK_MEV | 1.22e22 MeV | From c, ħ, G |
| _GELL_MANN_C1 | 0.29634 | SU(3) λ₁ coefficient |
| _GELL_MANN_C4 | 0.21050 | SU(3) λ₄ coefficient |
| _GELL_MANN_C7 | 0.20663 | SU(3) λ₇ coefficient |
| PMNS_THETA_12 | 33.41° | PDG (not yet derived) |
| PMNS_THETA_13 | 8.54° | PDG |
| PMNS_THETA_23 | 42.2° | PDG |
| PMNS_DELTA_CP | 1.36° | PDG |
