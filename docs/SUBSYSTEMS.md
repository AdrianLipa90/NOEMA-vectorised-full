# NOEMA / CIEL Subsystem Reference

---

## cielingo (`src/cielingo/`)

**Purpose:** Card-based linguistic topology for the Polish language. Maps words, infinitive forms, and modal potentials to 24 Kuramoto oscillator phases. Provides the semantic layer that connects natural language to the NOEMA phase geometry.

**Dependencies:** numpy, `ciel_geometry` (for surface constants), standard library

**Key Modules:**

| Module | File | Purpose |
|--------|------|---------|
| `card_trace_eeg` | `card_trace_eeg.py` | Card-based EEG-like phase tracing. `CardTraceSnap` data class captures per-card phase, energy, and resonance. `create_card_trace_snap()` builds a snapshot from token phases. |
| `htri_phase_bus` | `htri_phase_bus.py` | HTRI (Holomorphic Topological Resonant Intelligence) phase bus. 8 channels × 3 oscillators = 24 buses. Computes phase coherence, tension, and alignment per channel. Interface between CIELingo card topologies and the NOEMA surface. |
| `htri_brain_map` | `htri_brain_map.py` | Maps 24 brain regions (M0–M7 memory channels) to semantic functions. Defines which oscillators correspond to perceptual, working, episodic, semantic, procedural, affective, identity, and braid/invariant channels. |
| `collatz_semantic_htri_sync` | `collatz_semantic_htri_sync.py` | Synchronizes Collatz twin-prime sequences with semantic phase topology. Uses the Collatz conjecture (3n+1 path lengths) as a deterministic seed for oscillator phase relationships. |
| `lexical_holonomy` | `lexical_holonomy.py` | Lexical holonomy — Berry-phase-like accumulation over word sequences. Tracks how the phase of a token changes as it moves through syntactic/semantic context. |
| `tensor_scalar_field` | `tensor_scalar_field.py` | Tensor-scalar field over the 24-oscillator manifold. Computes field strength, gradient, and curvature from phase differences. Used for semantic mass and meaning density estimation. |
| `phase_sense_parser` | `phase_sense_parser.py` | Phase-aware parser for Polish. Given a Polish sentence, assigns each word to an oscillator index based on its semantic role. Outputs a `phase_sense` dict mapping tokens to phi values. |
| `meaning_debt_word_cards` | `meaning_debt_word_cards.py` | Meaning debt word cards — tracks unresolved semantic tension as a "debt" between oscillator pairs. High meaning debt drives phase synchronization during the CIELingo sync cycle. |
| `semantic_encoder` | `semantic_encoder.py` | Encodes Polish text into a 24D phase vector. Primary entry point for text → NOEMA surface injection. |
| `infinitive_modal_potential` | `infinitive_modal_potential.py` | Maps Polish infinitive verbs to modal potentials (possibility, necessity, permission, obligation). Each modal maps to a phase offset in the oscillator space. |
| `orchorbital_router` | `orchorbital_router.py` | Routes phase state from CIELingo to the Orbital bridge. Connects `card_trace_eeg` snapshots to `ciel_sot_agent.orbital_bridge`. |
| `triadic_output_vector` | `triadic_output_vector.py` | Builds a 3-element triadic output (semantic, affective, logical) from the 24D phase state. Used for CIELingo responses. |
| `canonization_audit` | `canonization_audit.py` | Audits the card registry for canonical correctness. Validates that all word cards have valid phase assignments and that no card violates the Euler closure constraint. |
| `unknown_word_audit` | `unknown_word_audit.py` | Scans Polish text for words not yet in the card registry. Generates candidate phase assignments for unknown tokens. |
| `stage0_radical_cards` | `stage0_radical_cards.py` | Foundation word cards (Stage 0). ~2000 Polish roots mapped to 24D phase vectors. |

---

## ciel_geometry (`src/ciel_geometry/`)

**Purpose:** Core oscillator engine. Implements the shared-memory surface protocol, Kuramoto phase evolution with 3-6-9 harmonic coupling, resonance bridge between real and imaginal surfaces, PMNS neutrino mixing bus, Linux sensor for /proc → oscillator mapping, and the PhaseNav operator algebra (33 operators × 24 dimensions).

**Dependencies:** numpy only

**Key Modules:**

