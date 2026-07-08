---
name: debug-surface
priority: 1
description: >
  >
---
# Debug Surface (36D)

## Raw mmap dump per field

```python
import numpy as np
phi = np.memmap('/dev/shm/ciel_noema/phi', dtype=np.float64, mode='r', shape=(36,))
omega = np.memmap('/dev/shm/ciel_noema/omega', dtype=np.float64, mode='r', shape=(36,))
g = np.memmap('/dev/shm/ciel_noema/g', dtype=np.float64, mode='r', shape=(36, 36))
flavor = np.memmap('/dev/shm/ciel_noema/flavor', dtype=np.float64, mode='r', shape=(6,))
tick = np.memmap('/dev/shm/ciel_noema/tick', dtype=np.uint64, mode='r', shape=(1,))
tau = np.memmap('/dev/shm/ciel_noema/tau', dtype=np.float64, mode='r', shape=(36,))
```

## Phase vector

```bash
python3 -c "
import numpy as np
phi = np.memmap('/dev/shm/ciel_noema/phi', dtype=np.float64, shape=(36,))
print('phi:', ['{:.3f}'.format(p) for p in phi])
print('coh:', abs(np.mean(np.exp(1j*phi))))
print('closure:', open('/dev/shm/ciel_noema/closure').read().strip())
print('warp:', open('/dev/shm/ciel_noema/imaginal_drive').read().strip())
"
```

## Analiza

| Odchylenie | Diagnoza |
|------------|----------|
| phi ~ uniform | brak synchronizacji |
| omega spike | CPU/IO szum |
| flavor[1] ~ 1 | memory pressure |
| gravity[1] > 5 | TARDIS aktywne |
| closure < 0.85 | algebra niedomknięta |
| phi[3:6] ~ 0 | AGENT attractor stracony |
