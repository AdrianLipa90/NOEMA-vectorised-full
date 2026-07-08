# NOEMA / CIEL — Python API Reference

This document covers the public Python API of each package. All packages depend only on numpy (except where noted). Internal/private functions (prefixed with `_`) are not documented here.

---

## Package: `ciel_geometry`

Core oscillator engine. Shared-memory surface protocol, Kuramoto evolution, resonance bridge, neutrino bus, Linux sensor, PhaseNav operator algebra.

### Surface Management

```python
from ciel_geometry.noema_surface_mmap import (
    ensure_surface,
    open_surface,
    read_surface_state,
    write_surface_state,
    evolve_surface,
    evolve_imaginal_surface,
    update_coupling_matrix,
    clear_surface,
    flush_surface,
    compute_zpe,
    sync_surface_geometry,
    seed_neutrino_mixing,
)
```

#### `ensure_surface(path="/dev/shm/ciel_noema")`
Create the surface directory and all binary files (`phi`, `omega`, `g`, `flavor`, `tick`, `Z_geom`, `psi_geom`, `R_geom`) if they do not exist. Initializes phases to random values in `[0, 2π)`, frequencies to `BASE_TEMPORAL_HZ ± noise`, coupling matrix `g` to a Gell-Mann-based SU(3) block structure. Safe to call multiple times — no-ops if surface already exists.

**Returns:** `None`

#### `open_surface(path="/dev/shm/ciel_noema")`
Open all surface files in `r+b` mode. Returns a dict of `{name: file_object}`. Each daemon should call this once at startup and keep the handles.

**Returns:** `dict[str, BinaryIO]`

#### `read_surface_state(surface=None, path="/dev/shm/ciel_noema")`
Read the complete surface state into a Python dict. If `surface` dict is provided (from `open_surface()`), reads from the open file handles; otherwise reads from disk.

**Returns:** `dict` with keys:
- `phi` — `list[float]` length 24, phases in `[0, 2π)`
- `omega` — `list[float]` length 24, frequencies in Hz
- `g` — `list[float]` length 576 (24×24 row-major), coupling matrix
- `flavor` — `list[float]` length 6: `[cpu_coherence, mem_pressure, io_wait, load_mood, lambda_cosmo, D_f]`
- `tick` — `int`, iteration counter (uint64)
- `Z_geom` — `list[float]` length 24, geometric phase in `[-π, π]`
- `psi_geom` — `list[float]` length 24, wavefunction magnitude in `[0, 1]`
- `R_geom` — `list[float]` length 24, geometric radius

#### `write_surface_state(state, surface=None, path="/dev/shm/ciel_noema")`
Write a state dict back to the surface files. Validates key names and array lengths. Calls `os.fsync()` on each file handle after writing.

**Raises:** `ValueError` if any array has wrong length.

#### `evolve_surface(surface=None, dt=0.05, steps=1, flush=True)`
Run one or more RK4 integration steps of the Kuramoto system on the 24 oscillators. The evolution uses:

- 3-6-9 harmonic coupling per oscillator (mask `H[i]` mapping to `{1, 3, 6, 9}` with weights `[1.0, 0.5, 0.33, 0.25]`)
- Gell-Mann SU(3) coupling matrix `g[i,j]`
- Base temporal frequency `BASE_TEMPORAL_HZ = 39.6` (Solfeggio 396 Hz / 10)
- Hebbian learning on `g` at each step (delta = `η · cos(φ_j - φ_i)`)

**Parameters:**
- `dt` — integration timestep in seconds (default 0.05)
- `steps` — number of RK4 steps (default 1)
- `flush` — if True, call `flush_surface()` after evolution

**Returns:** `float` — thinking delta `δΦ = mean(|φ_new - φ_old|)` over all oscillators

#### `evolve_imaginal_surface(surface=None, dt=0.05, steps=1, flush=True)`
Same as `evolve_surface()` but operates on the imaginal surface files (`Z_geom`, `psi_geom`, `R_geom`). Used by the resonance bridge. The imaginal surface has lower damping and acts as the primary generator.

#### `update_coupling_matrix(g_new, surface=None)`
Replace the `g` coupling matrix with a new 24×24 array. Used by the CIELingoSync daemon after W_ij PMNS blend.

**Parameters:**
- `g_new` — `np.ndarray` shape `(24, 24)` or flat list of 576 floats

**Raises:** `ValueError` if shape is not `(24, 24)`.