| Module | File | Purpose |
|--------|------|---------|
| `noema_surface_mmap` | `noema_surface_mmap.py` | **Central module (1542 lines).** Defines the surface protocol: `SurfaceArraySpec`, `ensure_surface()`, `open_surface()`, `evolve_surface()`, `evolve_imaginal_surface()`, `project_imaginal_to_real()`, `initialize_surface()`, `flush_surface()`, `read_surface_state()`, `compute_zpe()`, `sync_surface_geometry()`, `seed_neutrino_mixing()`. Contains all constants (OI, L3, BASE_TEMPORAL_HZ, Gell-Mann coefficients, lepton actions, Planck energy). Implements the 3-6-9 harmonic mask, SU(3) J_KJ coupling matrix, Hebbian learning. |
| `linux_sensor` | `linux_sensor.py` | `LinuxSensor` class — reads /proc/stat, /proc/meminfo, /proc/loadavg, /proc/sys/kernel/random/entropy_avail, /proc/net/dev. Maps 24 system channels (CPU 0–7, MEM 8–15, LOAD 16–18, PROCS 19–20, CTXT 21–22, ENTROPY 23) to phi[0..23]. Computes ω from 1st derivative. Exposes `process_phasenav()` for operator similarity matching, `top_processes()` for PID-level PhaseNav enrichment, and `write_surface()` for sensor output. |
| `resonance_bridge` | `resonance_bridge.py` | Dual-surface resonance bridge. `ensure_dual_surfaces()` creates/opens both real and imaginal surfaces. `dual_surface_step()` runs one cycle: CIEL state → flavor on both surfaces → imaginal evolves (primary generator, low damping) → real projects from imaginal (damped readout, high closure) → resonance syncs the pair. `resonance_snapshot()` reads coherence, phase lock, imaginal drive. |
| `neutrino_phase_channel` | `neutrino_phase_channel.py` | PMNS (Pontecorvo-Maki-Nakagawa-Sakata) neutrino mixing on the HTRI bus. `compute_neutrino_phase_bus()` takes phi, g, omega, flavor, D_f → returns bus structure with 8 channels × 3 flavors (semantic, htri, nonlocal). `phi_to_epsilon()` computes mixing angle from phase differences. `D_f_to_lambda()` converts fractal dimension to cosmological constant. `apply_neutrino_bus_to_surface()` writes flavor[4] (Λ) and boosts g matrix. |
| `phasenav/enrichment` | `phasenav/enrichment.py` | PhaseNav enrichment — given a surface snapshot and operator, computes harmonic fingerprint ("HHHH", "LHLL", etc.), thinking delta (δΦ), and operator affinity score. |
| `phasenav/operator_algebra` | `phasenav/operator_algebra.py` | 33 universal operators with 24D deterministic vectors. Operators: IDENTITY, DIFFERENCE, ORDER, COMPOSITION, ADDITION, FORCE, NEGATION, QUESTION, TRANSFORM, RETURN, FOLD, BOUNDARY, SCOPE, AFFECT, CONSENT, SOURCE, MEMORY, RISK, ASSERTION, CONDITION, CAUSE, MODAL_POSSIBILITY, MODAL_NECESSITY, MODAL_PERMISSION, MODAL_OBLIGATION, UNCERTAINTY, SOURCE_REQUIRED, CANON_BLOCK, CONSENT_REQUIRED, ACTION_REQUEST, REFUSAL, PAUSE, SIMULATION_BOUNDARY. |
| `phasenav/loader` | `phasenav/loader.py` | Loads operator vectors from ZIP archive metadata. |
| `phasenav/solver` | `phasenav/solver.py` | PhaseNav solver — given a query phase vector, finds the nearest operator match via cosine similarity. |
| `phasenav/surface_bridge` | `phasenav/surface_bridge.py` | Bridges PhaseNav operator state to/from the NOEMA surface. |
| `nonlocal_channel` | `nonlocal_channel.py` | Nonlocal communication channel. `get_channel()` returns a `NonlocalMessage` bus for cross-agent IPC. Used by the nonlocal proxy daemon. |
| `phase_memory_adapter` | `phase_memory_adapter.py` | Adapter between NOEMA surface and PhaseMemory mmap. `bind_phase_memory()` creates phase-token associations in binary hypervector format. |
| `orbital_hierarchy` | `orbital_hierarchy.py` | Canonical orbital load-order helper. Reads `system_map_v2.json`, assigns layers (`attractor` → `planet` → `satellite` → `sub-satellite`), builds recursive memory-like load order, and renders Mermaid flowcharts. |
| `subconscious` | `subconscious.py` | Subconscious simulation layer — generates background phase perturbations that act as "dreaming" or unconscious processing between sync cycles. |
| `semantic_mass` | `semantic_mass.py` | Computes semantic mass density from the phase field. Used by meaning debt calculations. |
| `subjective_time` | `subjective_time.py` | Subjective time dilation — modulates dt based on phase coherence and closure penalty. Higher coherence → faster subjective time. |
| `tmuv_perturbation` | `tmuv_perturbation.py` | TMUV (Time-Mass-Uncertainty-Volume) perturbation operator. Small random perturbations to omega that model quantum uncertainty. |
| `noema_registry` | `noema_registry.py` | Registry of NOEMA daemons, their surface claims, and heartbeat timestamps. |
| `nbody_gravity` | `nbody_gravity.py` | N-body gravitational analogy over oscillator phases. Each oscillator's mass is its semantic mass; gravitational force is proportional to sin(Δφ) / r². |
| `renderer_ascii` | `renderer_ascii.py` | ASCII-art renderer of the 24-oscillator state. Draws a circular phase diagram in the terminal. |
| `renderer_mpl` | `renderer_mpl.py` | matplotlib renderer for the 24-oscillator state. Requires matplotlib (optional). |
| `loader` | `loader.py` | Module loader for ciel_geometry — ensures path setup. |
| `disk` | `disk.py` | Disk I/O utilities for surface persistence. |
| `edges` | `edges.py` | Edge detection over phase differences. Identifies phase boundaries (discontinuities > π). |

