---
name: ciel-codex-bridge
priority: 2
description: >
  >
---
# Codex Bridge

## Flow

```
Codex agent → codex_bridge_to_ciel.py → surface → CIEL state
CIEL state → ciel_codex_bridge.sh → Codex agent
```

## Systemd

```bash
systemctl --user enable noema-codex-bridge.service
```

## Pliki

- `scripts/codex_bridge_to_ciel.py`
- `scripts/ciel_codex_bridge.sh`
- `scripts/ciel_codex_bridge.service`
- `scripts/enable_codex_bridge_systemd_user.sh`