#### `clear_surface(path="/dev/shm/ciel_noema")`
Reset all phases to random values, frequencies to `BASE_TEMPORAL_HZ ± uniform(-0.5, 0.5)`, coupling to base SU(3) matrix. Resets tick to 0.

#### `compute_zpe(phi, omega, g)`
Compute the Zero-Point Energy (ZPE) of the oscillator system. Returns a scalar float in arbitrary units. Used by the orbital bridge for energy accounting.

```python
zpe = sum(0.5 * omega[i]**2) + 0.5 * sum(g[i,j] * cos(phi[j] - phi[i]))
```

#### `sync_surface_geometry()`
Recalculate `Z_geom`, `psi_geom`, `R_geom` from the current `phi`, `omega`, `g`. Called periodically by the resonance bridge.

#### `seed_neutrino_mixing(flavor_out=None)`
Seed the neutrino mixing from the current flavor state. If `flavor_out` is provided, writes it to the flavor file; otherwise computes from the current `phi` and `g`.

---

### Resonance Bridge

```python
from ciel_geometry.resonance_bridge import (
    ensure_dual_surfaces,
    dual_surface_step,
    resonance_snapshot,
    read_imaginal_surface,
    project_imaginal_to_real,
)
```

#### `ensure_dual_surfaces(path="/dev/shm/ciel_noema")`
Create or open both the real surface (`phi`, `omega`, `g`, `tick`, `flavor`) and the imaginal surface (`Z_geom`, `psi_geom`, `R_geom`). Returns a tuple of two surface dicts `(real_surface, imaginal_surface)`.

#### `dual_surface_step(surface_real, surface_imaginal, dt=0.05)`
Run one dual-surface cycle:
1. Read CIEL state from both surfaces
2. Evolve imaginal surface (primary generator, low damping)
3. Project imaginal → real surface (damped readout, high closure)
4. Compute resonance coherence metric

**Returns:** `dict` with keys `coherence`, `phase_lock`, `imaginal_drive`, `closure`

#### `resonance_snapshot(surface_real, surface_imaginal)`
Read both surfaces and compute resonance diagnostics: coherence between real and imaginal phase vectors, phase locking value (PLV), and imaginal drive magnitude.

**Returns:** `dict` with `coherence` (Pearson `r`), `plv` (phase locking value), `imaginal_magnitude` (mean `|psi_geom|`)

#### `read_imaginal_surface(surface=None)`
Read `Z_geom`, `psi_geom`, `R_geom` from the surface.

**Returns:** `dict` with keys `Z_geom`, `psi_geom`, `R_geom` (each `list[float]` length 24)

#### `project_imaginal_to_real(imaginal_state, damping=0.3)`
Project an imaginal state dict onto the real surface. The projection applies damping: `phi_real = phi_imaginal * (1 - damping) + noise`. Returns a dict suitable for `write_surface_state()`.

---

### Neutrino Channel

```python
from ciel_geometry.neutrino_phase_channel import (
    compute_neutrino_phase_bus,
    D_f_to_lambda,
    phi_to_epsilon,
    apply_neutrino_bus_to_surface,
    pmns_mix,
    compute_lambda,
    compute_tau_modulation,
)
```

#### `compute_neutrino_phase_bus(phi, g, omega, flavor, D_f)`
Compute the full PMNS neutrino mixing bus from the current surface state.

**Parameters:**
- `phi` — 24 phases
- `g` — 24×24 coupling matrix
- `omega` — 24 frequencies
- `flavor` — 6 flavor channels (list or array)
- `D_f` — fractal dimension (scalar)

**Returns:** `dict` with `bus` (8 channels × 3 flavors), `mixing_angles`, `epsilon_matrix`

#### `D_f_to_lambda(D_f)`
Convert fractal dimension `D_f` to cosmological constant Λ.

```
Λ = (D_f - 2.0) / 0.57
```

**Returns:** `float`

#### `phi_to_epsilon(phi_i, phi_j)`
Compute the PMNS mixing angle from a phase difference. Used internally by `compute_neutrino_phase_bus`.

```
epsilon_ij = arcsin(sin(phi_j - phi_i))
```

#### `apply_neutrino_bus_to_surface(bus, surface=None)`
Write the neutrino bus results to the surface: updates `flavor[4]` (Λ) and `flavor[5]` (D_f), and boosts the `g` coupling matrix.

