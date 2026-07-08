---
name: system-health-check
priority: 1
description: >
  >
---
# Health Check

## 1. Daemony

```bash
systemctl --user list-units 'noema-*'
```
Oczekiwane: 10-12 ● active. Żadnego dead.

## 2. Registry

```bash
python3 scripts/noema_register_cli.py scan
```
Oczekiwane: wszystkie daemony heartbeat < 6s.

## 3. Surface coherence

```bash
python3 scripts/noema_status.py | grep coherence
```
R_coherence ~0.5-0.9. < 0.3 → problem.

## 4. CIEL state

```bash
python3 scripts/noema_status.py | grep "closure"
```
closure_penalty: < 0.15 → deep, 0.15-0.35 → standard, > 0.35 → safe.

## 5. Energia

```bash
python3 scripts/noema_status.py | grep unruh
```
unruh_power > 1.0 → WARP active. semantic_density zbyt wysoki → TARDIS zwalnia.

## Interpretacja

| Sygnał | Znaczenie | Akcja |
|--------|-----------|-------|
| R < 0.3 | Phase chaos | restart kuramoto |
| closure > 0.35 | CIEL stress | safe mode, reduce PMNS blend |
| stale daemons | Registry >6s | noema_watchdog restart |
| unruh = 0 | WARP dead | check daemon tick |
