# NOEMA Daemon Reference

**Verified against live state 2026-07-18** via `CIEL_CANON.py --sub status` and `/home/adrian/.config/systemd/user/noema-*.{service,path,timer}`. Corrects a prior claim (removed) that daemons are launched manually as background python processes — they are actually managed by **systemd user units**, grouped under `noema.target`.

To see what's actually running:
```bash
systemctl --user status noema.target
systemctl --user list-units 'noema-*'
```

To start/stop the full ensemble:
```bash
systemctl --user start noema.target
systemctl --user stop noema.target
```

## Full verified service inventory (21 units, 2026-07-18)

| Unit | Description (from systemd) | ExecStart |
|------|------|-----------|
| `noema-agent-backend.service` | Agent backend (HTTP :18520 subconscious) | `scripts/ciel_agent_backend.py` |
| `noema-analog-blend.service` | Analog blend daemon (hot+cold → surface phi) | `scripts/noema_analog_phase_blend.py` |
| `noema-archiver.service` | Phase archiver daemon (HDF5 surface snapshots) | `scripts/noema_phase_archiver.py` |
| `noema-canonical-hash-sync.service` (+ `.path` trigger) | Canonical hash metadata synchronizer | `scripts/sync_canonical_hashes.py --update` |
| `noema-cielingo-sync.service` | CIELingo sync daemon (closure + W_ij blend + orchestrator) | `scripts/ciel_noema_cielingo_sync.py` |
| `noema-codex-fifo-bridge.service` | Canonical Codex hook FIFO → headless socket bridge | `runtime/hooks/codex_fifo_bridge.py --timeout 60` |
| `noema-consolidator.service` | Memory consolidator daemon (MemoryLog → m8_audit) | `scripts/ciel_memory_consolidator.py --daemon` |
| `noema-headless.service` | CIELingo Headless Daemon — canonical New Volume runtime | `scripts/ciel_headless_daemon.py` (ExecStartPre: hash sync + sha256sum check against `config/headless_runtime.sha256`) |
| `noema-htri-computation.service` (+ `.timer`) | Verified HTRI CUDA computation publisher | `scripts/publish_htri_computation_state.py --once --cpu-steps 64 --gpu-steps 64` → `CIEL_memories/state/htri_computation_state.json` |
| `noema-kuramoto.service` | Kuramoto phase evolution daemon | `scripts/ciel_noema_kuramoto_daemon.py` |
| `noema-linux-sensor.service` | Linux sensor daemon (proc → flavor+phi) | `scripts/ciel_noema_linux_sensor_daemon.py` |
| `noema-neutrino.service` | Neutrino daemon (PMNS → D_f → Λ → g_boost) | `scripts/ciel_noema_neutrino_daemon.py` |
| `noema-nonlocal-proxy.service` | Nonlocal proxy daemon (channel broadcast) | `scripts/ciel_noema_nonlocal_proxy.py` |
| `noema-orbital.service` (+ `.path` trigger) | Strict orbital topology snapshot | `src/ciel_geometry/orbital_model.py --write-state --source-map system_map_v2.json` (ExecStartPre: sha256sum check against `config/orbital_runtime.sha256`) |
| `noema-phasenav-hot.service` | PhaseNav hot daemon (analog bus phi_hot) | `scripts/ciel_noema_phasenav_daemon.py --node hot` |
| `noema-portal.service` | Portal — Cockpit and Research API (port 18888) | `scripts/noema_portal_daemon.py --host 127.0.0.1 --port 18888` |
| `noema-resonance.service` | Real↔imaginal resonance bridge and host-ledger writer | `scripts/ciel_noema_resonance_bridge.py --interval 1` |
| `noema-subconscious.service` | Subconscious Monitor — surface observation + anomaly detection | `scripts/ciel_noema_subconscious_daemon.py --interval 5.0` |
| `noema-surface-init.service` | `/dev/shm` surface bootstrap (tmpfs init) | `scripts/noema_surface_init.py` |
| `noema-watchdog.service` | Watchdog daemon (heartbeat monitor 6s) | `scripts/noema_watchdog.py` |
| `noema.target` | Grouping target for the full ensemble (`noema.target.wants/` lists enabled units) | — |

