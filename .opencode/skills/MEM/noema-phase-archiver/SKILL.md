---
name: noema-phase-archiver
priority: 1
description: >
  >
---
# Phase Archiver

## Snapshot

Co 50 ticków zapisuje:
- phi, omega, g, flavor, gravity, tick
- timestamp, R_coherence, γ

## Format

```python
# HDF5 (preferowany)
with h5py.File(path) as f:
    f.create_dataset("phi", data=phi)
    f.create_dataset("omega", data=omega)
    f.attrs["tick"] = tick

# NPZ fallback
np.savez_compressed(path, phi=phi, omega=omega, tick=tick)
```

## Daemon

Systemd: `noema-archiver.service`

## Plik

`scripts/noema_phase_archiver.py`