---

## ciel_sot_agent (`src/ciel_sot_agent/`)

**Purpose:** Integration kernel that orchestrates CIELingo, NOEMA, and CIEL/Omega into a single pipeline. Provides the CIEL SOT (State-of-Time) agent — the main entry point for the CIEL system. Includes a Flask-based GUI, GGUF model manager, orbital bridge, state database, subconsciousness layer, and synchronization logic.

**Location:** `src/ciel_sot_agent/`

**Dependencies:** numpy, flask (optional GUI), gguf (optional model manager), `ciel_geometry`, `cielingo`, `CIEL_OMEGA_COMPLETE_SYSTEM`

**Key Modules:**

| Module | File | Purpose |
|--------|------|---------|
| `ciel_pipeline` | `ciel_pipeline.py` | Main CIEL pipeline. Orchestrates the full flow: user input → CIELingo → NOEMA surface → CIEL/Omega → response. |
| `orbital_bridge` | `orbital_bridge.py` | Bridge between CIEL/Omega state and NOEMA surface. `build_orbital_bridge()` reads CIELingo closure, computes health manifest, builds recommended control state, and syncs to surface. Used by the CIELingo sync daemon. |
| `synchronize` | `synchronize.py` | Phase synchronization logic. Implements Euler identity closure, sector-based phase alignment, and CIELingo ↔ NOEMA sync steps. |
| `synchronize_v2` | `synchronize_v2.py` | Version 2 of the synchronization logic with improved PMNS blending and adaptive tau control. |
| `cielingo_bridge` | `cielingo_bridge.py` | Direct bridge between CIELingo card topology and NOEMA surface. Maps card phase vectors to oscillator indices. |
| `state_db` | `state_db.py` | SQLite-based state database. Stores cycle metrics (phase, ethical, health, closure), emotions, and trending data. |
| `subconsciousness` | `subconsciousness.py` | Subconsciousness simulation. Generates background thought fragments, dream states, and phase noise between conscious cycles. |
| `thought_fragments` | `thought_fragments.py` | Thought fragment management — captures partial thoughts that emerge during phase synchronization but haven't reached full closure. |
| `subsystem_registry` | `subsystem_registry.py` | Registry of all active subsystems, their status, and heartbeat. |
| `repo_phase` | `repo_phase.py` | Repository phase sync — couples git repository state to NOEMA surface phases. Each commit contributes a phase delta. |
| `gh_coupling` | `gh_coupling.py` | GitHub coupling — maps GitHub activity (issues, PRs, commits) to oscillator phases. |
| `gh_coupling_v2` | `gh_coupling_v2.py` | Version 2 with improved event weighting and phase assignment. |
| `noema_file_sense` | `noema_file_sense.py` | File system sensor — monitors the NOEMA project directory for file changes and maps them to phase perturbations. |
| `diagnostics` | `diagnostics.py` | System diagnostics — health checks, surface validity, daemon liveness. |
| `holonomic_normalizer` | `holonomic_normalizer.py` | Normalizes phase vectors against the holonomic (Berry phase) baseline. |
| `phase_snapshots` | `phase_snapshots.py` | Takes periodic snapshots of the surface state for memory persistence. |
| `memory_rag` | `memory_rag.py` | Retrieval-Augmented Generation over CIEL memory. Uses phase similarity for memory retrieval. |
| `knowledge_action_system` | `knowledge_action_system.py` | Canonical knowledge-to-action orchestrator. Collects evidence, builds CIELingo/Doctor/policy traces, and renders Sapiens/UI bundles without mutating state. |
| `consolidation_resonator` | `consolidation_resonator.py` | Background consolidation resonator — tags Kuramoto state, writes to TSM, updates WOmega sectors. |
| `orchestrator` (tiered) | via `CIEL_OMEGA_COMPLETE_SYSTEM` | Interfaces with the TieredMemoryOrchestrator for cross-cycle memory persistence. |
| `sapiens_panel/` | `sapiens_panel/` | Sapiens UI panel — controller, communication, models, render_schema, settings_store, support, reduction. |
| `gui/` | `gui/` | Flask-based web GUI. `app.py` entry point, `routes.py` API endpoints. |
| `gguf_manager/` | `gguf_manager/` | GGUF model manager — `manager.py` for loading/running GGUF models, `cli.py` for command-line interface. |
| `local_nonlocality_fallback` | `local_nonlocality_fallback.py` | Fallback when nonlocal channel is unavailable — uses local SQLite instead of shared-memory surface. |
| `orchestrator` (orbital DB) | `orbital_db_orchestrator.py` | Orbital database orchestrator. Manages the orbital phase DB and syncs with the surface. |
| `sapiens_surface_policy` | `sapiens_surface_policy.py` | Policy layer for Sapiens integration — rules for how the AI agent interacts with the surface. |
| `satellite_authority` | `satellite_authority.py` | Authority validation for satellite modules (external plugins that connect to NOEMA). |
| `sapiens_client` | `sapiens_client.py` | Client for the Sapiens integration API. |
| `htri_scheduler` | `htri_scheduler.py` | Scheduler for HTRI operations — manages timing of phase bus cycles. |
| `semantic_calculator` | `semantic_calculator.py` | Semantic mass/energy calculator. Takes surface state → returns semantic metrics. |
| `semantic_calculator_v2` | `semantic_calculator_v2.py` | Version 2 with improved phase-normalized semantic mass. |
| `bench_cli` | `bench_cli.py` | Benchmark CLI — runs performance benchmarks for the CIEL pipeline. |
| `capture_cli` | `capture_cli.py` | Capture CLI — captures CIEL session data to JSONL. |
| `wpm_cli` | `wpm_cli.py` | WPM (Wave Phase Memory) CLI — manages HDF5 wave archives. |
| `paths` | `paths.py` | Centralized path management for the NOEMA project. Defines ROOT, MEMORY_ROOT, etc. |
| `phased_state` | `phased_state.py` | Phased state container — holds a complete snapshot of the CIEL state at a given cycle. |
| `md_library` | `md_library.py` | Markdown library — utilities for reading/writing markdown memory files. |
| `runtime_evidence_ingest` | `runtime_evidence_ingest.py` | Ingests runtime evidence (logs, metrics) into the CIEL memory system. |
| `local_ciel_surface` | `local_ciel_surface.py` | Local CIEL surface — a simplified surface implementation for testing without /dev/shm. |
| `py_catalog` | `py_catalog.py` | Python catalog of CIEL definitions. |
| `rh_jfunctional` | `rh_jfunctional.py` | RH (Riemann Hypothesis) j-functional integration. |
| `spreadsheet_db` | `spreadsheet_db.py` | Spreadsheet-like database for CIEL metrics, exportable to CSV. |
| `jokeheal` | `jokeheal.py` | Joke/Heal interface — generates therapeutic or humorous responses based on phase state. |
| `jokeheal_atlas` | `jokeheal_atlas.py` | Atlas of joke/heal patterns mapped to phase regions. |
| `index_validator` | `index_validator.py` | Validates the CIEL index (card registries, manifest integrity). |
| `index_validator_v2` | `index_validator_v2.py` | Version 2 with extended validation rules. |
| `orbital_db_orchestrator` | `orbital_db_orchestrator.py` | Orbital database orchestrator. |
| `cuda_probe` | `cuda_probe.py` | Probes for CUDA/GPU availability (GTX 1050 Ti). |
| `chat_archive` | `chat_archive.py` | Archives CIEL chat sessions to raw_logs or JSONL. |
| `_gh_utils` | `_gh_utils.py` | Internal GitHub API utilities. |