The 7 daemons detailed below (Kuramoto, Neutrino, Resonance Bridge, Linux Sensor, CIELingo Sync, Nonlocal Proxy, PhaseNav) still match their systemd `ExecStart` script paths — their algorithm descriptions below were **not** re-derived line-by-line from source in this pass, only their existence/entrypoint was confirmed. The other 14 units listed above (`agent-backend`, `analog-blend`, `archiver`, `canonical-hash-sync`, `codex-fifo-bridge`, `consolidator`, `headless`, `htri-computation`, `orbital`, `portal`, `subconscious`, `surface-init`, `watchdog`) have no algorithm section yet — only the verified Description/ExecStart above.

Each daemon self-registers with the subsystem registry (`ciel_sot_agent.subsystem_registry`) and the NOEMA daemon registry (`ciel_geometry.noema_registry`). The general lifecycle:

1. Insert `src/` into `sys.path`
2. Open or ensure the shared-memory surface via `ciel_geometry.noema_surface_mmap`
3. Read claimed surface files
4. Compute new state
5. Write results to surface files + flush
6. Heartbeat to registry
7. Sleep for interval

---

## 1. Kuramoto (`scripts/ciel_noema_kuramoto_daemon.py`)

| Property | Value |
|----------|-------|
| **Frequency** | 10 Hz (default `--interval 0.1`) |
| **Surface Claims** | `phi`, `omega`, `g`, `flavor[0]`, `tick` |
| **Cmdline** | `python scripts/ciel_noema_kuramoto_daemon.py [--interval 0.1] [--dt 0.05]` |
| **Registration** | `registry.register('kuramoto', claims=['phi','omega','g','tick'])` |
| **PID example** | 896372 |

**Purpose:** Primary phase evolution engine. Runs the Kuramoto synchronization algorithm with 3-6-9 harmonic coupling on the 24-oscillator surface at 10 Hz. All other daemons read the evolved phases and write modulations back.

**Algorithm:**
```
loop:
  surface = open_surface()
  thinking_delta = evolve_surface(surface, dt=args.dt, flush=True)
  step += 1
  every 5s: log tick, steps, phi_mean, coherence, mood, thinking_delta
  sleep(interval)
```

The `evolve_surface()` function (`src/ciel_geometry/noema_surface_mmap.py`):
```
For each oscillator i:
  S_i = Σ_h A_h · exp(i · h · φ_i)    // harmonic superposition
  Φ_eff_i = angle(S_i)                 // effective phase
  dφ_i/dt = ω_i + Σ_j g_ij · sin(Φ_eff_j - Φ_eff_i)
  φ_i ← φ_i + dt · dφ_i/dt
```

**Thinking trigger:** When the thinking delta (δΦ, the norm of the effective phase shift from harmonically coupled evolution) exceeds 0.5, the daemon logs a THINKING TRIGGER event.

**Surface I/O:**

| Reads | Writes |
|-------|--------|
| `phi`, `omega`, `g`, `flavor` | `phi` (evolved), `tick` (incremented) |

**Dependencies:** `ciel_geometry` (numpy)

---

## 2. Neutrino (`scripts/ciel_noema_neutrino_daemon.py`)

| Property | Value |
|----------|-------|
| **Frequency** | 0.5 Hz (every 2s, default `--interval 2.0`) |
| **Surface Claims** | `flavor[4]`, `flavor[5]`, `g` |
| **Cmdline** | `python scripts/ciel_noema_neutrino_daemon.py [--interval 2.0]` |
| **Registration** | `registry.register('neutrino', claims=['flavor','g'])` |
| **PID example** | 736714 |

**Purpose:** Implements the PMNS (Pontecorvo-Maki-Nakagawa-Sakata) neutrino flavor oscillation bus. Reads the fractal dimension D_f from flavor[5] (written by CIELingo sync), computes the cosmological constant Λ = (D_f - 2) / 0.57, writes Λ to flavor[4], and seeds the PMNS mixing matrix into the 3×3 intra-channel blocks of the g (coupling) matrix.

**Algorithm:**
```
loop:
  D_f = flavor[5]      # written by CIELingo sync daemon
  if D_f is invalid: D_f = 2.57 (default)
  bus = neutrino_bus_snapshot(surface, D_f)
  apply_neutrino_bus_to_surface(surface, bus,
      write_flavor=True, write_g=True)
  seed_neutrino_mixing(g, scale=flavor[4] * 0.3)
  flush_surface()
  every 5s: log cycle, D_f, Λ, bus_capacity, flavor[4], flavor[5]
  sleep(interval)
```

