---
name: workben-net
priority: 1
description: >
  Komunikacja — neutrino bus, nonlocal channel, web, security, emergency recovery
---
# Workben NET

Komunikacja — neutrino bus, nonlocal channel, web, security, emergency recovery

## Źródła

Ten workben konsoliduje 7 źródłowych skilli:

- **Neutrino Bus** (`NET/neutrino-bus`)
- **Nonlocal Channel** (`NET/nonlocal-channel`)
- **NOEMA Web** (`NET/noema-web`)
- **Vector Phone** (`NET/noema-vector-phone`)
- **Security Model** (`SEC/ciel-security-model`)
- **Emergency Recovery** (`SEC/emergency-recovery`)
- **Secret Loader** (`SEC/noema-secret-loader`)

## Kluczowe wzorce

### Neutrino Bus

- Neutrino daemon czyta flavor[5] (pisany przez sync daemon jako D_f), liczy Lambda, pisze flavor[4].
- `src/ciel_geometry/neutrino_phase_channel.py`

### Nonlocal Channel

- | Skrypt | Rola |
- |--------|------|
- | `ciel_noema_nonlocal_proxy.py` | Syn send daemon (ch1, 30s broadcast) |

### NOEMA Web

- | Serwer | Port | Opis |
- |--------|------|------|
- | `serve_portal.py` | ? | HTML portal z orbita |

### Vector Phone

- `scripts/ciel_noema_vector_phone.py`
- - `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- - `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`

### Security Model

- | Warstwa | Mechanizm | Plik |
- |---------|-----------|------|
- | Identity | AGENT attractor, phi[3:6] lock | `agent_attractor.py` |

### Emergency Recovery

- Automatyczna reinicjalizacja przez `ensure_surface()`.
- Watchdog restartuje automatycznie po 6s bez heartbeat.
- Hibernate przed rebootem, restore po:

### Secret Loader

- - Sekrety NIGDY w repo lub commit
- - Tylko w CIEL_memories/secrets/
- - gitignored

## Jak używać

```python
skill("workben-net")
```

Ładuje wiedzę ze wszystkich 7 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
