---
name: workben-debug
priority: 1
description: >
  Debug — watchdog, sonic diagnostic, test infra, audit, health check, holonomic doctor
---
# Workben DEBUG

Debug — watchdog, sonic diagnostic, test infra, audit, health check, holonomic doctor

## Źródła

Ten workben konsoliduje 13 źródłowych skilli:

- **Health Check** (`AUD/system-health-check`)
- **Watchdog** (`AUD/noema-watchdog`)
- **Sonic Diagnostic** (`AUD/noema-sonic-diagnostic`)
- **Test Infrastructure** (`AUD/noema-test-infra`)
- **Stress Tests** (`AUD/noema-stress-tests`)
- **Status** (`AUD/noema-status`)
- **Canon Audit** (`AUD/canon-audit`)
- **Monitoring** (`AUD/ciel-monitoring`)
- **CIELingo Audit** (`AUD/cielingo-audit-tools`)
- **Debug Surface (36D)** (`AUD/debug-surface`)
- **Audit Consolidator** (`AUD/noema-audit-consolidator`)
- **Holonomic Audit** (`COMP/noema-holonomic-audit`)
- **Holonomic Doctor** (`COMP/noema-holonomic-doctor`)

## Kluczowe wzorce

### Health Check

- Oczekiwane: 10-12 ● active. Żadnego dead.
- Oczekiwane: wszystkie daemony heartbeat < 6s.
- R_coherence ~0.5-0.9. < 0.3 → problem.

### Watchdog

- `scripts/noema_watchdog.py`
- - `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- - `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`

### Sonic Diagnostic

- Pokazuje co 10s:
- - closure_penalty, D_f, τ̄, Euler residual
- - Registry scan (live daemons)

### Test Infrastructure

- | Test | Lokacja | Status (Jun 25) |
- |------|---------|-----------------|
- | cielingo basic | `tests/` | 46/51 → 51/51 |

### Stress Tests

- - `src/ciel_lingophysics_lns_repo_v2_3/reports/v2_2_noema_retrieval_inference_gate_report.md`
- - `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md`
- - `src/ciel_lingophysics_lns_repo_v2_3/docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md`

### Status

- Pokazuje:
- - Phi (24), ω, g, flavor, gravity
- - Daemon registry (PID, tick, uptime)

### Canon Audit

- | Marker | Detection |
- |--------|-----------|
- | `except:pass` | `grep -r "except.*:" --include="*.py" \| grep -v "Exception\|Error\|Stop"` |

### Monitoring

- | Skrypt | Co monitoruje | Interwał |
- |--------|--------------|----------|
- | `ciel_monitor.py` | Engine cycle, CIEL state | 1s |

### CIELingo Audit

- | Skrypt | Cel |
- |--------|-----|
- | `cielingo_canonization_audit.py` | Canon integrity check |

### Debug Surface (36D)

- | Odchylenie | Diagnoza |
- |------------|----------|
- | phi ~ uniform | brak synchronizacji |

### Audit Consolidator

- Key: `(timestamp, event, source)` — jeśli triplet istnieje, skip.

### Holonomic Audit

- | Sektor | Źródło | Orbital |
- |--------|--------|---------|
- | CPU | /proc/stat | M4 (perception) |

### Holonomic Doctor

- `src/noema_holonomic_doctor/`
- `src/ciel_geometry/doctor_reports/`
- - `scripts/catalog_zips_noema.py`

## Jak używać

```python
skill("workben-debug")
```

Ładuje wiedzę ze wszystkich 13 źródłowych skilli.
Źródłowe skille pozostają nietknięte w repozytorium.