The bus computes 8 channels × 3 flavors (semantic ν_e, htri ν_μ, nonlocal ν_τ) with ε = sin²(2θ_eff) mixing angles derived from phase differences between oscillators within each triplet.

**Surface I/O:**

| Reads | Writes |
|-------|--------|
| `phi`, `omega`, `g`, `flavor` (all) | `flavor[4]` (Λ), `g` (PMNS-boosted) |

**Dependencies:** `ciel_geometry` (numpy), `ciel_sot_agent` (orbital manifest fallback)

---

## 3. Resonance Bridge (`scripts/ciel_noema_resonance_bridge.py`)

| Property | Value |
|----------|-------|
| **Frequency** | 1 Hz (every 1s, default `--interval 1.0`) |
| **Surface Claims** | Both surfaces: `phi`, `Z_geom`, `omega`, `flavor` |
| **Cmdline** | `python scripts/ciel_noema_resonance_bridge.py [--interval 1.0]` |
| **Registration** | `registry.register('resonance_bridge', claims=['phi','Z_geom'])` |
| **PID example** | 819580 |

**Purpose:** Maintains the dual-surface architecture. The imaginal surface (`/media/adrian/New Volume/CIEL_memories/imaginal/surface`) acts as the primary phase generator with low damping; it is not a `/dev/shm` mirror. The real surface (`/dev/shm/ciel_noema`) is a damped Poincaré section / readout. The bridge runs `dual_surface_step()`: updates both surfaces with CIEL state, evolves the imaginal autonomously, and computes resonance metrics (phase lock, coherence, drive).

**Algorithm:**
```
loop:
  bridge_state = {dominant_emotion, ethical_score, soul_invariant,
                  mood, coherence_index, closure_penalty}
  result = dual_surface_step(bridge_state, text=f"bridge_cycle_{cycle}")
  every 5s: log cycle, resonance_score, phase_lock, imaginal_drive, coherence
  sleep(interval)
```

The real surface is a "frozen slice" of the imaginal generator flow — analogous to a Poincaré section in dynamical systems. The resonance score measures how closely the surfaces are phase-locked.

**Surface I/O (real + imaginal):**

| Reads | Writes |
|-------|--------|
| `phi`, `omega`, `g`, `flavor` (both surfaces) | `phi`, `omega`, `Z_geom`, `R_geom`, `psi_geom` (both surfaces) |

**Dependencies:** `ciel_geometry` (numpy), `pi` (math)

---

## 4. Linux Sensor (`scripts/ciel_noema_linux_sensor_daemon.py`)

| Property | Value |
|----------|-------|
| **Frequency** | 1 Hz (fixed, `INTERVAL_S = 1.0`) |
| **Surface Claims** | `phi[0..23]`, `omega`, `flavor[0..5]` |
| **Cmdline** | `python scripts/ciel_noema_linux_sensor_daemon.py [--root /dev/shm/ciel_noema]` |
| **Registration** | `registry.register('linux_sensor', claims=['phi','omega','flavor'])` |
| **PID example** | 833527 (hypothetical) |

**Purpose:** Maps the real Linux system state (CPU, memory, load, processes, context switches, entropy) onto the 24 oscillator phases. Each oscillator channel corresponds to a system metric:

| Index | Metric | Source |
|-------|--------|--------|
| 0 | cpu_user | `/proc/stat` |
| 1 | cpu_nice | `/proc/stat` |
| 2 | cpu_system | `/proc/stat` |
| 3 | cpu_iowait | `/proc/stat` |
| 4 | cpu_irq | `/proc/stat` |
| 5 | cpu_softirq | `/proc/stat` |
| 6 | cpu_steal | `/proc/stat` |
| 7 | cpu_guest | `/proc/stat` |
| 8 | mem_total | `/proc/meminfo` |
| 9 | mem_free | `/proc/meminfo` |
| 10 | mem_available | `/proc/meminfo` |
| 11 | mem_cache | `/proc/meminfo` |
| 12 | mem_buffers | `/proc/meminfo` |
| 13 | swap_total | `/proc/meminfo` |
| 14 | swap_free | `/proc/meminfo` |
| 15 | swap_cached | `/proc/meminfo` |
| 16 | load_1 | `/proc/loadavg` |
| 17 | load_5 | `/proc/loadavg` |
| 18 | load_15 | `/proc/loadavg` |
| 19 | procs_run | `/proc/stat` |
| 20 | procs_block | `/proc/stat` |
| 21 | ctxt_per_sec | `/proc/stat` |
| 22 | forks_per_sec | `/proc/stat` |
| 23 | entropy | `/proc/sys/kernel/random/entropy_avail` |

