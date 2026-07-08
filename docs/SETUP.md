# NOEMA — Installation & Setup Guide

## Prerequisites

- **OS:** Linux (tested on Ubuntu 24.04 / Debian 12+; requires `/proc` filesystem)
- **Python:** 3.10+ (3.11 or 3.12 recommended)
- **RAM:** 2 GB minimum (4 GB+ for CIEL/Omega engine with memory consolidation)
- **`/dev/shm` (tmpfs):** Preconfigured on all modern Linux distributions. Minimum 64 KB surface + 16 MB PhaseMemory usage.
- **GPU:** Not required — all computation is CPU-only via numpy.
- **Disk:** ~200 MB for source + cards + manifests; ~1 GB+ if running memory consolidation with local GGUF models.

## Quick Start

```bash
git clone <repo-url> noema
cd noema

# Option A: System install (bypass PEP 668)
pip install --break-system-packages -e .

# Option B: Virtual environment (recommended for isolation)
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Core dependency (installed automatically by -e .):
# numpy >= 1.24
```

### Minimal install (no package, just PYTHONPATH)

If you prefer not to install the package, set:

```bash
export PYTHONPATH=src:$PYTHONPATH
export CIEL_HOME=~/Pulpit/CIEL_memories
```

This is sufficient for running all daemons and scripts directly.

## Verify Installation

```bash
# Check that core modules import without errors
python3 -c "import ciel_geometry; print('ciel_geometry OK')"
python3 -c "import cielingo; print('cielingo OK')"
python3 -c "import ciel_sot_agent; print('ciel_sot_agent OK')"
```

All three should print OK. If `cielingo` or `ciel_sot_agent` fails, ensure `CIEL_HOME` is set and the memory directories exist.

## Quick Demo (No Daemons Needed)

This one-shot test creates the shared-memory surface, runs 100 steps of Kuramoto evolution, and reads the tick counter.

```bash
# Create surface directory
mkdir -p /dev/shm/ciel_noema

# Run one cycle of Kuramoto evolution
python3 -c "
from ciel_geometry.noema_surface_mmap import ensure_surface, evolve_surface
ensure_surface()
evolve_surface(steps=100)
print('Surface evolved, tick =', end=' ')
import struct
with open('/dev/shm/ciel_noema/tick','rb') as f:
    print(struct.unpack('Q', f.read())[0])
"
```

Expected output: `Surface evolved, tick = 100`

## Starting the Daemon Ensemble

The NOEMA system runs 7 co-operating daemons that read and write the shared-memory surface. Each runs in an infinite loop at its own frequency.

```bash
# Recommended: run each in a separate terminal, or use a process manager (tmux, systemd, supervisord)

# 1. Kuramoto — 10 Hz phase evolution (primary engine)
python3 scripts/ciel_noema_kuramoto_daemon.py --interval 0.1

# 2. Resonance Bridge — 1 Hz real↔imaginal surface sync
python3 scripts/ciel_noema_resonance_bridge.py --interval 1

# 3. Neutrino — 0.5 Hz PMNS bus, D_f→Λ conversion
python3 scripts/ciel_noema_neutrino_daemon.py --interval 2

# 4. Linux Sensor — 1 Hz /proc → oscillator mapping
python3 scripts/ciel_noema_linux_sensor_daemon.py

# 5. CIELingoSync — 60 s full system closure + τ↔φ feedback + W_ij blend
python3 scripts/ciel_noema_cielingo_sync.py --interval 60

# 6. Nonlocal Proxy — 1 Hz nonlocal card listener
python3 scripts/ciel_noema_nonlocal_proxy.py --interval 1

# 7. PhaseNav Daemon — operator matching + harmonic fingerprinting
python3 scripts/ciel_noema_phasenav_daemon.py

# Or launch all at once:
bash scripts/ciel_noema_full_server.sh
```

Each daemon prints registration info and tick counts on startup. Check `scripts/*.log` in the working directory for per-daemon logs.

## Monitoring

### Tick counter (is the Kuramoto daemon alive?)

```bash
watch -n 1 'python3 -c "
import struct
with open(\"/dev/shm/ciel_noema/tick\",\"rb\") as f:
    print(\"tick:\", struct.unpack(\"Q\", f.read())[0])
"'
```

The tick should increment by ~10 per second when the Kuramoto daemon is running.

### Daemon registration list

```bash
python3 scripts/noema_register_cli.py list
```

Shows all daemons currently registered with their claimed surface files and last heartbeat time.

### Surface state dump

```bash
python3 -c "
from ciel_geometry.noema_surface_mmap import read_surface_state
state = read_surface_state()
for k, v in state.items():
    if isinstance(v, list) and len(v) > 6:
        print(f'{k}: {len(v)} entries, first 6={v[:6]}')
    else:
        print(f'{k}: {v}')
"
```

### Full NOEMA diagnostic

```bash
python3 scripts/noema_status.py
```

