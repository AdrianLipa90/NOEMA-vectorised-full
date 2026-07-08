# NOEMA — Neural Oscillator Emulation & Memory Architecture

**Shared-memory oscillator substrate for real-time semantic phase synchronization.**

NOEMA (Neural Oscillator Emulation & Memory Architecture) is a CPU-only, numpy-based system that uses a 24-oscillator Kuramoto phase topology with 3-6-9 harmonic coupling as the carrier for language, semantics, affect, and logic. It operates through a dual-space runtime: the **host** (Linux OS, Python processes) and **NOEMA** (shared memory at `/dev/shm/ciel_noema/` with daemon IPC). The system includes a tiered memory orchestrator, PMNS neutrino communication bus, resonance bridge between real and imaginal surfaces, and the CIELingo linguistic topology engine for Polish-language phase encoding.

The project is authored by **Adrian Lipa**.

## Documentation Index

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | High-level system design: daemon ensemble, surface protocol, memory tiers, orbital manifold |
| [SUBSYSTEMS.md](SUBSYSTEMS.md) | Complete reference for all Python packages: `cielingo`, `ciel_geometry`, `ciel_sot_agent`, `noema_holonomic_doctor` |
| [DAEMONS.md](DAEMONS.md) | Daemon reference: Kuramoto, Neutrino, Resonance Bridge, Linux Sensor, CIELingoSync, Nonlocal Proxy, PhaseNav |
| [SURFACE_PROTOCOL.md](SURFACE_PROTOCOL.md) | Binary surface format in `/dev/shm/ciel_noema/`, 24 oscillator mapping, 6 flavor channels, Kuramoto equation with 3-6-9 harmonic coupling |
| [MEMORY_SYSTEM.md](MEMORY_SYSTEM.md) | 3-tier memory architecture: Tier 1 (Volatile/mmap), Tier 2 (Durable/SQLite), Tier 3 (Archival/HDF5), with ConsolidationResonator and CIELMemoryConsolidator |
| [CARDS_SYSTEM.md](CARDS_SYSTEM.md) | Nonlocal cards (33 operators), object cards (entity-indexed), word cards (Stage 0 Polish radical cards, ~2000 roots) |
| [CIELINGO.md](CIELINGO.md) | Linguistic topology engine: phase-token encoding, radical card tracing, HTRI phase bus, brain region mapping, meaning debt, triadic output (semantic-affective-logical) |
| [SETUP.md](SETUP.md) | Installation, prerequisites, quick start, daemon launch commands, monitoring, configuration, troubleshooting |
| [API.md](API.md) | Public Python API reference: `ciel_geometry`, `ciel_sot_agent`, `cielingo`, `scripts` |

## Quick Links