#### `compute_tau_modulation(R, tau_base=0.353)`
Compute τ (temporal coherence) adjustment from Euler residual `R`:
```
tau_adj = tau_base + 0.05 * R * cos(phi_target - phi_i) - 0.02 * (tau - 0.353)
```
**Returns:** `float` clipped to `[0.01, 1.0]`

---

### Linux Sensor

```python
from ciel_geometry.linux_sensor import LinuxSensor
```

#### `LinuxSensor(smoothing=0.3)`

**Constructor:**
- `smoothing` — EMA smoothing factor for `/proc` readings (default 0.3)

**Attributes:**
- `SYSTEM_OSC_MAP` — dict mapping oscillator indices to system metrics:
  - `0–7`: CPU core utilization (from `/proc/stat`)
  - `8–15`: Memory pressure (from `/proc/meminfo`)
  - `16–18`: Load average (from `/proc/loadavg`)
  - `19–20`: Process count (from `/proc/loadavg`)
  - `21–22`: Context switches (from `/proc/stat`)
  - `23`: Entropy availability (from `/proc/sys/kernel/random/entropy_avail`)
- `FLAVOR_MAP` — dict mapping flavor index to derived metric:
  - `0`: cpu_coherence (1 - std(CPU utilizations))
  - `1`: mem_pressure (ratio of used/total memory)
  - `2`: io_wait (from `/proc/stat`)
  - `3`: load_mood (scaled load average)
  - `4`: entropy_open (log-normalized entropy)
  - `5`: sys_mode (derived mode classification)

**Methods:**

```python
snapshot() -> dict
```
Read all `/proc` sources and compute 24 phases `phi[0..23]` in `[0, 2π)`, 6 flavor values `flavor[0..5]`, and frequency estimate `omega` from the first derivative of each channel.

```python
write_surface(surface=None) -> None
```
Call `snapshot()` and write the results to the NOEMA surface files.

```python
process_phasenav(n_top=1) -> dict
```
Compute PhaseNav operator matching for the current snapshot. Returns the best-matching operator from the 33-operator algebra, its harmonic fingerprint (e.g. `"HHHH"`, `"LHLL"`), cosine similarity score, and thinking delta `δΦ`.

```python
top_processes(n=5) -> list[dict]
```
Read `/proc` for top CPU-consuming processes. Returns a list of dicts with `pid`, `name`, `cpu_percent`, and a PhaseNav enrichment string `(pid:{PID} → operator)`.

---

### PhaseNav

```python
from ciel_geometry.phasenav import (
    OperatorAlgebra,
    TeleusingSolver,
    SurfaceBridge,
)
```

#### `OperatorAlgebra`

Class holding the 33 universal operators, each a deterministic 24D vector.

```python
op = OperatorAlgebra()
op.vectors          # dict[str, np.ndarray] — 33 entries
op.names            # list[str] — operator names

op.match(query_vec: np.ndarray) -> tuple[str, float]
```
Match a query 24D phase vector to the nearest operator by cosine similarity. Returns `(operator_name, similarity_score)`.

#### `TeleusingSolver`

Solve the Euler identity constraint `Σe^{iφ} = 0` for a subset of oscillators.

```python
solver = TeleusingSolver()
solver.solve(phi: np.ndarray) -> np.ndarray
```
Adjust phases to satisfy the Euler closure constraint while minimizing displacement from the input.

#### `SurfaceBridge`

Bridge between the NOEMA surface and the PhaseNav operator algebra.

```python
bridge = SurfaceBridge()
bridge.surface_to_operator(surface=None) -> tuple[str, float, np.ndarray]
```
Read current surface state, compute operator match. Returns `(operator_name, similarity, phi_vector)`.

---

### Registry

```python
from ciel_geometry.noema_registry import registry
```

#### `registry.register(name, claims=None)` -> str
Register a daemon with the NOEMA registry. Returns a unique token string.

**Parameters:**
- `name` — daemon name (e.g. `"kuramoto"`)
- `claims` — list of surface files this daemon writes to (e.g. `["phi", "omega", "g", "tick"]`)

#### `registry.heartbeat(token)` -> bool
Send a heartbeat to keep the registration alive. Returns True if still registered.

#### `registry.unregister(token)` -> bool
Unregister a daemon. Called on graceful shutdown.

#### `registry.list_active(timeout=30)` -> list[dict]
List all daemons that have sent a heartbeat within `timeout` seconds. Each entry contains `name`, `claims`, `pid`, `last_heartbeat`, `registered_at`.