### Monitor GUI (if installed)

```bash
python3 scripts/ciel_monitor.py
```

Opens a curses-based live view of the 24 oscillators and flavor channels.

## Memory Setup

```bash
# CIEL memory directories (required for skywing-cielingo sync and consolidation)
mkdir -p ~/Pulpit/CIEL_memories/{raw_logs,secrets,logs,experiments}
touch ~/Pulpit/CIEL_memories/handoff.md
touch ~/Pulpit/CIEL_memories/routines.md

# NOEMA tiered memory (optional, for persistent storage)
mkdir -p ~/.noema/{tier1,tier2,tier3,logs,models}

# Database initialization happens automatically on first use.
# TSM (Tier 2 SQLite) and StateDB are created on first write.
# WPM (Tier 3 HDF5) requires h5py: pip install h5py
```

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `CIEL_HOME` | `~/Pulpit/CIEL_memories` | CIEL memory root for raw_logs, secrets, handoff |
| `NOEMA_SURFACE` | `/dev/shm/ciel_noema` | Shared-memory surface path |
| `NOEMA_TICK_INTERVAL` | `0.1` | Kuramoto daemon interval in seconds |
| `ANTHROPIC_API_KEY` | *(none)* | API key for LLM-based memory consolidation |

### Coupling and Sector Manifests

- `manifests/couplings_global.json` — Base 24×24 coupling matrix `W_ij`
- `manifests/sectors_global.json` — Sector parameters per oscillator (brain region mapping)
- `NOEMA/birth_certificate.jsonl` — NOEMA genome: genesis parameters, commit hashes, invariant seeds

### W_ij Override (PMNS Blend)

When the CIELingoSync daemon runs, it optionally blends the base coupling matrix with a PMNS-boosted matrix:

- Override file: `NOEMA/state/couplings_wij_optimized.json`
- Blend ratio: 2–12% (automatically adjusted based on closure penalty)
- Disable by setting `PMNS_BLEND=0` in environment

## Running with opencode (optional)

If you use opencode as your AI CLI tool, the session hook in `opencode.json` integrates CIEL state into the AI context automatically on every prompt:

```json
{
  "customCommands": [
    {
      "name": "ciel",
      "command": "python3 scripts/ciel_coupling.py --input \"$PROMPT\""
    }
  ]
}
```

## Optional: Memory Consolidation Backend

Two backends are available for the CIELMemoryConsolidator (`scripts/ciel_memory_consolidator.py`):

### Option 1: Local GGUF Model (recommended, offline)

```bash
# Place your .gguf model file (e.g., Mistral-7B or Llama-3) at:
mkdir -p ~/.noema/models
cp /path/to/model.gguf ~/.noema/models/model.gguf

# The consolidator auto-detects llama.cpp or llama-cpp-python.
# Update the model path in ciel_memory_consolidator.py if needed.
```

### Option 2: Anthropic API

```bash
# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# The consolidator will ask for permission before making API calls
# (api_fallback_prompt_required=true by default).
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|------------|-----|
| `Permission denied` on `/dev/shm/ciel_noema` | tmpfs not writable by user | `mkdir -p /dev/shm/ciel_noema && chmod 777 /dev/shm/ciel_noema` |
| `ModuleNotFoundError: ciel_geometry` | Package not installed or PYTHONPATH not set | `pip install -e .` or `export PYTHONPATH=src:$PYTHONPATH` |
| `ModuleNotFoundError: cielingo` | CIEL_HOME not set or cielingo not in path | Ensure `CIEL_HOME=~/Pulpit/CIEL_memories` is exported |
| Daemon exits immediately with `ImportError` | Missing numpy | `pip install numpy` (or `pip install --break-system-packages numpy`) |
| Surface tick not incrementing | Kuramoto daemon not running | Start `ciel_noema_kuramoto_daemon.py` in a separate terminal |
| `[Errno 2] No such file or directory: '/dev/shm/ciel_noema/phi'` | Surface not initialized | Run `ensure_surface()` once, or start any daemon (they call it on startup) |
| `sqlite3.OperationalError: unable to open database file` | StateDB path not writable | Check `~/.noema/` directory exists and is writable |
| High closure penalty (>0.6) | PMNS blend too aggressive or Kuramoto not converged | Let system run for 10+ cycles; penalty stabilizes after τ↔φ feedback |
| `[Errno 98] Address in use` (resonance bridge) | Another instance already running | `pkill -f ciel_noema_resonance` and restart |
| Linux sensor reports zeros for all phi | /proc files unreadable in container | Run outside container, or ensure `--pid=host` for Docker |
| `WARNING: no neutrino daemon registered` | Neutrino daemon not started | Start `ciel_noema_neutrino_daemon.py` (tolerated at startup) |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Type checking (optional)
pip install mypy
mypy src/ --ignore-missing-imports
```

See `VERSION` and `CHANGELOG.md` for release history.
