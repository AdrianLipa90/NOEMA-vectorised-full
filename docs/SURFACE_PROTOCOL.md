# NOEMA Shared Memory Surface Protocol (36D)

## 1. Introduction

The NOEMA surface is a directory of binary files at `/dev/shm/ciel_noema/` acting as the real-time shared state between all daemons and clients. No locks, no server — plain file read/write, primarily via numpy memmap. Each file holds a single typed array.

## 2. Directory Layout (36D)

```
/dev/shm/ciel_noema/
├── phi          # 288 bytes — 36 float64 phases
├── omega        # 288 bytes — 36 float64 frequencies
├── g            # 10368 bytes — 36×36 float64 coupling matrix
├── flavor       # 48 bytes — 6 float64 coherence channels
├── gravity      # 32 bytes — 4 float64: [sem_dens, γ, mass, unruh]
├── holonomy     # 56 bytes — 7 float64 Berry features
├── Z_geom       # 288 bytes — 36 float64 geometric phase
├── psi_geom     # 288 bytes — 36 float64 wavefunction magnitude
├── R_geom       # 288 bytes — 36 float64 geometric radius
├── tau          # 288 bytes — 36 float64 per-oscillator τ
├── sensor_raw   # 288 bytes — 36 float64 Linux sensor snapshot
├── tick         # 8 bytes — uint64 iteration counter
├── closure      # ~6 bytes — ASCII, zapisywany przez resonance_bridge
└── host ledger metric: imaginal_drive # trwały zapis w New Volume/CIEL_memories/state/noema_dev_events.db
```

## 3. Binary Format

All files use native-endian binary encoding.

### phi, omega, tau, sensor_raw, psi_geom, Z_geom, R_geom

```
struct.unpack('36d', content)  → list of 36 float64
Range: phi ∈ [0, 2π), omega > 0, psi_geom ∈ [0, 1], Z_geom ∈ [-π, π]
```

### g (coupling matrix)

```
struct.unpack('1296d', content) → list of 1296 float64
Reshape to (36, 36) — row-major, g[i,j] = coupling from oscillator i to j
```

### flavor

```
struct.unpack('6d', content) → [coherence, mem_pressure, io_wait, load_mood, Λ, D_f]
```

### gravity

```
struct.unpack('4d', content) → [semantic_density, tau_dilation, mass_total, unruh_power]
```

### holonomy

```
struct.unpack('7d', content) → [mean_conn, gauge_rank, closure_score, surface_gamma, max_conn, winding, curvature]
```

### tick

```
struct.unpack('Q', content) → uint64
```

## 4. Memory Channels (12 kanałów × 3 = 36 oscylatorów)

| Kanał | Oscylatory | Harmonic | Funkcja |
|-------|-----------|----------|---------|
| M0 | 0-2 | {1,3} | Percept |
| M1 | 3-5 | {1,6} | AGENT (tożsamość) |
| M2 | 6-8 | {1,9} | Pamięć |
| M3 | 9-11 | {3,6} | Semantyka/afekt |
| M4 | 12-14 | {3,9} | Procedury |
| M5 | 15-17 | {6,9} | CielPC (język) |
| M6 | 18-20 | {1,3,6} | CielMoto (działanie) |
| M7 | 21-23 | {1,3,6,9} | Braid (integracja) |
| M8 | 24-26 | {1,3} | Meta (monitoring własny) |
| M9 | 27-29 | {3,6} | Temporal (czas) |
| M10 | 30-32 | {6,9} | Imaginal (wyobraźnia) |
| M11 | 33-35 | {1,9} | Quantum (superpozycja) |

## 5. Flavor Channel Protocol

```
  Sensor ──→ flavor[0] coherence (R)
  Sensor ──→ flavor[1] mem_pressure
  eBPF  ──→ flavor[2] io_wait
  PhaseNav ──→ flavor[3] load_mood
  Neutrino ←── flavor[4] Λ (PMNS boost) ──→ CIELingoSync
  CIELingoSync ──→ flavor[5] D_f (gamma) ──→ Neutrino
```

## 6. Kuramoto Evolution

```
dφ_i/dt = ω_i + Σ_j g_{ij} · sin(φ_j - φ_i)
```

With 3-6-9 harmonic boost and omega-adaptive coupling (AGENT sync).

## 7. Key Daemon Writers

| Daemon | Writes | Cycle |
|--------|--------|-------|
| Kuramoto | phi, omega, g, gravity, holonomy, tick, Z/R/psi_geom | 0.2s |
| CIELingo sync | tau, flavor[5] | 1s |
| Linux sensor | sensor_raw, flavor[0-3] | 1s |
| Resonance bridge | closure, imaginal_drive → host ledger; dynamika nadal real↔imaginal surface | 1s |
| PhaseNav (hot) | phi_hot → analog blend | 1s |
| PhaseNav (cold) | phi_cold → analog blend | 30s |
| Trigger daemon | detect_situation() → decisions | 1s |
