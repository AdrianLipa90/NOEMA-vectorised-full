---
name: nonlocal-channel
priority: 1
description: >
  >
---
# Nonlocal Channel

## Architektura

```
Agent A → nonlocal proxy → mmap → nonlocal listener → Agent B
         \→ X25519 encrypted (ciel_noema_x25519_exchange.py)
```

## Składniki

| Skrypt | Rola |
|--------|------|
| `ciel_noema_nonlocal_proxy.py` | Syn send daemon (ch1, 30s broadcast) |
| `ciel_noema_nonlocal_listener.py` | Listen daemon (ch1, parse broadcast) |
| `ciel_noema_x25519_exchange.py` | X25519 key exchange + encrypt |
| `build_nonlocal_cards_registry.py` | Card definitions |
| `build_nonlocal_definition_edges.py` | Edge definitions |