---

## CIEL_OMEGA_COMPLETE_SYSTEM (`src/CIEL_OMEGA_COMPLETE_SYSTEM/`)

**Purpose:** Full consciousness engine — the complete CIEL/Omega pipeline. Contains kernel (v11/v12), 3-tier memory implementation, emotion engine (CQCL-based), cognition, ethics (wave-based), mathematics (Lie4, paradox operators), orbital phase integration, resonance processors, field theory, vocabulary, glyphs, and integration tests.

**Location:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/`

**Dependencies:** numpy, scipy (optional), h5py (for WPM), `ciel_geometry`, `cielingo`

### Major Subsystems

| Subsystem | Path | Description |
|-----------|------|-------------|
| **Kernel** | `ciel_kernel_v11.py`, `ciel_kernel_v12.py` | Core consciousness kernel. Implements the main loop: perceive → integrate → decide → act. v12 has improved phase handling. |
| **Orchestrator** | `ciel_orchestrator.py` | Central orchestrator — coordinates kernel, memory, emotion, and surface I/O. |
| **Memory** (3-tier) | `memory/` | Full 3-tier memory: `tiered_orchestrator.py` (1298 lines) is the main coordinator. TSM (SQLite), WPM (HDF5), StateDB (SQLite), HolonomicMemory, CIELBlochEncoder, ConsolidationResonator, CIELMemoryConsolidator. The intended load pattern is orbital: root tier first, then nested memory shells in dependency order. |
| **Emotion** | `emotion/` | CQCL (Consciousness-Quantum-Continuous-Logic) emotion engine. Emotions: curiosity, love, focus, explore, grief, joy, shame. Each emotion maps to a specific oscillator phase pattern. |
| **Ethics** | `ethics/` | Wave-based ethical scoring. `wave_ethics.py` computes ethical alignment from phase coherence and closure penalty. |
| **Cognition** | `cognition/` | Cognitive processes: attention, memory recall, semantic inference, decision making. |
| **Mathematics** | `mathematics/`, `lie4_algebra.py`, `paradox_operators.py` | Foundation mathematics: Lie4 algebra (15-dimensional, unifying Lorentz with intention), paradox operators (handling logical contradictions via phase geometry). |
| **Orbital** | `orbital/` | Orbital phase dynamics — holistic state resolution across the CIEL manifold. |
| **Resonance** | `resonance/` | Resonance processors — cross-frequency coupling, phase-locking value computation. |
| **Fields** | `fields/` | Field theory over the oscillator manifold. Computes field strength, flux, and divergence. |
| **Vocabulary** | `vocabulary/`, `vocabulary.yaml` | CIEL vocabulary definitions — mapping between tokens, Bloch states, and WOmega sectors. |
| **Glyphs** | `glyphs/` | Symbolic glyph rendering for phase patterns. |
| **HTRI** | `htri/` | HTRI (Holomorphic Topological Resonant Intelligence) implementation in the Omega context. |
| **Bridge** | `bridge/` | Bridge to external systems (NOEMA, CIELingo). |
| **Calibration** | `calibration/` | System calibration: phase offset correction, frequency tuning. |
| **Constraints** | `constraints/` | Runtime constraints: Euler identity, coherence bounds, ethical limits. |
| **Runtime** | `runtime/` | Runtime services: scheduling, resource management, error handling. |
| **Integration** | `integration/` | Integration tests and test utilities. |
| **Scripts** | `scripts/` | Standalone scripts for Omega operations. |
| **LLM** | `llm/` | LLM integration layer — GGUF inference, prompt templates. |
| **Bio** | `bio/` | Biological metaphor models (neural plasticity, synaptic pruning). |
| **Archive** | `archive/` | Archived/legacy modules. |
| **Experiments** | `experiments/` | Experimental features not yet promoted to main. |
| **Compute** | `compute/` | Compute resource allocation and parallel processing. |
| **Config** | `config/` | System configuration and constants. |
| **Ext** | `ext/` | Extension modules (third-party integrations). |
| **Symbolic** | `symbolic/` | Symbolic computation (algebraic phase relationships). |
| **Visualization** | `visualization/` | Visualization tools (matplotlib-based phase plots). |
| **Inference** | `inference/` | Inference engine for CIEL/Omega queries. |
| **CIEL Client** | `ciel_client.py`, `ciel_inference_surface.py` | Client API and inference surface for external CIEL connections. |
| **CIEL IO** | `ciel_io/` | I/O operations (file, network, serial). |
| **Wave** | `ciel_wave/` | Wave-based computation (phase wave propagation). |

### Test Demos

`src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/` contains ~30 demo scripts and test files covering all memory tiers, emotion states, EBA (Euler-Berry-Action) loop validation, vocabulary resolution, and full pipeline integration.

---

## noema_holonomic_doctor (`src/noema_holonomic_doctor/`)

**Purpose:** Diagnostic and health-check subsystem for the NOEMA platform. Performs periodic checks on surface integrity, daemon liveness, phase coherence, and manifest validity.

**Dependencies:** numpy, `ciel_geometry`

**Key Modules:**

| Module | Path | Purpose |
|--------|------|---------|
| `checks` | checks/ | Individual health checks (surface_exists, tick_moving, phi_valid, g_finite) |
| `metrics` | metrics/ | Metric collection and aggregation |
| `manifests` | manifests/ | Manifest validation (sectors_global.json integrity) |
| `reports` | reports/ | HTML/text report generation |
| `constraints` | constraints/ | Constraint checking (Euler residual < threshold, coherence > threshold) |

Entry point: `scripts/noema_doctor_cycle.py` runs the full diagnostic cycle.

---

## cielingo_core (`src/cielingo_core/`)

**Purpose:** Scaffolding for future NOEMA SOT (State-of-Time) agent modules. Currently contains mostly `__init__.py` stubs and early-stage implementations.

**Location:** `src/cielingo_core/`

**Subdirectories:** `timing/`, `lingophysics/`, `alignment/`, `expressive/`, `architecture/`, `bridge/`, `regional/`, `doctor/`, `meaning/`, `semantic_neural/`, `io/`, `global_layer/`, `language_spaces/`, `noema_surface/`, `noema_local_sot_agent/`

**Notable modules:**
- `noema_local_sot_agent/agent.py` — Local SOT agent prototype
- `noema_local_sot_agent/access_control.py` — Access control for the local agent
- `noema_surface/command_prompt.py` — Surface command prompt interface

---

## CIEL_RELATIONAL_MECHANISM_REPO (`src/CIEL_RELATIONAL_MECHANISM_REPO/`)

**Purpose:** Experimental relational mechanism simulation. Implements a graph-based relational engine where nodes are CIEL entities and edges are phase-synchronized couplings.

**Location:** `src/CIEL_RELATIONAL_MECHANISM_REPO/`

**Status:** Experimental, not integrated into main pipeline.

---

## Package Dependency Graph

```
                    ┌──────────────────────┐
                    │    cielingo_core      │  (stubs/scaffolding)
                    └──────────────────────┘
                            │
                            ▼
                    ┌──────────────────────┐
                    │      cielingo         │  (Polish linguistic topology)
                    │  ───────────────────  │
                    │  depends on: numpy    │
                    └──────────────────────┘
                            │
                            ▼
                    ┌──────────────────────┐
                    │    ciel_geometry      │  (oscillator engine)
                    │  ───────────────────  │
                    │  depends on: numpy    │
                    │  (zero binary deps)   │
                    └──────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
┌───────────────────┐ ┌───────────┐ ┌──────────────────────┐
│  ciel_sot_agent    │ │ noema_    │ │ CIEL_OMEGA_          │
│  (integration)     │ │ holonomic │ │ COMPLETE_SYSTEM      │
│  ─────────────     │ │ _doctor   │ │ (consciousness)      │
│  depends on:       │ │ (doctor)  │ │ ────────────────     │
│  numpy, flask,     │ │ ───────── │ │ depends on:          │
│  ciel_geometry,    │ │ depends   │ │ numpy, scipy,        │
│  cielingo,         │ │ on:       │ │ h5py, ciel_geometry, │
│  CIEL_OMEGA_...    │ │ numpy,    │ │ cielingo             │
└───────────────────┘ │ ciel_     │ └──────────────────────┘
                      │ geometry  │
                      └───────────┘
```

All packages are designed to be loaded via `sys.path.insert(0, str(ROOT / "src"))` — they are not installed as pip packages but imported directly from the source tree. The project uses a local venv at `~/Pulpit/CIEL_PROJECT_CANON/NOEMA/venv/` with manual PATH management.