Also writes flavor slots: `cpu_coherence` (0), `mem_pressure` (1), `io_wait` (2), `load_mood` (3), `entropy_open` (4), `sys_mode` (5).

**Algorithm:**
```
loop:
  snap = sensor.snapshot()          # reads /proc → phi[24], flavor[6], omega[24]
  sensor.write_surface(surface, snap)
  every 5 cycles:
    pn = sensor.process_phasenav()  # compute operator fingerprint
    if fingerprint changed: log new op + harmonic fingerprint
  every 30 cycles:
    top = top_processes(5)          # top 5 PIDs with PhaseNav enrichment
    log PID, command, CPU time, operator_id, harmonic_fingerprint
  sleep(1.0s - elapsed)
```

**Surface I/O:**

| Reads | Writes |
|-------|--------|
| — | `phi[0..23]`, `omega[0..23]`, `flavor[0..5]` |

**Dependencies:** `ciel_geometry` (numpy, `LinuxSensor` class), `/proc` filesystem

---

## 5. CIELingo Sync (`scripts/ciel_noema_cielingo_sync.py`)

| Property | Value |
|----------|-------|
| **Frequency** | ~0.03 Hz (every 30s, default `--interval 30.0`) |
| **Surface Claims** | `phi`, `flavor[5]`, `g`, `tick` |
| **Cmdline** | `python scripts/ciel_noema_cielingo_sync.py [--interval 30.0] [--oneshot]` |
| **Registration** | `registry.register('cielingo_sync', claims=['phi','flavor','g','tick'])` |
| **PID example** | 812641 |

**Purpose:** The most complex daemon. Runs the full CIELingo closure cycle every ~30s:

1. **CIELingo orbital bridge**: Calls `build_orbital_bridge()` which runs the CIELingo semantic model, reads the manifest, computes closure penalty (cp), coherence, and recommended control mode.
2. **PMNS boost**: Reads `phi`, `g`, `omega`, `flavor` from surface, runs `compute_neutrino_phase_bus()`, applies boost to `g` matrix.
3. **τ ↔ φ feedback**: Modulates tau (learning rate) from Euler residual R and cp. `τ_i += 0.05 · R · cos(φ_target - φ_i) - 0.02 · (τ - 0.353)`, clipped to [0.01, 1.0].
4. **D_f → Λ → g_boost loop**: cp → D_f = 2.57 − 0.57·min(1.0, cp/1.5) → flavor[5] → neutrino daemon reads flavor[5] → Λ = (D_f-2)/0.57 → flavor[4] → PMNS boost g.
5. **Euler identity sync**: Applies Euler closure constraint: `φ_i → φ_i + 0.08 · angle(e^{i(φ_target_i - φ_i)})`, targeting Σ e^{iφ} = 0.
6. **W_ij override**: Writes `couplings_wij_optimized.json` as an adaptive blend (1–12%) between base coupling and PMNS-boosted g values. Uses cp trajectory to adjust blend ratio.
7. **Tiered memory orchestrator**: Writes a snapshot to the 3-tier memory system via `get_orchestrator().write()` with salience derived from cp.
8. **Manifest sync**: Reads/writes `integration/Orbital/main/manifests/sectors_global.json`.

**Algorithm:**
```
loop:
  # 1. CIELingo closure
  bridge = build_orbital_bridge(ROOT)
  cp = bridge.closure_penalty, coh = bridge.coherence, mode = bridge.mode

  # 2. PMNS boost + Euler sync on surface
  surface = ensure_surface()
  bus = compute_neutrino_phase_bus(phi, g, omega, flavor, D_f=2.57)
  apply_neutrino_bus_to_surface(surface, bus)

  # 3. τ ← φ feedback
  R = |Σ exp(i·φ_i)|
  τ_i += 0.05 · R · cos(target_i - φ_i)
  τ_i -= 0.02 · (τ_i - 0.353)
  τ_i = clip(τ_i, 0.01, 1.0)

  # 4. D_f from cp
  D_f = 2.57 - 0.57 · min(1.0, cp/1.5)
  flavor[5] = D_f           # for neutrino daemon
  flavor[3] = min(1.0, R/6.0)  # Euler residual proxy

  # 5. Adaptive W_ij blend
  blend = adjust_based_on_cp_trajectory()
  W_override = blend(base_couplings, pmns_boosted_g, blend)
  write(couplings_wij_optimized.json)

  # 6. Tiered memory orchestrator
  get_orchestrator().write(snapshot, mode=WriteMode.AUTO)

  # 7. manifest → surface: Euler enforcement
  manifest_to_surface(surface)
  flush_surface()

  sleep(interval - elapsed)
```

