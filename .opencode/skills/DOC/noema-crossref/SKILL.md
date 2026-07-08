---
name: noema-crossref
priority: 1
description: >
  >
---
# NOEMA CrossRef

## Daemon → Plik

| Daemon systemd | Script |
|----------------|--------|
| noema-kuramoto | `scripts/ciel_noema_kuramoto_daemon.py` |
| noema-resonance-bridge | `scripts/ciel_noema_resonance_bridge.py` |
| noema-agent-backend | `scripts/ciel_agent_backend.py` |
| noema-linux-sensor | `scripts/ciel_noema_linux_sensor_daemon.py` |
| noema-neutrino | `scripts/ciel_noema_neutrino_daemon.py` |
| noema-cielingo-sync | `scripts/ciel_noema_cielingo_sync.py` |
| noema-phasenav (cold) | `scripts/ciel_noema_phasenav_daemon.py --node cold` |
| noema-phasenav-hot | `scripts/ciel_noema_phasenav_daemon.py --node hot` |
| noema-analog-blend | `scripts/noema_analog_phase_blend.py` |
| noema-archiver | `scripts/noema_phase_archiver.py` |
| noema-consolidator | `scripts/ciel_noema_consolidator_daemon.py` |
| noema-nonlocal-proxy | `scripts/ciel_noema_nonlocal_proxy.py` |

## Surface mmap → Kto pisze

| Field | Writer |
|-------|--------|
| phi | kuramoto (evolve) + analog-blend (inject) |
| omega | kuramoto |
| g | kuramoto + CIELingo sync (W_ij override) |
| flavor[0] | kuramoto (coherence) |
| flavor[1] | linux-sensor (mem_pressure) |
| flavor[3] | phasenav (mood) |
| flavor[4] | neutrino (Λ) |
| flavor[5] | CIELingo sync (D_f) |
| tick | kuramoto |
| gravity | kuramoto (evolve_surface) |

## Library → NOEMA

| Ścieżka | Opis |
|---------|------|
| `PHASE_INDEX/library_index.npy` | 1287×24D concept vectors |
| `PHASE_INDEX/library_meta.npy` | structured metadata |
| `/dev/shm/ciel_noema/zip_catalog/index.jsonl` | PhaseNav source |
| `agent_db/agent_state.db` | AGENT snapshots |
| `NOEMA/pdf_catalog.noema.json` | PDF catalog |
| `INDEX/system_map_v1.json` | system state |
