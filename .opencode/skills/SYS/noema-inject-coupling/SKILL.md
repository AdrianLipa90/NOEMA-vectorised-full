---
name: noema-inject-coupling
priority: 1
description: >
  >
---
# Inject Coupling

## Manual

```bash
python3 scripts/noema_inject_coupling.py --pair M3,M5 --boost 0.5
```

## Automatic (w CIELingo sync daemon)

```
cp → D_f → flavor[5] → neutrino → flavor[4] → g_boost → W_ij blend
```

## Format override

`couplings_wij_optimized.json` — blend (2-12%) między base coupling a PMNS-boosted g.