**Surface I/O:**

| Reads | Writes |
|-------|--------|
| `phi`, `omega`, `g`, `flavor` | `phi` (Euler-synced), `g` (PMNS-boosted), `flavor[5]` (D_f), `flavor[3]` (Euler proxy) |

**Dependencies:** `ciel_geometry`, `ciel_sot_agent` (orbital_bridge), `CIEL_OMEGA_COMPLETE_SYSTEM` (orchestrator), numpy

---

## 6. Nonlocal Proxy (`scripts/ciel_noema_nonlocal_proxy.py`)

| Property | Value |
|----------|-------|
| **Frequency** | 1 Hz (default `--interval 1.0`) |
| **Surface Claims** | Both surfaces: `phi`, `flavor` (all channels) |
| **Cmdline** | `python scripts/ciel_noema_nonlocal_proxy.py [--interval 1.0] [--no-relay]` |
| **Registration** | `registry.register('nonlocal_proxy', claims=['phi','flavor'])` |
| **PID example** | 833527 |

**Purpose:** Cross-agent φ-RAG (phase-based Retrieval-Augmented Generation) relay. Listens on all 8 communication channels on both surfaces, relays messages between real and imaginal surfaces via phase coupling, handles X25519 key exchange for encrypted sessions, and logs all nonlocal events to `nonlocal_inbox.jsonl`.

**Agent model:** Agent A (MAC a) → nonlocal proxy → Agent B (MAC b). The proxy bridges the real surface (Agent A's readout) with the imaginal surface (Agent B's generator) through phase differences.

**Algorithm:**
```
loop:
  phi_r = real["phi"], phi_i = imag["phi"]
  for each channel 0..7:
    msgs = channel.listen(ch_id)
    for each message:
      # X25519 auto-respond
      if msg.type == "x25519_exchange":
        respond with public key, anchor flavor[5]=4.0
      # log to inbox
      log_entry(entry)

  if relay enabled:
    for each channel 0..7:
      diff = angle(exp(i · (phi_i - phi_r)))  # phase diff = message delta
      energy = std(diff)
      if energy > 0.8:
        # REAL → IMAG: gamma = 0.05
        imag["phi"] += gamma · sin(phi_r - phi_i)
        log_relay(channel, energy)

  every 5s: log coherence_R, coherence_I, lock, message_count
  sleep(interval)
```

**Surface I/O (real + imaginal):**

| Reads | Writes |
|-------|--------|
| `phi`, `omega`, `flavor` (both surfaces) | `phi` (imaginal, relayed), `flavor[5]` (on X25519 completion) |

**Dependencies:** `ciel_geometry` (nonlocal_channel, surface), `cryptography` (X25519), numpy

---

## 7. PhaseNav (`scripts/ciel_noema_phasenav_daemon.py`)

| Property | Value |
|----------|-------|
| **Frequency** | 0.2 Hz (every 5s, default `--interval 5.0`) |
| **Surface Claims** | `phi`, `flavor[3]` |
| **Cmdline** | `python scripts/ciel_noema_phasenav_daemon.py [--interval 5.0] [--strength 0.2]` |
| **Registration** | `registry.register('phasenav', claims=['phi','flavor'])` |
| **PID example** | (varies) |

**Purpose:** PhaseNav operator enrichment daemon. Seeds oscillator phases with operator attractor vectors from the 33-operator algebra. Uses the LinuxSensor's system fingerprint to match current system state to an operator, then blends the operator's phase signature into the surface.

In addition to operator seeding, the daemon reads the ZIP index (`/dev/shm/ciel_noema/zip_catalog/index.jsonl`) and seeds concepts from the 5GB CIEL archive that match the current operator fingerprint.

