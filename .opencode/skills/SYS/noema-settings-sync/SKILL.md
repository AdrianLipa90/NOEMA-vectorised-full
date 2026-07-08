---
name: noema-settings-sync
priority: 1
description: >
  >
---
# Settings Sync

## Sync flow

```
MCP set → noema_config.json write → systemctl restart daemon
```

## Pliki

- `noema_config.json` (w repo)
- `src/ciel_geometry/noema_config.py` (loader)
- `.config/systemd/user/noema-*.service` (ExecStart args)

## Zrodlo

- `scripts/catalog_zips_noema.py`
- `scripts/ciel_noema_x25519_exchange.py`
- `scripts/noema_register_cli.py`