#### `registry.check_access(token, file)` -> bool
Check if a daemon token has write access to a given surface file.

#### `registry.cleanup()` -> int
Remove stale registrations (heartbeat older than 60 seconds). Returns the number of cleaned entries.

---

## Package: `ciel_sot_agent`

Integration kernel. Connects NOEMA geometry with CIELingo phase topology, orbital manifold, and relational contract.

```python
from ciel_sot_agent import (
    synchronize,
    orbital_bridge,
    ciel_pipeline,
    state_db,
    cielingo_bridge,
    thought_fragments,
    subconsciousness,
    htri_scheduler,
    htri_resource_gate,
    subsystem_registry,
    synchronize_v2,
)
```

### `synchronize`

Full system synchronization cycle. Called by `ciel_noema_cielingo_sync.py` every 60 seconds.

```python
synchronize.run_full_cycle() -> dict
```

Returns a dict with `closure_defect`, `ethical_score`, `health`, `phase`, `emotion`, and a list of `actions` taken during the cycle.

### `orbital_bridge`

Constructs and manages the orbital manifold — a 15-dimensional relational space (Lie₄ × intention field).

```python
orbital_bridge.build_manifold() -> dict
orbital_bridge.project_to_orbital(state: dict) -> dict
orbital_bridge.relational_map() -> dict
```

`relational_map()` returns the entity-coupling graph shown in the CIEL system state: each entity has a name, coupling strength, and role description.

### `ciel_pipeline`

CIEL/Omega consciousness pipeline. Three-stage processing: phase encoding → holonomic retrieval → response generation.

```python
ciel_pipeline.run(input_text: str) -> dict
```

Returns a dict with `encoded_phases`, `retrieved_memories`, `generated_response`, `bloch_state`.

### `state_db`

SQLite persistence for orchestrator state, metrics history, and system snapshots.

```python
state_db.save_metrics(cycle: int, metrics: dict)
state_db.get_history(n: int = 10) -> list[dict]
state_db.get_latest() -> dict
state_db.get_latest_tick() -> int
```

### `cielingo_bridge`

Bridge between CIELingo linguistic topology and the NOEMA surface.

```python
from ciel_sot_agent.cielingo_bridge import (
    build_lingo_frame,
    process_user_input,
    get_ciel_state,
)
```

#### `build_lingo_frame(text: str, fast=False) -> dict`
Full CIELingo processing pipeline: card trace → phase bus → brain topology → meaning debt → triadic output.

If `fast=True`, skips the meaning debt computation and orbital bridge projection.

**Returns:** dict with keys `tokens`, `phases`, `coherence`, `emotion`, `ethical_score`, `triadic`, `meaning_debt`.

#### `process_user_input(text: str, enrich=True) -> dict`
User text → enriched state dict. If `enrich=True`, also runs PhaseNav operator matching and updates the CIEL state file at `NOEMA/state/ciel_state.json`.

#### `get_ciel_state() -> dict`
Return the last known CIEL state from the state file. If the file is missing, returns a default state with `closure_defect=1.0`, `ethical_score=0.5`, `health=0.5`.

### `thought_fragments`

Fragment assembly and subconscious triage.

```python
thought_fragments.assemble(fragments: list) -> dict
thought_fragments.triage() -> list
```

### `subconsciousness`

Subconscious layer implementing Zeta/Schrödinger anti-collapse dynamics.

```python
subconsciousness.process(state: dict) -> dict
subconsciousness.get_zeta_potential() -> float
```

### `htri_scheduler` / `htri_resource_gate`

HTRI resource scheduling and access gating for the 24 oscillators.

```python
htri_scheduler.schedule_cycle(resources: dict) -> dict
htri_resource_gate.check_access(channel: int, token: str) -> bool
```

### `subsystem_registry`

Central registry for all CIEL subsystems.

```python
subsystem_registry.register(name, version, deps=[])
subsystem_registry.list_subsystems() -> list[dict]
subsystem_registry.check_dependencies(name) -> list[str]
```

### `synchronize_v2`

Enhanced sync cycle with τ↔φ feedback, W_ij PMNS blend, and orchestrator integration.

```python
synchronize_v2.run_cycle(cycle: int) -> dict
```

---

## Package: `cielingo`

Linguistic topology engine for Polish. Maps words and sentences to 24D phase vectors.

