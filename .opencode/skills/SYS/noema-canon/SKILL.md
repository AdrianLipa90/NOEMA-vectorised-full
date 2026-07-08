---
name: noema-canon
priority: 1
description: >
  >
---
# CIEL Canon CLI

## Użycie

```bash
python3 CIEL_CANON.py              # → status (daemony + warp + holonomy + consolidator)
python3 CIEL_CANON.py --probe      # → live surface read (tick, R, γ, unruh, mean_g)
python3 CIEL_CANON.py --up         # → systemctl start noema.target + consolidator
python3 CIEL_CANON.py --down       # → systemctl stop wszystkich daemonów
python3 CIEL_CANON.py --sonic      # → noema_sonic_daemon.main()
python3 CIEL_CANON.py --self       # → SelfModel().identity()
python3 CIEL_CANON.py --search Q   # → query_text(Q, top_k=10)
python3 CIEL_CANON.py --gaps       # → SelfModel().gaps()
python3 CIEL_CANON.py --sync       # → dual-surface read + metrics
```

## DAEMONS list

```python
DAEMONS = [
    "noema-kuramoto", "noema-phasenav", "noema-neutrino",
    "noema-resonance-bridge", "noema-linux-sensor",
    "noema-cielingo-sync", "noema-nonlocal-proxy",
    "noema-agent-backend", "noema-consolidator",
]
```

## Plik

`CIEL_CANON.py` (root projektowy)