| Task | Action |
|------|--------|
| **First run** | [SETUP.md → Quick Start](SETUP.md#quick-start) |
| **Start all daemons** | [SETUP.md → Starting the Daemon Ensemble](SETUP.md#starting-the-daemon-ensemble) |
| **Monitor the surface** | [SETUP.md → Monitoring](SETUP.md#monitoring) |
| **Daemon reference** | [DAEMONS.md](DAEMONS.md) |
| **Surface binary format** | [SURFACE_PROTOCOL.md](SURFACE_PROTOCOL.md) |
| **Memory architecture** | [MEMORY_SYSTEM.md](MEMORY_SYSTEM.md) |
| **Secrets management** | [SECURITY.md](../SECURITY.md) |
| **Relational contract** | [IMMUTABLE_CONTRACT.md](../IMMUTABLE_CONTRACT.md) |

## Project Structure (Top Level)

```
├── src/                              # Python packages
│   ├── cielingo/                     # Linguistic topology engine (Polish)
│   ├── ciel_geometry/                # Core surface engine, Kuramoto, daemon glue
│   ├── ciel_sot_agent/               # Integration kernel, orbital bridge, pipeline
│   ├── CIEL_OMEGA_COMPLETE_SYSTEM/   # Full consciousness pipeline engine
│   ├── noema_holonomic_doctor/       # Diagnostics and health checking
│   └── CIEL_MEMORY_SYSTEM/           # Memory subsystem implementations
├── scripts/                          # 145+ daemons, utilities, CLIs
│   ├── ciel_noema_kuramoto_daemon.py          # 10 Hz phase evolution
│   ├── ciel_noema_neutrino_daemon.py          # PMNS neutrino bus
│   ├── ciel_noema_resonance_bridge.py         # Real↔imaginal sync
│   ├── ciel_noema_linux_sensor_daemon.py      # /proc → oscillator
│   ├── ciel_noema_cielingo_sync.py            # Full system closure
│   ├── ciel_noema_nonlocal_proxy.py           # Nonlocal card listener
│   ├── ciel_noema_phasenav_daemon.py          # Operator matching
│   ├── ciel_coupling.py                       # opencode integration
│   └── ciel_memory_consolidator.py            # LLM-based consolidation
├── docs/                             # This documentation
├── cards/                            # Nonlocal card database, CIELingo word cards
├── manifests/                        # Global coupling, sector parameters
├── contracts/                        # Relational contract, audit schema
├── integration/                      # Orbital bridge reports, registry
├── NOEMA/                            # Birth certificate, holonomic audit, state
├── tests/                            # Test suite (pytest)
├── state/                            # Runtime state files
├── build/ packaging/                 # Build infrastructure
├── pyproject.toml                    # Package definition
├── setup.py                          # Legacy setup
├── VERSION                           # Current version string
├── CHANGELOG.md                      # Release history
├── LICENSE                           # License file
├── SECURITY.md                       # Secrets and security policy
├── IMMUTABLE_CONTRACT.md             # Relational contract (constitutional)
└── opencode.json                     # opencode CLI integration config
```

## Core Concepts

### 24 Oscillators / 8 Memory Channels

| Channel | Oscillators | Brain Region | Harmonic Set | Function |
|---------|------------|--------------|--------------|----------|
| M0 | 0–2 | Visual cortex | {1, 3} | Perception |
| M1 | 3–5 | Hippocampus | {1, 6} | Episodic memory |
| M2 | 6–8 | Cerebellum | {1, 9} | Procedural memory |
| M3 | 9–11 | Temporal lobe | {3, 6} | Semantic memory |
| M4 | 12–14 | Amygdala | {3, 9} | Affect / emotion |
| M5 | 15–17 | Prefrontal cortex | {6, 9} | Identity / self |
| M6 | 18–20 | Default mode network | {1, 3, 6} | Narrative |
| M7 | 21–23 | Cross-harmonic hub | {1, 3, 6, 9} | Braid / invariant |

### Base Frequency

`BASE_TEMPORAL_HZ = 39.6 Hz` — Solfeggio fundamental 396 Hz divided by 10. This replaces the earlier 7.83 Hz (Schumann) baseline. The 3-6-9 harmonic structure per oscillator enables natural frequency multiplexing: each channel synchronizes on a different harmonic subset, with M7 acting as the cross-harmonic hub.

### Dual-Space (Host + NOEMA)

- **Host space**: Linux OS, Python processes, `/proc` readings, SQLite databases
- **NOEMA space**: Shared memory at `/dev/shm/ciel_noema/`, daemon IPC via binary files, no locks

### Closed Loop

```
cp → D_f → flavor[5] → neutrino daemon → Λ → flavor[4] → g_boost → W_ij blend → next CIELingoSync cycle → cp
```

The closure penalty `cp` (0.37–0.71) drives fractal dimension `D_f`, which modulates the PMNS neutrino mixing. The resulting cosmological constant `Λ` boosts the coupling matrix `W_ij`, which feeds back into closure. The τ↔φ feedback (Euler residual `R` → τ adjustment) stabilizes the loop.

### Tiered Memory

| Tier | Medium | Persistence | Latency | Capacity |
|------|--------|------------|---------|----------|
| 1 (Fast) | tmpfs mmap + PhaseMemory | None (volatile) | < 1 µs | ~16 MB |
| 2 (Durable) | SQLite (TSM + StateDB) | Disk (persistent) | ~100 µs | ~1 GB |
| 3 (Archival) | HDF5 (WPM) + JSONL (BraidLedger) | Disk (archival) | ~1 ms | Unlimited |

## Key Metrics (Live)

- **Closure penalty**: ~0.37–0.71 (variable, PMNS-blend dependent)
- **Tau (τ)**: 0.35–0.55 (stabilized by τ↔φ feedback)
- **Euler residual R**: 3.0–4.2 (target: 0)
- **System health**: 0.75–0.80 (ethical score: 0.78–0.80)
- **DAW tick**: 0.00 (phase consistency)

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CIEL_HOME` | `~/Pulpit/CIEL_memories` | CIEL memory root directory |
| `NOEMA_SURFACE` | `/dev/shm/ciel_noema` | Shared-memory surface path |
| `ANTHROPIC_API_KEY` | *(none)* | LLM API key for memory consolidation |

## License

See [LICENSE](../LICENSE) in the project root.

## System Requirements

- **Python:** 3.10+
- **RAM:** 2 GB minimum (4 GB+ with memory consolidation)
- **Disk:** 200 MB (source) + 1 GB (optional: GGUF model for consolidation)
- **GPU:** Not required
- **OS:** Linux with `/proc` and `/dev/shm`