```python
from cielingo import (
    encode,
    card_trace,
    build_phase_bus,
    brain_phase_topology,
    get_meaning_debt,
    canonize_text,
    CIELingo,
)
```

### `encode(text: str) -> EncodeResult`

Encode Polish text into phase tokens. Returns an `EncodeResult` with:
- `tokens` — list of `(word, oscillator_index, phi)` tuples
- `phases` — 24D phase vector `np.ndarray`
- `confidence` — float in `[0, 1]`
- `unresolved` — list of words not in the card registry

### `card_trace(text: str) -> list[dict]`

Trace each word through the Stage 0 radical card database. Returns a list of per-card snapshots with `word`, `card_id`, `phase`, `energy`, `resonance`.

### `build_phase_bus() -> dict`

Build the HTRI bus report: 8 channels × 3 oscillators = 24 buses. Each channel reports phase coherence, tension, and alignment.

### `brain_phase_topology() -> dict`

Return the oscillator-to-brain-region mapping:
- M0 (0–2): Perception
- M1 (3–5): Episodic
- M2 (6–8): Procedural
- M3 (9–11): Semantic
- M4 (12–14): Affective
- M5 (15–17): Identity
- M6 (18–20): Narrative
- M7 (21–23): Braid / cross-harmonic hub

### `get_meaning_debt() -> list[dict]`

Return a list of unresolved semantic tensions between oscillator pairs. Each entry has `source`, `target`, `debt` (float), and `phase_gap`.

### `canonize_text(text: str) -> dict`

Validate that every word in the text has a card entry. Returns `known`, `unknown`, and `coverage` (fraction of known words).

### `CIELingo` class

```python
cielingo = CIELingo()
cielingo.process(text: str) -> dict   # Full pipeline
cielingo.reset()                       # Clear internal state
```

---

## Package: `scripts` (Standalone CLIs)

These modules in `scripts/` provide command-line interfaces and are run directly with `python3 scripts/<name>.py`.

### `ciel_coupling.py` — opencode integration

```python
from scripts.ciel_coupling import process_user_input, get_ciel_state
```

- `process_user_input(text)` — Direct text → state dict with emotion, ethics, phase, coherence
- `get_ciel_state()` — Returns last processed CIEL state

### `noema_register_cli.py` — Registration CLI

```bash
python3 scripts/noema_register_cli.py list
python3 scripts/noema_register_cli.py register <name> [--claims FILE...]
python3 scripts/noema_register_cli.py unregister <token>
python3 scripts/noema_register_cli.py check <token> <file>
```

### `ciel_memory_consolidator.py` — Background consolidation

```python
from scripts.ciel_memory_consolidator import CIELMemoryConsolidator

consolidator = CIELMemoryConsolidator(backend="local")
consolidator.consolidate(memory_payload: dict) -> dict
```

### `ciel_monitor.py` — Curses UI

```bash
python3 scripts/ciel_monitor.py
```

Live curses display of all 24 oscillator phases, flavor channels, tick, and daemon heartbeats. Press `q` to quit.

---

## Constants

Defined in `ciel_geometry.noema_surface_mmap`:

| Constant | Value | Meaning |
|----------|-------|---------|
| `BASE_TEMPORAL_HZ` | `39.6` | Solfeggio 396 Hz / 10 |
| `NUM_OSCILLATORS` | `24` | HTRI oscillators |
| `SURFACE_PATH` | `"/dev/shm/ciel_noema"` | Default shared-memory path |
| `OI` | `1.5` | Orbital inclination constant |
| `L3` | `0.577` | Third Love number (tidal) |
| `HARMONIC_MASK` | `{0:[1,3], 1:[1,6], 2:[1,9], 3:[3,6], 4:[3,9], 5:[6,9], 6:[1,3,6], 7:[1,3,6,9]}` | Harmonic sets per memory channel |
| `HARMONIC_WEIGHTS` | `{1:1.0, 3:0.5, 6:0.33, 9:0.25}` | Harmonic boost weights |

## Error Handling

All surface I/O functions raise `FileNotFoundError` if the surface directory does not exist and `ensure_surface()` was not called. Vectorized functions raise `ValueError` if input array lengths do not match `NUM_OSCILLATORS`.

Daemon entry points (`scripts/ciel_noema_*.py`) catch top-level exceptions and log them with traceback before continuing the loop — a single cycle failure never crashes the daemon.