**Algorithm:**
```
loop:
  snap = sensor.snapshot()
  pn = sensor.process_phasenav(snap)
  current_op = pn["operator"]
  current_fp = pn["harmonic_fingerprint"]

  if cycle % 2 == 0:
    seed operator vector for current_op → blend into phi
  elif cycle % 3 == 0 and matching ZIP exists:
    seed concept from ZIP archive with same operator
  elif cycle % 5 == 0:
    seed random operator from archive

  flavor[3] = 0.1 + 0.8 * cos_similarity  # mood = operator affinity
  flush_surface()
  sleep(interval)
```

**Surface I/O:**

| Reads | Writes |
|-------|--------|
| `phi` | `phi` (operator-seeded blend), `flavor[3]` (mood) |

**Dependencies:** `ciel_geometry` (phasenav, linux_sensor, surface), numpy

---

## Orchestrator: The 6-Flavor Handshake

The six flavor channels form a closed-loop communication bus between daemons. Each daemon writes only its assigned slots and reads slots written by others:

```
flavor[0]  cpu_coherence
  Writer:   Linux Sensor (1Hz) — CPU utilization coherence
  Reader:   Kuramoto (10Hz) — modulates omega baseline

flavor[1]  mem_pressure
  Writer:   Linux Sensor (1Hz) — MemAvailable / MemTotal
  Reader:   (reserved for future use)

flavor[2]  io_wait
  Writer:   Linux Sensor (1Hz) — I/O pressure proxy (context switch rate)
  Reader:   Resonance Bridge (1s) — dampens imaginal→real projection
            on high I/O

flavor[3]  load_mood
  Writer:   Linux Sensor (1Hz) / PhaseNav (5s) — inverse system load,
            modulated by operator affinity
  Reader:   CIELingo Sync (30s) — influences blend aggressiveness

flavor[4]  entropy / Λ (cosmological constant)
  Writer:   Neutrino daemon (2s) — Λ = (D_f - 2) / 0.57
  Reader:   CIELingo Sync (30s) — reads Λ for PMNS boost scale
            PhaseNav (5s) — reads entropy for operator affinity

flavor[5]  mode / D_f (fractal dimension)
  Writer:   CIELingo Sync (30s) — D_f = 2.57 - 0.57·min(1.0, cp/1.5)
  Reader:   Neutrino daemon (2s) — reads D_f for PMNS bus computation
            Nonlocal Proxy (1s) — anchors flavor[5]=4.0 on X25519
```

### Closed-Loop Flow

```
                     ┌─────────────────────────────────────┐
                     │          CIELingo Sync              │
                     │  cp → D_f → flavor[5]               │
                     │  flavor[4] (Λ) → PMNS boost scale   │
                     └──────────┬──────────────────────────┘
                                │ flavor[5]
                                ▼
                     ┌─────────────────────────────────────┐
                     │          Neutrino Daemon             │
                     │  flavor[5] (D_f) → Λ → flavor[4]    │
                     │  PMNS mixing → g matrix boost        │
                     └──────────┬──────────────────────────┘
                                │ flavor[4] (Λ)
                                ▼
                     ┌─────────────────────────────────────┐
                     │          CIELingo Sync              │
                     │  reads Λ → scales PMNS blend       │
                     │  new cp → new D_f → flavor[5]       │
                     └─────────────────────────────────────┘
```

This feedback loop is the core of the NOEMA self-optimization:
- Lower cp → higher D_f → higher Λ → stronger PMNS boost → lower cp (reinforcing)
- Higher cp → lower D_f → lower Λ → weaker PMNS boost → higher cp (damping)

The Linux Sensor feeds real system data into `flavor[0..3]`, providing the environmental context that modulates the loop.

---

## Daemon Launcher (corrected: systemd, not manual scripts)

The ensemble is managed by `systemctl --user` via `noema.target` (see the verified service inventory above) — `scripts/ciel.sh`/`scripts/ciel_start.sh` may still exist as manual/dev-mode alternatives but are not the production launch path as of 2026-07-18.

```bash
systemctl --user start noema.target      # start the full ensemble
systemctl --user status noema.target     # check status
journalctl --user -u noema-kuramoto.service -f   # tail a specific daemon's logs
```

To verify all daemons are running and the surface is alive:

```bash
python3 CIEL_CANON.py --sub status
python scripts/noema_status.py
```
