---
name: linux-sensor
priority: 1
description: >
  >
---
# Linux Sensor

## Klasa

```python
sensor = LinuxSensor(smoothing=0.3)
snap = sensor.snapshot()              # → LinuxSensorSnapshot
sensor.write_surface(surface, snap)   # → mmap
report = sensor.process_phasenav(snap)  # → operator match
procs = sensor.top_processes(n=10)    # → top PID z PhaseNav
```

## 24 kanały (SYSTEM_OSC_MAP)

```
CPU (0-7):      user(0), nice(1), system(2), iowait(3), irq(4), softirq(5), steal(6), guest(7)
MEM (8-15):     total(8), free(9), available(10), cache(11), buffers(12),
                swap_total(13), swap_free(14), swap_cached(15)
LOAD (16-23):   load_1(16), load_5(17), load_15(18), procs_run(19), procs_block(20),
                ctxt_per_sec(21), forks_per_sec(22), entropy(23)
```

## snapshot()

```python
snap.phi[0:8]   = cpu_phi     # /proc/stat → min(val/100,1)*2π
snap.phi[8:16]  = mem_phi     # /proc/meminfo → kB→GB, min(v/16,1)*2π
snap.phi[16:24] = load_phi    # /proc/loadavg → min(v/8,1)*2π; entropy → /proc/sys/.../entropy_avail
snap.flavor[1]  = 1 - mem_available/mem_total   # mem_pressure
snap.omega      = clip(|dphi|*100, 0.1, 100.0)  # 1st derivative
snap.thinking_delta = mean(|raw - prev_raw| / prev_raw)
```

**EMA smoothing**: `φ_ema = 0.3·φ_raw + 0.7·φ_ema_prev` — silne wygładzanie.

## write_surface()

```python
surface["phi"] = snap.phi
surface["omega"] = snap.omega
surface["flavor"][1] = snap.flavor[1]   # only mem_pressure
surface["tick"] = snap.tick
surface["Z_geom"] = cos(snap.phi)
surface["R_geom"] = |mean(e^{iφ})|
surface["psi_geom"] = angle(mean(e^{iφ}))
```

## process_phasenav()

```python
state_vec = concat(sin(φ[:12]), cos(φ[:12]))   # 24D
cos_sims = op_matrix @ normalize(state_vec)
best_op = argmax(cos_sims)
R_h = |mean(e^{i·h·φ})| for h∈{1,3,6,9}
fp = "".join("H" if R_h>0.5 else "L")          # "HHHH", "LLHL"
# return {operator, cos_similarity, harmonic_fingerprint, R, thinking_delta, flavor, tick}
```

## top_processes(n=10)

Scan /proc → top N po CPU sec → PhaseNav enrich per PID.

## Plik

`src/ciel_geometry/linux_sensor.py` (305 lines)
